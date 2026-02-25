# OpenClaw Gateway & Operations Reference

Configuration, security, sandboxing, protocols, networking, remote access, web interfaces.


---
## Gateway > Authentication

[Source: https://docs.openclaw.ai/gateway/authentication]

Authentication - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Configuration and operations
Authentication
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
Gateway
Gateway Runbook
Configuration and operations
Configuration
Configuration Reference
Configuration Examples
Authentication
Trusted proxy auth
Health Checks
Heartbeat
Doctor
Logging
Gateway Lock
Background Exec and Process Tool
Multiple Gateways
Troubleshooting
Security and sandboxing
Protocols and APIs
Networking and discovery
Remote access
Remote Access
Remote Gateway Setup
Tailscale
Security
Formal Verification (Security Models)
Web interfaces
Web
Control UI
Dashboard
WebChat
TUI
Authentication
Recommended Anthropic setup (API key)
Anthropic: setup-token (subscription auth)
Checking model auth status
Controlling which credential is used
Per-session (chat command)
Per-agent (CLI override)
Troubleshooting
“No credentials found”
Token expiring/expired
Requirements
Configuration and operations
Authentication
Authentication
OpenClaw supports OAuth and API keys for model providers. For Anthropic
accounts, we recommend using an
API key
. For Claude subscription access,
use the long‑lived token created by
claude setup-token
See
/concepts/oauth
for the full OAuth flow and storage
layout.
Recommended Anthropic setup (API key)
If you’re using Anthropic directly, use an API key.
Create an API key in the Anthropic Console.
Put it on the
gateway host
(the machine running
openclaw gateway
Copy
export
ANTHROPIC_API_KEY
&quot;...&quot;
openclaw
models
status
If the Gateway runs under systemd/launchd, prefer putting the key in
~/.openclaw/.env
so the daemon can read it:
Copy
cat
&gt;&gt;
~/.openclaw/.env
&lt;&lt;
&#x27;EOF&#x27;
ANTHROPIC_API_KEY=...
EOF
Then restart the daemon (or restart your Gateway process) and re-check:
Copy
openclaw
models
status
openclaw
doctor
If you’d rather not manage env vars yourself, the onboarding wizard can store
API keys for daemon use:
openclaw onboard
See
Help
for details on env inheritance (
env.shellEnv
~/.openclaw/.env
, systemd/launchd).
Anthropic: setup-token (subscription auth)
For Anthropic, the recommended path is an
API key
. If you’re using a Claude
subscription, the setup-token flow is also supported. Run it on the
gateway host
Copy
claude
setup-token
Then paste it into OpenClaw:
Copy
openclaw
models
auth
setup-token
--provider
anthropic
If the token was created on another machine, paste it manually:
Copy
openclaw
models
auth
paste-token
--provider
anthropic
If you see an Anthropic error like:
Copy
This credential is only authorized for use with Claude Code and cannot be used for other API requests.
…use an Anthropic API key instead.
Manual token entry (any provider; writes
auth-profiles.json
+ updates config):
Copy
openclaw
models
auth
paste-token
--provider
anthropic
openclaw
models
auth
paste-token
--provider
openrouter
Automation-friendly check (exit
when expired/missing,
when expiring):
Copy
openclaw
models
status
--check
Optional ops scripts (systemd/Termux) are documented here:
/automation/auth-monitoring
claude setup-token
requires an interactive TTY.
Checking model auth status
Copy
openclaw
models
status
openclaw
doctor
Controlling which credential is used
Per-session (chat command)
Use
/model &lt;alias-or-id&gt;@&lt;profileId&gt;
to pin a specific provider credential for the current session (example profile ids:
anthropic:default
anthropic:work
Use
/model
(or
/model list
) for a compact picker; use
/model status
for the full view (candidates + next auth profile, plus provider endpoint details when configured).
Per-agent (CLI override)
Set an explicit auth profile order override for an agent (stored in that agent’s
auth-profiles.json
Copy
openclaw
models
auth
order
get
--provider
anthropic
openclaw
models
auth
order
set
--provider
anthropic
anthropic:default
openclaw
models
auth
order
clear
--provider
anthropic
Use
--agent &lt;id&gt;
to target a specific agent; omit it to use the configured default agent.
Troubleshooting
“No credentials found”
If the Anthropic token profile is missing, run
claude setup-token
on the
gateway host
, then re-check:
Copy
openclaw
models
status
Token expiring/expired
Run
openclaw models status
to confirm which profile is expiring. If the profile
is missing, rerun
claude setup-token
and paste the token again.
Requirements
Claude Max or Pro subscription (for
claude setup-token
Claude Code CLI installed (
claude
command available)
Configuration Examples
Trusted proxy auth

---
## Gateway > Background Process

[Source: https://docs.openclaw.ai/gateway/background-process]

Background Exec and Process Tool - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Configuration and operations
Background Exec and Process Tool
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
Gateway
Gateway Runbook
Configuration and operations
Configuration
Configuration Reference
Configuration Examples
Authentication
Trusted proxy auth
Health Checks
Heartbeat
Doctor
Logging
Gateway Lock
Background Exec and Process Tool
Multiple Gateways
Troubleshooting
Security and sandboxing
Protocols and APIs
Networking and discovery
Remote access
Remote Access
Remote Gateway Setup
Tailscale
Security
Formal Verification (Security Models)
Web interfaces
Web
Control UI
Dashboard
WebChat
TUI
Background Exec + Process Tool
exec tool
Child process bridging
process tool
Examples
Configuration and operations
Background Exec and Process Tool
Background Exec + Process Tool
OpenClaw runs shell commands through the
exec
tool and keeps long‑running tasks in memory. The
process
tool manages those background sessions.
exec tool
Key parameters:
command
(required)
yieldMs
(default 10000): auto‑background after this delay
background
(bool): background immediately
timeout
(seconds, default 1800): kill the process after this timeout
elevated
(bool): run on host if elevated mode is enabled/allowed
Need a real TTY? Set
pty: true
workdir
env
Behavior:
Foreground runs return output directly.
When backgrounded (explicit or timeout), the tool returns
status: &quot;running&quot;
sessionId
and a short tail.
Output is kept in memory until the session is polled or cleared.
If the
process
tool is disallowed,
exec
runs synchronously and ignores
yieldMs
background
Child process bridging
When spawning long-running child processes outside the exec/process tools (for example, CLI respawns or gateway helpers), attach the child-process bridge helper so termination signals are forwarded and listeners are detached on exit/error. This avoids orphaned processes on systemd and keeps shutdown behavior consistent across platforms.
Environment overrides:
PI_BASH_YIELD_MS
: default yield (ms)
PI_BASH_MAX_OUTPUT_CHARS
: in‑memory output cap (chars)
OPENCLAW_BASH_PENDING_MAX_OUTPUT_CHARS
: pending stdout/stderr cap per stream (chars)
PI_BASH_JOB_TTL_MS
: TTL for finished sessions (ms, bounded to 1m–3h)
Config (preferred):
tools.exec.backgroundMs
(default 10000)
tools.exec.timeoutSec
(default 1800)
tools.exec.cleanupMs
(default 1800000)
tools.exec.notifyOnExit
(default true): enqueue a system event + request heartbeat when a backgrounded exec exits.
tools.exec.notifyOnExitEmptySuccess
(default false): when true, also enqueue completion events for successful backgrounded runs that produced no output.
process tool
Actions:
list
: running + finished sessions
poll
: drain new output for a session (also reports exit status)
log
: read the aggregated output (supports
offset
limit
write
: send stdin (
data
, optional
eof
kill
: terminate a background session
clear
: remove a finished session from memory
remove
: kill if running, otherwise clear if finished
Notes:
Only backgrounded sessions are listed/persisted in memory.
Sessions are lost on process restart (no disk persistence).
Session logs are only saved to chat history if you run
process poll/log
and the tool result is recorded.
process
is scoped per agent; it only sees sessions started by that agent.
process list
includes a derived
name
(command verb + target) for quick scans.
process log
uses line-based
offset
limit
When both
offset
and
limit
are omitted, it returns the last 200 lines and includes a paging hint.
When
offset
is provided and
limit
is omitted, it returns from
offset
to the end (not capped to 200).
Examples
Run a long task and poll later:
Copy
&quot;tool&quot;
&quot;exec&quot;
&quot;command&quot;
&quot;sleep 5 &amp;&amp; echo done&quot;
&quot;yieldMs&quot;
1000
Copy
&quot;tool&quot;
&quot;process&quot;
&quot;action&quot;
&quot;poll&quot;
&quot;sessionId&quot;
&quot;&lt;id&gt;&quot;
Start immediately in background:
Copy
&quot;tool&quot;
&quot;exec&quot;
&quot;command&quot;
&quot;npm run build&quot;
&quot;background&quot;
true
Send stdin:
Copy
&quot;tool&quot;
&quot;process&quot;
&quot;action&quot;
&quot;write&quot;
&quot;sessionId&quot;
&quot;&lt;id&gt;&quot;
&quot;data&quot;
&quot;y\n&quot;
Gateway Lock
Multiple Gateways

---
## Gateway > Bonjour

[Source: https://docs.openclaw.ai/gateway/bonjour]

Bonjour Discovery - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Networking and discovery
Bonjour Discovery
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
Gateway
Gateway Runbook
Configuration and operations
Security and sandboxing
Protocols and APIs
Networking and discovery
Network model
Gateway-Owned Pairing
Discovery and Transports
Bonjour Discovery
Remote access
Remote Access
Remote Gateway Setup
Tailscale
Security
Formal Verification (Security Models)
Web interfaces
Web
Control UI
Dashboard
WebChat
TUI
Bonjour / mDNS discovery
Wide‑area Bonjour (Unicast DNS‑SD) over Tailscale
Gateway config (recommended)
One‑time DNS server setup (gateway host)
Tailscale DNS settings
Gateway listener security (recommended)
What advertises
Service types
TXT keys (non‑secret hints)
Debugging on macOS
Debugging in Gateway logs
Debugging on iOS node
Common failure modes
Escaped instance names (\032)
Disabling / configuration
Related docs
Networking and discovery
Bonjour Discovery
Bonjour / mDNS discovery
OpenClaw uses Bonjour (mDNS / DNS‑SD) as a
LAN‑only convenience
to discover
an active Gateway (WebSocket endpoint). It is best‑effort and does
not
replace SSH or
Tailnet-based connectivity.
Wide‑area Bonjour (Unicast DNS‑SD) over Tailscale
If the node and gateway are on different networks, multicast mDNS won’t cross the
boundary. You can keep the same discovery UX by switching to
unicast DNS‑SD
(“Wide‑Area Bonjour”) over Tailscale.
High‑level steps:
Run a DNS server on the gateway host (reachable over Tailnet).
Publish DNS‑SD records for
_openclaw-gw._tcp
under a dedicated zone
(example:
openclaw.internal.
Configure Tailscale
split DNS
so your chosen domain resolves via that
DNS server for clients (including iOS).
OpenClaw supports any discovery domain;
openclaw.internal.
is just an example.
iOS/Android nodes browse both
local.
and your configured wide‑area domain.
Gateway config (recommended)
Copy
gateway
bind
&quot;tailnet&quot;
// tailnet-only (recommended)
discovery
wideArea
enabled
true
} }
// enables wide-area DNS-SD publishing
One‑time DNS server setup (gateway host)
Copy
openclaw
dns
setup
--apply
This installs CoreDNS and configures it to:
listen on port 53 only on the gateway’s Tailscale interfaces
serve your chosen domain (example:
openclaw.internal.
) from
~/.openclaw/dns/&lt;domain&gt;.db
Validate from a tailnet‑connected machine:
Copy
dns-sd
_openclaw-gw._tcp
openclaw.internal.
dig
&lt;
TAILNET_IPV
4&gt;
_openclaw-gw._tcp.openclaw.internal
PTR
+short
Tailscale DNS settings
In the Tailscale admin console:
Add a nameserver pointing at the gateway’s tailnet IP (UDP/TCP 53).
Add split DNS so your discovery domain uses that nameserver.
Once clients accept tailnet DNS, iOS nodes can browse
_openclaw-gw._tcp
in your discovery domain without multicast.
Gateway listener security (recommended)
The Gateway WS port (default
18789
) binds to loopback by default. For LAN/tailnet
access, bind explicitly and keep auth enabled.
For tailnet‑only setups:
Set
gateway.bind: &quot;tailnet&quot;
~/.openclaw/openclaw.json
Restart the Gateway (or restart the macOS menubar app).
What advertises
Only the Gateway advertises
_openclaw-gw._tcp
Service types
_openclaw-gw._tcp
— gateway transport beacon (used by macOS/iOS/Android nodes).
TXT keys (non‑secret hints)
The Gateway advertises small non‑secret hints to make UI flows convenient:
role=gateway
displayName=&lt;friendly name&gt;
lanHost=&lt;hostname&gt;.local
gatewayPort=&lt;port&gt;
(Gateway WS + HTTP)
gatewayTls=1
(only when TLS is enabled)
gatewayTlsSha256=&lt;sha256&gt;
(only when TLS is enabled and fingerprint is available)
canvasPort=&lt;port&gt;
(only when the canvas host is enabled; currently the same as
gatewayPort
sshPort=&lt;port&gt;
(defaults to 22 when not overridden)
transport=gateway
cliPath=&lt;path&gt;
(optional; absolute path to a runnable
openclaw
entrypoint)
tailnetDns=&lt;magicdns&gt;
(optional hint when Tailnet is available)
Security notes:
Bonjour/mDNS TXT records are
unauthenticated
. Clients must not treat TXT as authoritative routing.
Clients should route using the resolved service endpoint (SRV + A/AAAA). Treat
lanHost
tailnetDns
gatewayPort
, and
gatewayTlsSha256
as hints only.
TLS pinning must never allow an advertised
gatewayTlsSha256
to override a previously stored pin.
iOS/Android nodes should treat discovery-based direct connects as
TLS-only
and require explicit user confirmation before trusting a first-time fingerprint.
Debugging on macOS
Useful built‑in tools:
Browse instances:
Copy
dns-sd
_openclaw-gw._tcp
local.
Resolve one instance (replace
&lt;instance&gt;
Copy
dns-sd
&quot;&lt;instance&gt;&quot;
_openclaw-gw._tcp
local.
If browsing works but resolving fails, you’re usually hitting a LAN policy or
mDNS resolver issue.
Debugging in Gateway logs
The Gateway writes a rolling log file (printed on startup as
gateway log file: ...
). Look for
bonjour:
lines, especially:
bonjour: advertise failed ...
bonjour: ... name conflict resolved
hostname conflict resolved
bonjour: watchdog detected non-announced service ...
Debugging on iOS node
The iOS node uses
NWBrowser
to discover
_openclaw-gw._tcp
To capture logs:
Settings → Gateway → Advanced →
Discovery Debug Logs
Settings → Gateway → Advanced →
Discovery Logs
→ reproduce →
Copy
The log includes browser state transitions and result‑set changes.
Common failure modes
Bonjour doesn’t cross networks
: use Tailnet or SSH.
Multicast blocked
: some Wi‑Fi networks disable mDNS.
Sleep / interface churn
: macOS may temporarily drop mDNS results; retry.
Browse works but resolve fails
: keep machine names simple (avoid emojis or
punctuation), then restart the Gateway. The service instance name derives from
the host name, so overly complex names can confuse some resolvers.
Escaped instance names (
\032
Bonjour/DNS‑SD often escapes bytes in service instance names as decimal
\DDD
sequences (e.g. spaces become
\032
This is normal at the protocol level.
UIs should decode for display (iOS uses
BonjourEscapes.decode
Disabling / configuration
OPENCLAW_DISABLE_BONJOUR=1
disables advertising (legacy:
OPENCLAW_DISABLE_BONJOUR
gateway.bind
~/.openclaw/openclaw.json
controls the Gateway bind mode.
OPENCLAW_SSH_PORT
overrides the SSH port advertised in TXT (legacy:
OPENCLAW_SSH_PORT
OPENCLAW_TAILNET_DNS
publishes a MagicDNS hint in TXT (legacy:
OPENCLAW_TAILNET_DNS
OPENCLAW_CLI_PATH
overrides the advertised CLI path (legacy:
OPENCLAW_CLI_PATH
Related docs
Discovery policy and transport selection:
Discovery
Node pairing + approvals:
Gateway pairing
Discovery and Transports
Remote Access

---
## Gateway > Bridge Protocol

[Source: https://docs.openclaw.ai/gateway/bridge-protocol]

Bridge Protocol - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Protocols and APIs
Bridge Protocol
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
Gateway
Gateway Runbook
Configuration and operations
Security and sandboxing
Protocols and APIs
Gateway Protocol
Bridge Protocol
OpenAI Chat Completions
Tools Invoke API
CLI Backends
Local Models
Networking and discovery
Remote access
Remote Access
Remote Gateway Setup
Tailscale
Security
Formal Verification (Security Models)
Web interfaces
Web
Control UI
Dashboard
WebChat
TUI
Bridge protocol (legacy node transport)
Why we have both
Transport
Handshake + pairing
Frames
Exec lifecycle events
Tailnet usage
Versioning
Protocols and APIs
Bridge Protocol
Bridge protocol (legacy node transport)
The Bridge protocol is a
legacy
node transport (TCP JSONL). New node clients
should use the unified Gateway WebSocket protocol instead.
If you are building an operator or node client, use the
Gateway protocol
Note:
Current OpenClaw builds no longer ship the TCP bridge listener; this document is kept for historical reference.
Legacy
bridge.*
config keys are no longer part of the config schema.
Why we have both
Security boundary
: the bridge exposes a small allowlist instead of the
full gateway API surface.
Pairing + node identity
: node admission is owned by the gateway and tied
to a per-node token.
Discovery UX
: nodes can discover gateways via Bonjour on LAN, or connect
directly over a tailnet.
Loopback WS
: the full WS control plane stays local unless tunneled via SSH.
Transport
TCP, one JSON object per line (JSONL).
Optional TLS (when
bridge.tls.enabled
is true).
Legacy default listener port was
18790
(current builds do not start a TCP bridge).
When TLS is enabled, discovery TXT records include
bridgeTls=1
plus
bridgeTlsSha256
as a non-secret hint. Note that Bonjour/mDNS TXT records are
unauthenticated; clients must not treat the advertised fingerprint as an
authoritative pin without explicit user intent or other out-of-band verification.
Handshake + pairing
Client sends
hello
with node metadata + token (if already paired).
If not paired, gateway replies
error
NOT_PAIRED
UNAUTHORIZED
Client sends
pair-request
Gateway waits for approval, then sends
pair-ok
and
hello-ok
hello-ok
returns
serverName
and may include
canvasHostUrl
Frames
Client → Gateway:
req
res
: scoped gateway RPC (chat, sessions, config, health, voicewake, skills.bins)
event
: node signals (voice transcript, agent request, chat subscribe, exec lifecycle)
Gateway → Client:
invoke
invoke-res
: node commands (
canvas.*
camera.*
screen.record
location.get
sms.send
event
: chat updates for subscribed sessions
ping
pong
: keepalive
Legacy allowlist enforcement lived in
src/gateway/server-bridge.ts
(removed).
Exec lifecycle events
Nodes can emit
exec.finished
exec.denied
events to surface system.run activity.
These are mapped to system events in the gateway. (Legacy nodes may still emit
exec.started
Payload fields (all optional unless noted):
sessionKey
(required): agent session to receive the system event.
runId
: unique exec id for grouping.
command
: raw or formatted command string.
exitCode
timedOut
success
output
: completion details (finished only).
reason
: denial reason (denied only).
Tailnet usage
Bind the bridge to a tailnet IP:
bridge.bind: &quot;tailnet&quot;
~/.openclaw/openclaw.json
Clients connect via MagicDNS name or tailnet IP.
Bonjour does
not
cross networks; use manual host/port or wide-area DNS‑SD
when needed.
Versioning
Bridge is currently
implicit v1
(no min/max negotiation). Backward‑compat
is expected; add a bridge protocol version field before any breaking changes.
Gateway Protocol
OpenAI Chat Completions

---
## Gateway > Cli Backends

[Source: https://docs.openclaw.ai/gateway/cli-backends]

CLI Backends - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Protocols and APIs
CLI Backends
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
Gateway
Gateway Runbook
Configuration and operations
Security and sandboxing
Protocols and APIs
Gateway Protocol
Bridge Protocol
OpenAI Chat Completions
Tools Invoke API
CLI Backends
Local Models
Networking and discovery
Remote access
Remote Access
Remote Gateway Setup
Tailscale
Security
Formal Verification (Security Models)
Web interfaces
Web
Control UI
Dashboard
WebChat
TUI
CLI backends (fallback runtime)
Beginner-friendly quick start
Using it as a fallback
Configuration overview
Example configuration
How it works
Sessions
Images (pass-through)
Inputs / outputs
Defaults (built-in)
Limitations
Troubleshooting
Protocols and APIs
CLI Backends
CLI backends (fallback runtime)
OpenClaw can run
local AI CLIs
as a
text-only fallback
when API providers are down,
rate-limited, or temporarily misbehaving. This is intentionally conservative:
Tools are disabled
(no tool calls).
Text in → text out
(reliable).
Sessions are supported
(so follow-up turns stay coherent).
Images can be passed through
if the CLI accepts image paths.
This is designed as a
safety net
rather than a primary path. Use it when you
want “always works” text responses without relying on external APIs.
Beginner-friendly quick start
You can use Claude Code CLI
without any config
(OpenClaw ships a built-in default):
Copy
openclaw
agent
--message
&quot;hi&quot;
--model
claude-cli/opus-4.6
Codex CLI also works out of the box:
Copy
openclaw
agent
--message
&quot;hi&quot;
--model
codex-cli/gpt-5.3-codex
If your gateway runs under launchd/systemd and PATH is minimal, add just the
command path:
Copy
agents
defaults
cliBackends
&quot;claude-cli&quot;
command
&quot;/opt/homebrew/bin/claude&quot;
That’s it. No keys, no extra auth config needed beyond the CLI itself.
Using it as a fallback
Add a CLI backend to your fallback list so it only runs when primary models fail:
Copy
agents
defaults
model
primary
&quot;anthropic/claude-opus-4-6&quot;
fallbacks
&quot;claude-cli/opus-4.6&quot;
&quot;claude-cli/opus-4.5&quot;
models
&quot;anthropic/claude-opus-4-6&quot;
alias
&quot;Opus&quot;
&quot;claude-cli/opus-4.6&quot;
&quot;claude-cli/opus-4.5&quot;
Notes:
If you use
agents.defaults.models
(allowlist), you must include
claude-cli/...
If the primary provider fails (auth, rate limits, timeouts), OpenClaw will
try the CLI backend next.
Configuration overview
All CLI backends live under:
Copy
agents.defaults.cliBackends
Each entry is keyed by a
provider id
(e.g.
claude-cli
my-cli
The provider id becomes the left side of your model ref:
Copy
&lt;provider&gt;/&lt;model&gt;
Example configuration
Copy
agents
defaults
cliBackends
&quot;claude-cli&quot;
command
&quot;/opt/homebrew/bin/claude&quot;
&quot;my-cli&quot;
command
&quot;my-cli&quot;
args
&quot;--json&quot;
output
&quot;json&quot;
input
&quot;arg&quot;
modelArg
&quot;--model&quot;
modelAliases
&quot;claude-opus-4-6&quot;
&quot;opus&quot;
&quot;claude-opus-4-5&quot;
&quot;opus&quot;
&quot;claude-sonnet-4-5&quot;
&quot;sonnet&quot;
sessionArg
&quot;--session&quot;
sessionMode
&quot;existing&quot;
sessionIdFields
&quot;session_id&quot;
&quot;conversation_id&quot;
systemPromptArg
&quot;--system&quot;
systemPromptWhen
&quot;first&quot;
imageArg
&quot;--image&quot;
imageMode
&quot;repeat&quot;
serialize
true
How it works
Selects a backend
based on the provider prefix (
claude-cli/...
Builds a system prompt
using the same OpenClaw prompt + workspace context.
Executes the CLI
with a session id (if supported) so history stays consistent.
Parses output
(JSON or plain text) and returns the final text.
Persists session ids
per backend, so follow-ups reuse the same CLI session.
Sessions
If the CLI supports sessions, set
sessionArg
(e.g.
--session-id
) or
sessionArgs
(placeholder
{sessionId}
) when the ID needs to be inserted
into multiple flags.
If the CLI uses a
resume subcommand
with different flags, set
resumeArgs
(replaces
args
when resuming) and optionally
resumeOutput
(for non-JSON resumes).
sessionMode
always
: always send a session id (new UUID if none stored).
existing
: only send a session id if one was stored before.
none
: never send a session id.
Images (pass-through)
If your CLI accepts image paths, set
imageArg
Copy
imageArg:
&quot;--image&quot;
imageMode:
&quot;repeat&quot;
OpenClaw will write base64 images to temp files. If
imageArg
is set, those
paths are passed as CLI args. If
imageArg
is missing, OpenClaw appends the
file paths to the prompt (path injection), which is enough for CLIs that auto-
load local files from plain paths (Claude Code CLI behavior).
Inputs / outputs
output: &quot;json&quot;
(default) tries to parse JSON and extract text + session id.
output: &quot;jsonl&quot;
parses JSONL streams (Codex CLI
--json
) and extracts the
last agent message plus
thread_id
when present.
output: &quot;text&quot;
treats stdout as the final response.
Input modes:
input: &quot;arg&quot;
(default) passes the prompt as the last CLI arg.
input: &quot;stdin&quot;
sends the prompt via stdin.
If the prompt is very long and
maxPromptArgChars
is set, stdin is used.
Defaults (built-in)
OpenClaw ships a default for
claude-cli
command: &quot;claude&quot;
args: [&quot;-p&quot;, &quot;--output-format&quot;, &quot;json&quot;, &quot;--dangerously-skip-permissions&quot;]
resumeArgs: [&quot;-p&quot;, &quot;--output-format&quot;, &quot;json&quot;, &quot;--dangerously-skip-permissions&quot;, &quot;--resume&quot;, &quot;{sessionId}&quot;]
modelArg: &quot;--model&quot;
systemPromptArg: &quot;--append-system-prompt&quot;
sessionArg: &quot;--session-id&quot;
systemPromptWhen: &quot;first&quot;
sessionMode: &quot;always&quot;
OpenClaw also ships a default for
codex-cli
command: &quot;codex&quot;
args: [&quot;exec&quot;,&quot;--json&quot;,&quot;--color&quot;,&quot;never&quot;,&quot;--sandbox&quot;,&quot;read-only&quot;,&quot;--skip-git-repo-check&quot;]
resumeArgs: [&quot;exec&quot;,&quot;resume&quot;,&quot;{sessionId}&quot;,&quot;--color&quot;,&quot;never&quot;,&quot;--sandbox&quot;,&quot;read-only&quot;,&quot;--skip-git-repo-check&quot;]
output: &quot;jsonl&quot;
resumeOutput: &quot;text&quot;
modelArg: &quot;--model&quot;
imageArg: &quot;--image&quot;
sessionMode: &quot;existing&quot;
Override only if needed (common: absolute
command
path).
Limitations
No OpenClaw tools
(the CLI backend never receives tool calls). Some CLIs
may still run their own agent tooling.
No streaming
(CLI output is collected then returned).
Structured outputs
depend on the CLI’s JSON format.
Codex CLI sessions
resume via text output (no JSONL), which is less
structured than the initial
--json
run. OpenClaw sessions still work
normally.
Troubleshooting
CLI not found
: set
command
to a full path.
Wrong model name
: use
modelAliases
to map
provider/model
→ CLI model.
No session continuity
: ensure
sessionArg
is set and
sessionMode
is not
none
(Codex CLI currently cannot resume with JSON output).
Images ignored
: set
imageArg
(and verify CLI supports file paths).
Tools Invoke API
Local Models

---
## Gateway > Configuration Examples

[Source: https://docs.openclaw.ai/gateway/configuration-examples]

Configuration Examples - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Configuration and operations
Configuration Examples
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
Gateway
Gateway Runbook
Configuration and operations
Configuration
Configuration Reference
Configuration Examples
Authentication
Trusted proxy auth
Health Checks
Heartbeat
Doctor
Logging
Gateway Lock
Background Exec and Process Tool
Multiple Gateways
Troubleshooting
Security and sandboxing
Protocols and APIs
Networking and discovery
Remote access
Remote Access
Remote Gateway Setup
Tailscale
Security
Formal Verification (Security Models)
Web interfaces
Web
Control UI
Dashboard
WebChat
TUI
Configuration Examples
Quick start
Absolute minimum
Recommended starter
Expanded example (major options)
Common patterns
Multi-platform setup
Secure DM mode (shared inbox / multi-user DMs)
OAuth with API key failover
Anthropic subscription + API key, MiniMax fallback
Work bot (restricted access)
Local models only
Tips
Configuration and operations
Configuration Examples
Configuration Examples
Examples below are aligned with the current config schema. For the exhaustive reference and per-field notes, see
Configuration
Quick start
Absolute minimum
Copy
agent
workspace
&quot;~/.openclaw/workspace&quot;
channels
whatsapp
allowFrom
&quot;+15555550123&quot;
] } }
Save to
~/.openclaw/openclaw.json
and you can DM the bot from that number.
Recommended starter
Copy
identity
name
&quot;Clawd&quot;
theme
&quot;helpful assistant&quot;
emoji
&quot;🦞&quot;
agent
workspace
&quot;~/.openclaw/workspace&quot;
model
primary
&quot;anthropic/claude-sonnet-4-5&quot;
channels
whatsapp
allowFrom
&quot;+15555550123&quot;
groups
&quot;*&quot;
requireMention
true
} }
Expanded example (major options)
JSON5 lets you use comments and trailing commas. Regular JSON works too.
Copy
// Environment + shell
env
OPENROUTER_API_KEY
&quot;sk-or-...&quot;
vars
GROQ_API_KEY
&quot;gsk-...&quot;
shellEnv
enabled
true
timeoutMs
15000
// Auth profile metadata (secrets live in auth-profiles.json)
auth
profiles
&quot;anthropic:
[email&#160;protected]
&quot;
provider
&quot;anthropic&quot;
mode
&quot;oauth&quot;
email
&quot;
[email&#160;protected]
&quot;
&quot;anthropic:work&quot;
provider
&quot;anthropic&quot;
mode
&quot;api_key&quot;
&quot;openai:default&quot;
provider
&quot;openai&quot;
mode
&quot;api_key&quot;
&quot;openai-codex:default&quot;
provider
&quot;openai-codex&quot;
mode
&quot;oauth&quot;
order
anthropic
&quot;anthropic:
[email&#160;protected]
&quot;
&quot;anthropic:work&quot;
openai
&quot;openai:default&quot;
&quot;openai-codex&quot;
&quot;openai-codex:default&quot;
// Identity
identity
name
&quot;Samantha&quot;
theme
&quot;helpful sloth&quot;
emoji
&quot;🦥&quot;
// Logging
logging
level
&quot;info&quot;
file
&quot;/tmp/openclaw/openclaw.log&quot;
consoleLevel
&quot;info&quot;
consoleStyle
&quot;pretty&quot;
redactSensitive
&quot;tools&quot;
// Message formatting
messages
messagePrefix
&quot;[openclaw]&quot;
responsePrefix
&quot;&gt;&quot;
ackReaction
&quot;👀&quot;
ackReactionScope
&quot;group-mentions&quot;
// Routing + queue
routing
groupChat
mentionPatterns
&quot;@openclaw&quot;
&quot;openclaw&quot;
historyLimit
queue
mode
&quot;collect&quot;
debounceMs
1000
cap
drop
&quot;summarize&quot;
byChannel
whatsapp
&quot;collect&quot;
telegram
&quot;collect&quot;
discord
&quot;collect&quot;
slack
&quot;collect&quot;
signal
&quot;collect&quot;
imessage
&quot;collect&quot;
webchat
&quot;collect&quot;
// Tooling
tools
media
audio
enabled
true
maxBytes
20971520
models
provider
&quot;openai&quot;
model
&quot;gpt-4o-mini-transcribe&quot;
// Optional CLI fallback (Whisper binary):
// { type: &quot;cli&quot;, command: &quot;whisper&quot;, args: [&quot;--model&quot;, &quot;base&quot;, &quot;{{MediaPath}}&quot;] }
timeoutSeconds
120
video
enabled
true
maxBytes
52428800
models
provider
&quot;google&quot;
model
&quot;gemini-3-flash-preview&quot;
// Session behavior
session
scope
&quot;per-sender&quot;
reset
mode
&quot;daily&quot;
atHour
idleMinutes
resetByChannel
discord
mode
&quot;idle&quot;
idleMinutes
10080 }
resetTriggers
&quot;/new&quot;
&quot;/reset&quot;
store
&quot;~/.openclaw/agents/default/sessions/sessions.json&quot;
maintenance
mode
&quot;warn&quot;
pruneAfter
&quot;30d&quot;
maxEntries
500
rotateBytes
&quot;10mb&quot;
typingIntervalSeconds
sendPolicy
default
&quot;allow&quot;
rules
action
&quot;deny&quot;
match
channel
&quot;discord&quot;
chatType
&quot;group&quot;
} }]
// Channels
channels
whatsapp
dmPolicy
&quot;pairing&quot;
allowFrom
&quot;+15555550123&quot;
groupPolicy
&quot;allowlist&quot;
groupAllowFrom
&quot;+15555550123&quot;
groups
&quot;*&quot;
requireMention
true
} }
telegram
enabled
true
botToken
&quot;YOUR_TELEGRAM_BOT_TOKEN&quot;
allowFrom
&quot;123456789&quot;
groupPolicy
&quot;allowlist&quot;
groupAllowFrom
&quot;123456789&quot;
groups
&quot;*&quot;
requireMention
true
} }
discord
enabled
true
token
&quot;YOUR_DISCORD_BOT_TOKEN&quot;
enabled
true
allowFrom
&quot;steipete&quot;
] }
guilds
&quot;123456789012345678&quot;
slug
&quot;friends-of-openclaw&quot;
requireMention
false
channels
general
allow
true
help
allow
true
requireMention
true
slack
enabled
true
botToken
&quot;xoxb-REPLACE_ME&quot;
appToken
&quot;xapp-REPLACE_ME&quot;
channels
&quot;#general&quot;
allow
true
requireMention
true
enabled
true
allowFrom
&quot;U123&quot;
] }
slashCommand
enabled
true
name
&quot;openclaw&quot;
sessionPrefix
&quot;slack:slash&quot;
ephemeral
true
// Agent runtime
agents
defaults
workspace
&quot;~/.openclaw/workspace&quot;
userTimezone
&quot;America/Chicago&quot;
model
primary
&quot;anthropic/claude-sonnet-4-5&quot;
fallbacks
&quot;anthropic/claude-opus-4-6&quot;
&quot;openai/gpt-5.2&quot;
imageModel
primary
&quot;openrouter/anthropic/claude-sonnet-4-5&quot;
models
&quot;anthropic/claude-opus-4-6&quot;
alias
&quot;opus&quot;
&quot;anthropic/claude-sonnet-4-5&quot;
alias
&quot;sonnet&quot;
&quot;openai/gpt-5.2&quot;
alias
&quot;gpt&quot;
thinkingDefault
&quot;low&quot;
verboseDefault
&quot;off&quot;
elevatedDefault
&quot;on&quot;
blockStreamingDefault
&quot;off&quot;
blockStreamingBreak
&quot;text_end&quot;
blockStreamingChunk
minChars
800
maxChars
1200
breakPreference
&quot;paragraph&quot;
blockStreamingCoalesce
idleMs
1000
humanDelay
mode
&quot;natural&quot;
timeoutSeconds
600
mediaMaxMb
typingIntervalSeconds
maxConcurrent
heartbeat
every
&quot;30m&quot;
model
&quot;anthropic/claude-sonnet-4-5&quot;
target
&quot;last&quot;
&quot;+15555550123&quot;
prompt
&quot;HEARTBEAT&quot;
ackMaxChars
300
memorySearch
provider
&quot;gemini&quot;
model
&quot;gemini-embedding-001&quot;
remote
apiKey
&quot;${GEMINI_API_KEY}&quot;
extraPaths
&quot;../team-docs&quot;
&quot;/srv/shared-notes&quot;
sandbox
mode
&quot;non-main&quot;
perSession
true
workspaceRoot
&quot;~/.openclaw/sandboxes&quot;
docker
image
&quot;openclaw-sandbox:bookworm-slim&quot;
workdir
&quot;/workspace&quot;
readOnlyRoot
true
tmpfs
&quot;/tmp&quot;
&quot;/var/tmp&quot;
&quot;/run&quot;
network
&quot;none&quot;
user
&quot;1000:1000&quot;
browser
enabled
false
tools
allow
&quot;exec&quot;
&quot;process&quot;
&quot;read&quot;
&quot;write&quot;
&quot;edit&quot;
&quot;apply_patch&quot;
deny
&quot;browser&quot;
&quot;canvas&quot;
exec
backgroundMs
10000
timeoutSec
1800
cleanupMs
1800000
elevated
enabled
true
allowFrom
whatsapp
&quot;+15555550123&quot;
telegram
&quot;123456789&quot;
discord
&quot;steipete&quot;
slack
&quot;U123&quot;
signal
&quot;+15555550123&quot;
imessage
&quot;
[email&#160;protected]
&quot;
webchat
&quot;session:demo&quot;
// Custom model providers
models
mode
&quot;merge&quot;
providers
&quot;custom-proxy&quot;
baseUrl
&quot;http://localhost:4000/v1&quot;
apiKey
&quot;LITELLM_KEY&quot;
api
&quot;openai-responses&quot;
authHeader
true
headers
&quot;X-Proxy-Region&quot;
&quot;us-west&quot;
models
&quot;llama-3.1-8b&quot;
name
&quot;Llama 3.1 8B&quot;
api
&quot;openai-responses&quot;
reasoning
false
input
&quot;text&quot;
cost
input
output
cacheRead
cacheWrite
0 }
contextWindow
128000
maxTokens
32000
// Cron jobs
cron
enabled
true
store
&quot;~/.openclaw/cron/cron.json&quot;
maxConcurrentRuns
sessionRetention
&quot;24h&quot;
// Webhooks
hooks
enabled
true
path
&quot;/hooks&quot;
token
&quot;shared-secret&quot;
presets
&quot;gmail&quot;
transformsDir
&quot;~/.openclaw/hooks/transforms&quot;
mappings
&quot;gmail-hook&quot;
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
&quot;From: {{messages[0].from}}\nSubject: {{messages[0].subject}}&quot;
textTemplate
&quot;{{messages[0].snippet}}&quot;
deliver
true
channel
&quot;last&quot;
&quot;+15555550123&quot;
thinking
&quot;low&quot;
timeoutSeconds
300
transform
module
&quot;gmail.js&quot;
export
&quot;transformGmail&quot;
gmail
account
&quot;
[email&#160;protected]
&quot;
label
&quot;INBOX&quot;
topic
&quot;projects/&lt;project-id&gt;/topics/gog-gmail-watch&quot;
subscription
&quot;gog-gmail-watch-push&quot;
pushToken
&quot;shared-push-token&quot;
hookUrl
&quot;http://127.0.0.1:18789/hooks/gmail&quot;
includeBody
true
maxBytes
20000
renewEveryMinutes
720
serve
bind
&quot;127.0.0.1&quot;
port
8788
path
&quot;/&quot;
tailscale
mode
&quot;funnel&quot;
path
&quot;/gmail-pubsub&quot;
// Gateway + networking
gateway
mode
&quot;local&quot;
port
18789
bind
&quot;loopback&quot;
controlUi
enabled
true
basePath
&quot;/openclaw&quot;
auth
mode
&quot;token&quot;
token
&quot;gateway-token&quot;
allowTailscale
true
tailscale
mode
&quot;serve&quot;
resetOnExit
false
remote
url
&quot;ws://gateway.tailnet:18789&quot;
token
&quot;remote-token&quot;
reload
mode
&quot;hybrid&quot;
debounceMs
300 }
skills
allowBundled
&quot;gemini&quot;
&quot;peekaboo&quot;
load
extraDirs
&quot;~/Projects/agent-scripts/skills&quot;
install
preferBrew
true
nodeManager
&quot;npm&quot;
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
Common patterns
Multi-platform setup
Copy
agent
workspace
&quot;~/.openclaw/workspace&quot;
channels
whatsapp
allowFrom
&quot;+15555550123&quot;
] }
telegram
enabled
true
botToken
&quot;YOUR_TOKEN&quot;
allowFrom
&quot;123456789&quot;
discord
enabled
true
token
&quot;YOUR_TOKEN&quot;
allowFrom
&quot;yourname&quot;
] }
Secure DM mode (shared inbox / multi-user DMs)
If more than one person can DM your bot (multiple entries in
allowFrom
, pairing approvals for multiple people, or
dmPolicy: &quot;open&quot;
), enable
secure DM mode
so DMs from different senders don’t share one context by default:
Copy
// Secure DM mode (recommended for multi-user or sensitive DM agents)
session
dmScope
&quot;per-channel-peer&quot;
channels
// Example: WhatsApp multi-user inbox
whatsapp
dmPolicy
&quot;allowlist&quot;
allowFrom
&quot;+15555550123&quot;
&quot;+15555550124&quot;
// Example: Discord multi-user inbox
discord
enabled
true
token
&quot;YOUR_DISCORD_BOT_TOKEN&quot;
enabled
true
allowFrom
&quot;alice&quot;
&quot;bob&quot;
] }
OAuth with API key failover
Copy
auth
profiles
&quot;anthropic:subscription&quot;
provider
&quot;anthropic&quot;
mode
&quot;oauth&quot;
email
&quot;
[email&#160;protected]
&quot;
&quot;anthropic:api&quot;
provider
&quot;anthropic&quot;
mode
&quot;api_key&quot;
order
anthropic
&quot;anthropic:subscription&quot;
&quot;anthropic:api&quot;
agent
workspace
&quot;~/.openclaw/workspace&quot;
model
primary
&quot;anthropic/claude-sonnet-4-5&quot;
fallbacks
&quot;anthropic/claude-opus-4-6&quot;
Anthropic subscription + API key, MiniMax fallback
Copy
auth
profiles
&quot;anthropic:subscription&quot;
provider
&quot;anthropic&quot;
mode
&quot;oauth&quot;
email
&quot;
[email&#160;protected]
&quot;
&quot;anthropic:api&quot;
provider
&quot;anthropic&quot;
mode
&quot;api_key&quot;
order
anthropic
&quot;anthropic:subscription&quot;
&quot;anthropic:api&quot;
models
providers
minimax
baseUrl
&quot;https://api.minimax.io/anthropic&quot;
api
&quot;anthropic-messages&quot;
apiKey
&quot;${MINIMAX_API_KEY}&quot;
agent
workspace
&quot;~/.openclaw/workspace&quot;
model
primary
&quot;anthropic/claude-opus-4-6&quot;
fallbacks
&quot;minimax/MiniMax-M2.1&quot;
Work bot (restricted access)
Copy
identity
name
&quot;WorkBot&quot;
theme
&quot;professional assistant&quot;
agent
workspace
&quot;~/work-openclaw&quot;
elevated
enabled
false
channels
slack
enabled
true
botToken
&quot;xoxb-...&quot;
channels
&quot;#engineering&quot;
allow
true
requireMention
true
&quot;#general&quot;
allow
true
requireMention
true
Local models only
Copy
agent
workspace
&quot;~/.openclaw/workspace&quot;
model
primary
&quot;lmstudio/minimax-m2.1-gs32&quot;
models
mode
&quot;merge&quot;
providers
lmstudio
baseUrl
&quot;http://127.0.0.1:1234/v1&quot;
apiKey
&quot;lmstudio&quot;
api
&quot;openai-responses&quot;
models
&quot;minimax-m2.1-gs32&quot;
name
&quot;MiniMax M2.1 GS32&quot;
reasoning
false
input
&quot;text&quot;
cost
input
output
cacheRead
cacheWrite
0 }
contextWindow
196608
maxTokens
8192
Tips
If you set
dmPolicy: &quot;open&quot;
, the matching
allowFrom
list must include
&quot;*&quot;
Provider IDs differ (phone numbers, user IDs, channel IDs). Use the provider docs to confirm the format.
Optional sections to add later:
web
browser
discovery
canvasHost
talk
signal
imessage
See
Providers
and
Troubleshooting
for deeper setup notes.
Configuration Reference
Authentication

---
## Gateway > Configuration Reference

[Source: https://docs.openclaw.ai/gateway/configuration-reference]

Configuration Reference - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Configuration and operations
Configuration Reference
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
Gateway
Gateway Runbook
Configuration and operations
Configuration
Configuration Reference
Configuration Examples
Authentication
Trusted proxy auth
Health Checks
Heartbeat
Doctor
Logging
Gateway Lock
Background Exec and Process Tool
Multiple Gateways
Troubleshooting
Security and sandboxing
Protocols and APIs
Networking and discovery
Remote access
Remote Access
Remote Gateway Setup
Tailscale
Security
Formal Verification (Security Models)
Web interfaces
Web
Control UI
Dashboard
WebChat
TUI
Configuration Reference
Channels
DM and group access
WhatsApp
Telegram
Discord
Google Chat
Slack
Mattermost
Signal
iMessage
Multi-account (all channels)
Group chat mention gating
DM history limits
Self-chat mode
Commands (chat command handling)
Agent defaults
agents.defaults.workspace
agents.defaults.repoRoot
agents.defaults.skipBootstrap
agents.defaults.bootstrapMaxChars
agents.defaults.bootstrapTotalMaxChars
agents.defaults.userTimezone
agents.defaults.timeFormat
agents.defaults.model
agents.defaults.cliBackends
agents.defaults.heartbeat
agents.defaults.compaction
agents.defaults.contextPruning
Block streaming
Typing indicators
agents.defaults.sandbox
agents.list (per-agent overrides)
Multi-agent routing
Binding match fields
Per-agent access profiles
Session
Messages
Response prefix
Ack reaction
Inbound debounce
TTS (text-to-speech)
Talk
Tools
Tool profiles
Tool groups
tools.allow / tools.deny
tools.byProvider
tools.elevated
tools.exec
tools.web
tools.media
tools.agentToAgent
tools.sessions
tools.subagents
Custom providers and base URLs
Provider examples
Skills
Plugins
Browser
Gateway
OpenAI-compatible endpoints
Multi-instance isolation
Hooks
Gmail integration
Canvas host
Discovery
mDNS (Bonjour)
Wide-area (DNS-SD)
Environment
env (inline env vars)
Env var substitution
Auth storage
Logging
Wizard
Identity
Bridge (legacy, removed)
Cron
Media model template variables
Config includes ($include)
Configuration and operations
Configuration Reference
Complete field-by-field reference for ~/.openclaw/openclaw.json
Configuration Reference
Every field available in
~/.openclaw/openclaw.json
. For a task-oriented overview, see
Configuration
Config format is
JSON5
(comments + trailing commas allowed). All fields are optional — OpenClaw uses safe defaults when omitted.
Channels
Each channel starts automatically when its config section exists (unless
enabled: false
DM and group access
All channels support DM policies and group policies:
DM policy
Behavior
pairing
(default)
Unknown senders get a one-time pairing code; owner must approve
allowlist
Only senders in
allowFrom
(or paired allow store)
open
Allow all inbound DMs (requires
allowFrom: [&quot;*&quot;]
disabled
Ignore all inbound DMs
Group policy
Behavior
allowlist
(default)
Only groups matching the configured allowlist
open
Bypass group allowlists (mention-gating still applies)
disabled
Block all group/room messages
channels.defaults.groupPolicy
sets the default when a provider’s
groupPolicy
is unset.
Pairing codes expire after 1 hour. Pending DM pairing requests are capped at
3 per channel
Slack/Discord have a special fallback: if their provider section is missing entirely, runtime group policy can resolve to
open
(with a startup warning).
WhatsApp
WhatsApp runs through the gateway’s web channel (Baileys Web). It starts automatically when a linked session exists.
Copy
channels
whatsapp
dmPolicy
&quot;pairing&quot;
// pairing | allowlist | open | disabled
allowFrom
&quot;+15555550123&quot;
&quot;+447700900123&quot;
textChunkLimit
4000
chunkMode
&quot;length&quot;
// length | newline
mediaMaxMb
sendReadReceipts
true
// blue ticks (false in self-chat mode)
groups
&quot;*&quot;
requireMention
true
groupPolicy
&quot;allowlist&quot;
groupAllowFrom
&quot;+15551234567&quot;
web
enabled
true
heartbeatSeconds
reconnect
initialMs
2000
maxMs
120000
factor
1.4
jitter
0.2
maxAttempts
Multi-account WhatsApp
Copy
channels
whatsapp
accounts
default
personal
biz
// authDir: &quot;~/.openclaw/credentials/whatsapp/biz&quot;,
Outbound commands default to account
default
if present; otherwise the first configured account id (sorted).
Legacy single-account Baileys auth dir is migrated by
openclaw doctor
into
whatsapp/default
Per-account overrides:
channels.whatsapp.accounts.&lt;id&gt;.sendReadReceipts
channels.whatsapp.accounts.&lt;id&gt;.dmPolicy
channels.whatsapp.accounts.&lt;id&gt;.allowFrom
Telegram
Copy
channels
telegram
enabled
true
botToken
&quot;your-bot-token&quot;
dmPolicy
&quot;pairing&quot;
allowFrom
&quot;tg:123456789&quot;
groups
&quot;*&quot;
requireMention
true
&quot;-1001234567890&quot;
allowFrom
&quot;@admin&quot;
systemPrompt
&quot;Keep answers brief.&quot;
topics
&quot;99&quot;
requireMention
false
skills
&quot;search&quot;
systemPrompt
&quot;Stay on topic.&quot;
customCommands
command
&quot;backup&quot;
description
&quot;Git backup&quot;
command
&quot;generate&quot;
description
&quot;Create an image&quot;
historyLimit
replyToMode
&quot;first&quot;
// off | first | all
linkPreview
true
streamMode
&quot;partial&quot;
// off | partial | block
draftChunk
minChars
200
maxChars
800
breakPreference
&quot;paragraph&quot;
// paragraph | newline | sentence
actions
reactions
true
sendMessage
true
reactionNotifications
&quot;own&quot;
// off | own | all
mediaMaxMb
retry
attempts
minDelayMs
400
maxDelayMs
30000
jitter
0.1
network
autoSelectFamily
false
proxy
&quot;socks5://localhost:9050&quot;
webhookUrl
&quot;https://example.com/telegram-webhook&quot;
webhookSecret
&quot;secret&quot;
webhookPath
&quot;/telegram-webhook&quot;
Bot token:
channels.telegram.botToken
channels.telegram.tokenFile
, with
TELEGRAM_BOT_TOKEN
as fallback for the default account.
configWrites: false
blocks Telegram-initiated config writes (supergroup ID migrations,
/config set|unset
Telegram stream previews use
sendMessage
editMessageText
(works in direct and group chats).
Retry policy: see
Retry policy
Discord
Copy
channels
discord
enabled
true
token
&quot;your-bot-token&quot;
mediaMaxMb
allowBots
false
actions
reactions
true
stickers
true
polls
true
permissions
true
messages
true
threads
true
pins
true
search
true
memberInfo
true
roleInfo
true
roles
false
channelInfo
true
voiceStatus
true
events
true
moderation
false
replyToMode
&quot;off&quot;
// off | first | all
dmPolicy
&quot;pairing&quot;
allowFrom
&quot;1234567890&quot;
&quot;steipete&quot;
enabled
true
groupEnabled
false
groupChannels
&quot;openclaw-dm&quot;
] }
guilds
&quot;123456789012345678&quot;
slug
&quot;friends-of-openclaw&quot;
requireMention
false
reactionNotifications
&quot;own&quot;
users
&quot;987654321098765432&quot;
channels
general
allow
true
help
allow
true
requireMention
true
users
&quot;987654321098765432&quot;
skills
&quot;docs&quot;
systemPrompt
&quot;Short answers only.&quot;
historyLimit
textChunkLimit
2000
chunkMode
&quot;length&quot;
// length | newline
maxLinesPerMessage
components
accentColor
&quot;#5865F2&quot;
retry
attempts
minDelayMs
500
maxDelayMs
30000
jitter
0.1
Token:
channels.discord.token
, with
DISCORD_BOT_TOKEN
as fallback for the default account.
Use
user:&lt;id&gt;
(DM) or
channel:&lt;id&gt;
(guild channel) for delivery targets; bare numeric IDs are rejected.
Guild slugs are lowercase with spaces replaced by
; channel keys use the slugged name (no
). Prefer guild IDs.
Bot-authored messages are ignored by default.
allowBots: true
enables them (own messages still filtered).
maxLinesPerMessage
(default 17) splits tall messages even when under 2000 chars.
channels.discord.ui.components.accentColor
sets the accent color for Discord components v2 containers.
Reaction notification modes:
off
(none),
own
(bot’s messages, default),
all
(all messages),
allowlist
(from
guilds.&lt;id&gt;.users
on all messages).
Google Chat
Copy
channels
googlechat
enabled
true
serviceAccountFile
&quot;/path/to/service-account.json&quot;
audienceType
&quot;app-url&quot;
// app-url | project-number
audience
&quot;https://gateway.example.com/googlechat&quot;
webhookPath
&quot;/googlechat&quot;
botUser
&quot;users/1234567890&quot;
enabled
true
policy
&quot;pairing&quot;
allowFrom
&quot;users/1234567890&quot;
groupPolicy
&quot;allowlist&quot;
groups
&quot;spaces/AAAA&quot;
allow
true
requireMention
true
actions
reactions
true
typingIndicator
&quot;message&quot;
mediaMaxMb
Service account JSON: inline (
serviceAccount
) or file-based (
serviceAccountFile
Env fallbacks:
GOOGLE_CHAT_SERVICE_ACCOUNT
GOOGLE_CHAT_SERVICE_ACCOUNT_FILE
Use
spaces/&lt;spaceId&gt;
users/&lt;userId|email&gt;
for delivery targets.
Slack
Copy
channels
slack
enabled
true
botToken
&quot;xoxb-...&quot;
appToken
&quot;xapp-...&quot;
dmPolicy
&quot;pairing&quot;
allowFrom
&quot;U123&quot;
&quot;U456&quot;
&quot;*&quot;
enabled
true
groupEnabled
false
groupChannels
&quot;G123&quot;
] }
channels
C123
allow
true
requireMention
true
allowBots
false
&quot;#general&quot;
allow
true
requireMention
true
allowBots
false
users
&quot;U123&quot;
skills
&quot;docs&quot;
systemPrompt
&quot;Short answers only.&quot;
historyLimit
allowBots
false
reactionNotifications
&quot;own&quot;
reactionAllowlist
&quot;U123&quot;
replyToMode
&quot;off&quot;
// off | first | all
thread
historyScope
&quot;thread&quot;
// thread | channel
inheritParent
false
actions
reactions
true
messages
true
pins
true
memberInfo
true
emojiList
true
slashCommand
enabled
true
name
&quot;openclaw&quot;
sessionPrefix
&quot;slack:slash&quot;
ephemeral
true
textChunkLimit
4000
chunkMode
&quot;length&quot;
mediaMaxMb
Socket mode
requires both
botToken
and
appToken
SLACK_BOT_TOKEN
SLACK_APP_TOKEN
for default account env fallback).
HTTP mode
requires
botToken
plus
signingSecret
(at root or per-account).
configWrites: false
blocks Slack-initiated config writes.
Use
user:&lt;id&gt;
(DM) or
channel:&lt;id&gt;
for delivery targets.
Reaction notification modes:
off
own
(default),
all
allowlist
(from
reactionAllowlist
Thread session isolation:
thread.historyScope
is per-thread (default) or shared across channel.
thread.inheritParent
copies parent channel transcript to new threads.
Action group
Default
Notes
reactions
enabled
React + list reactions
messages
enabled
Read/send/edit/delete
pins
enabled
Pin/unpin/list
memberInfo
enabled
Member info
emojiList
enabled
Custom emoji list
Mattermost
Mattermost ships as a plugin:
openclaw plugins install @openclaw/mattermost
Copy
channels
mattermost
enabled
true
botToken
&quot;mm-token&quot;
baseUrl
&quot;https://chat.example.com&quot;
dmPolicy
&quot;pairing&quot;
chatmode
&quot;oncall&quot;
// oncall | onmessage | onchar
oncharPrefixes
&quot;&gt;&quot;
&quot;!&quot;
textChunkLimit
4000
chunkMode
&quot;length&quot;
Chat modes:
oncall
(respond on @-mention, default),
onmessage
(every message),
onchar
(messages starting with trigger prefix).
Signal
Copy
channels
signal
reactionNotifications
&quot;own&quot;
// off | own | all | allowlist
reactionAllowlist
&quot;+15551234567&quot;
&quot;uuid:123e4567-e89b-12d3-a456-426614174000&quot;
historyLimit
Reaction notification modes:
off
own
(default),
all
allowlist
(from
reactionAllowlist
iMessage
OpenClaw spawns
imsg rpc
(JSON-RPC over stdio). No daemon or port required.
Copy
channels
imessage
enabled
true
cliPath
&quot;imsg&quot;
dbPath
&quot;~/Library/Messages/chat.db&quot;
remoteHost
&quot;user@gateway-host&quot;
dmPolicy
&quot;pairing&quot;
allowFrom
&quot;+15555550123&quot;
&quot;
[email&#160;protected]
&quot;
&quot;chat_id:123&quot;
historyLimit
includeAttachments
false
mediaMaxMb
service
&quot;auto&quot;
region
&quot;US&quot;
Requires Full Disk Access to the Messages DB.
Prefer
chat_id:&lt;id&gt;
targets. Use
imsg chats --limit 20
to list chats.
cliPath
can point to an SSH wrapper; set
remoteHost
for SCP attachment fetching.
iMessage SSH wrapper example
Copy
#!/usr/bin/env bash
exec
ssh
gateway-host
imsg
&quot;$@&quot;
Multi-account (all channels)
Run multiple accounts per channel (each with its own
accountId
Copy
channels
telegram
accounts
default
name
&quot;Primary bot&quot;
botToken
&quot;123456:ABC...&quot;
alerts
name
&quot;Alerts bot&quot;
botToken
&quot;987654:XYZ...&quot;
default
is used when
accountId
is omitted (CLI + routing).
Env tokens only apply to the
default
account.
Base channel settings apply to all accounts unless overridden per account.
Use
bindings[].match.accountId
to route each account to a different agent.
Group chat mention gating
Group messages default to
require mention
(metadata mention or regex patterns). Applies to WhatsApp, Telegram, Discord, Google Chat, and iMessage group chats.
Mention types:
Metadata mentions
: Native platform @-mentions. Ignored in WhatsApp self-chat mode.
Text patterns
: Regex patterns in
agents.list[].groupChat.mentionPatterns
. Always checked.
Mention gating is enforced only when detection is possible (native mentions or at least one pattern).
Copy
messages
groupChat
historyLimit
50 }
agents
list
&quot;main&quot;
groupChat
mentionPatterns
&quot;@openclaw&quot;
&quot;openclaw&quot;
] } }]
messages.groupChat.historyLimit
sets the global default. Channels can override with
channels.&lt;channel&gt;.historyLimit
(or per-account). Set
to disable.
DM history limits
Copy
channels
telegram
dmHistoryLimit
dms
&quot;123456789&quot;
historyLimit
50 }
Resolution: per-DM override → provider default → no limit (all retained).
Supported:
telegram
whatsapp
discord
slack
signal
imessage
msteams
Self-chat mode
Include your own number in
allowFrom
to enable self-chat mode (ignores native @-mentions, only responds to text patterns):
Copy
channels
whatsapp
allowFrom
&quot;+15555550123&quot;
groups
&quot;*&quot;
requireMention
true
} }
agents
list
&quot;main&quot;
groupChat
mentionPatterns
&quot;reisponde&quot;
&quot;@openclaw&quot;
] }
Commands (chat command handling)
Copy
commands
native
&quot;auto&quot;
// register native commands when supported
text
true
// parse /commands in chat messages
bash
false
// allow ! (alias: /bash)
bashForegroundMs
2000
config
false
// allow /config
debug
false
// allow /debug
restart
false
// allow /restart + gateway restart tool
allowFrom
&quot;*&quot;
&quot;user1&quot;
discord
&quot;user:123&quot;
useAccessGroups
true
Command details
Text commands must be
standalone
messages with leading
native: &quot;auto&quot;
turns on native commands for Discord/Telegram, leaves Slack off.
Override per channel:
channels.discord.commands.native
(bool or
&quot;auto&quot;
false
clears previously registered commands.
channels.telegram.customCommands
adds extra Telegram bot menu entries.
bash: true
enables
! &lt;cmd&gt;
for host shell. Requires
tools.elevated.enabled
and sender in
tools.elevated.allowFrom.&lt;channel&gt;
config: true
enables
/config
(reads/writes
openclaw.json
channels.&lt;provider&gt;.configWrites
gates config mutations per channel (default: true).
allowFrom
is per-provider. When set, it is the
only
authorization source (channel allowlists/pairing and
useAccessGroups
are ignored).
useAccessGroups: false
allows commands to bypass access-group policies when
allowFrom
is not set.
Agent defaults
agents.defaults.workspace
Default:
~/.openclaw/workspace
Copy
agents
defaults
workspace
&quot;~/.openclaw/workspace&quot;
} }
agents.defaults.repoRoot
Optional repository root shown in the system prompt’s Runtime line. If unset, OpenClaw auto-detects by walking upward from the workspace.
Copy
agents
defaults
repoRoot
&quot;~/Projects/openclaw&quot;
} }
agents.defaults.skipBootstrap
Disables automatic creation of workspace bootstrap files (
AGENTS.md
SOUL.md
TOOLS.md
IDENTITY.md
USER.md
HEARTBEAT.md
BOOTSTRAP.md
Copy
agents
defaults
skipBootstrap
true
} }
agents.defaults.bootstrapMaxChars
Max characters per workspace bootstrap file before truncation. Default:
20000
Copy
agents
defaults
bootstrapMaxChars
20000 } }
agents.defaults.bootstrapTotalMaxChars
Max total characters injected across all workspace bootstrap files. Default:
24000
Copy
agents
defaults
bootstrapTotalMaxChars
24000 } }
agents.defaults.userTimezone
Timezone for system prompt context (not message timestamps). Falls back to host timezone.
Copy
agents
defaults
userTimezone
&quot;America/Chicago&quot;
} }
agents.defaults.timeFormat
Time format in system prompt. Default:
auto
(OS preference).
Copy
agents
defaults
timeFormat
&quot;auto&quot;
} }
// auto | 12 | 24
agents.defaults.model
Copy
agents
defaults
models
&quot;anthropic/claude-opus-4-6&quot;
alias
&quot;opus&quot;
&quot;minimax/MiniMax-M2.1&quot;
alias
&quot;minimax&quot;
model
primary
&quot;anthropic/claude-opus-4-6&quot;
fallbacks
&quot;minimax/MiniMax-M2.1&quot;
imageModel
primary
&quot;openrouter/qwen/qwen-2.5-vl-72b-instruct:free&quot;
fallbacks
&quot;openrouter/google/gemini-2.0-flash-vision:free&quot;
thinkingDefault
&quot;low&quot;
verboseDefault
&quot;off&quot;
elevatedDefault
&quot;on&quot;
timeoutSeconds
600
mediaMaxMb
contextTokens
200000
maxConcurrent
model.primary
: format
provider/model
(e.g.
anthropic/claude-opus-4-6
). If you omit the provider, OpenClaw assumes
anthropic
(deprecated).
models
: the configured model catalog and allowlist for
/model
. Each entry can include
alias
(shortcut) and
params
(provider-specific:
temperature
maxTokens
imageModel
: only used if the primary model lacks image input.
maxConcurrent
: max parallel agent runs across sessions (each session still serialized). Default: 1.
Built-in alias shorthands
(only apply when the model is in
agents.defaults.models
Alias
Model
opus
anthropic/claude-opus-4-6
sonnet
anthropic/claude-sonnet-4-5
gpt
openai/gpt-5.2
gpt-mini
openai/gpt-5-mini
gemini
google/gemini-3-pro-preview
gemini-flash
google/gemini-3-flash-preview
Your configured aliases always win over defaults.
Z.AI GLM-4.x models automatically enable thinking mode unless you set
--thinking off
or define
agents.defaults.models[&quot;zai/&lt;model&gt;&quot;].params.thinking
yourself.
agents.defaults.cliBackends
Optional CLI backends for text-only fallback runs (no tool calls). Useful as a backup when API providers fail.
Copy
agents
defaults
cliBackends
&quot;claude-cli&quot;
command
&quot;/opt/homebrew/bin/claude&quot;
&quot;my-cli&quot;
command
&quot;my-cli&quot;
args
&quot;--json&quot;
output
&quot;json&quot;
modelArg
&quot;--model&quot;
sessionArg
&quot;--session&quot;
sessionMode
&quot;existing&quot;
systemPromptArg
&quot;--system&quot;
systemPromptWhen
&quot;first&quot;
imageArg
&quot;--image&quot;
imageMode
&quot;repeat&quot;
CLI backends are text-first; tools are always disabled.
Sessions supported when
sessionArg
is set.
Image pass-through supported when
imageArg
accepts file paths.
agents.defaults.heartbeat
Periodic heartbeat runs.
Copy
agents
defaults
heartbeat
every
&quot;30m&quot;
// 0m disables
model
&quot;openai/gpt-5.2-mini&quot;
includeReasoning
false
session
&quot;main&quot;
&quot;+15555550123&quot;
target
&quot;last&quot;
// last | whatsapp | telegram | discord | ... | none
prompt
&quot;Read HEARTBEAT.md if it exists...&quot;
ackMaxChars
300
every
: duration string (ms/s/m/h). Default:
30m
Per-agent: set
agents.list[].heartbeat
. When any agent defines
heartbeat
only those agents
run heartbeats.
Heartbeats run full agent turns — shorter intervals burn more tokens.
agents.defaults.compaction
Copy
agents
defaults
compaction
mode
&quot;safeguard&quot;
// default | safeguard
reserveTokensFloor
24000
memoryFlush
enabled
true
softThresholdTokens
6000
systemPrompt
&quot;Session nearing compaction. Store durable memories now.&quot;
prompt
&quot;Write any lasting notes to memory/YYYY-MM-DD.md; reply with NO_REPLY if nothing to store.&quot;
mode
default
safeguard
(chunked summarization for long histories). See
Compaction
memoryFlush
: silent agentic turn before auto-compaction to store durable memories. Skipped when workspace is read-only.
agents.defaults.contextPruning
Prunes
old tool results
from in-memory context before sending to the LLM. Does
not
modify session history on disk.
Copy
agents
defaults
contextPruning
mode
&quot;cache-ttl&quot;
// off | cache-ttl
ttl
&quot;1h&quot;
// duration (ms/s/m/h), default unit: minutes
keepLastAssistants
softTrimRatio
0.3
hardClearRatio
0.5
minPrunableToolChars
50000
softTrim
maxChars
4000
headChars
1500
tailChars
1500 }
hardClear
enabled
true
placeholder
&quot;[Old tool result content cleared]&quot;
tools
deny
&quot;browser&quot;
&quot;canvas&quot;
] }
cache-ttl mode behavior
mode: &quot;cache-ttl&quot;
enables pruning passes.
ttl
controls how often pruning can run again (after the last cache touch).
Pruning soft-trims oversized tool results first, then hard-clears older tool results if needed.
Soft-trim
keeps beginning + end and inserts
...
in the middle.
Hard-clear
replaces the entire tool result with the placeholder.
Notes:
Image blocks are never trimmed/cleared.
Ratios are character-based (approximate), not exact token counts.
If fewer than
keepLastAssistants
assistant messages exist, pruning is skipped.
See
Session Pruning
for behavior details.
Block streaming
Copy
agents
defaults
blockStreamingDefault
&quot;off&quot;
// on | off
blockStreamingBreak
&quot;text_end&quot;
// text_end | message_end
blockStreamingChunk
minChars
800
maxChars
1200 }
blockStreamingCoalesce
idleMs
1000 }
humanDelay
mode
&quot;natural&quot;
// off | natural | custom (use minMs/maxMs)
Non-Telegram channels require explicit
*.blockStreaming: true
to enable block replies.
Channel overrides:
channels.&lt;channel&gt;.blockStreamingCoalesce
(and per-account variants). Signal/Slack/Discord/Google Chat default
minChars: 1500
humanDelay
: randomized pause between block replies.
natural
= 800–2500ms. Per-agent override:
agents.list[].humanDelay
See
Streaming
for behavior + chunking details.
Typing indicators
Copy
agents
defaults
typingMode
&quot;instant&quot;
// never | instant | thinking | message
typingIntervalSeconds
Defaults:
instant
for direct chats/mentions,
message
for unmentioned group chats.
Per-session overrides:
session.typingMode
session.typingIntervalSeconds
See
Typing Indicators
agents.defaults.sandbox
Optional
Docker sandboxing
for the embedded agent. See
Sandboxing
for the full guide.
Copy
agents
defaults
sandbox
mode
&quot;non-main&quot;
// off | non-main | all
scope
&quot;agent&quot;
// session | agent | shared
workspaceAccess
&quot;none&quot;
// none | ro | rw
workspaceRoot
&quot;~/.openclaw/sandboxes&quot;
docker
image
&quot;openclaw-sandbox:bookworm-slim&quot;
containerPrefix
&quot;openclaw-sbx-&quot;
workdir
&quot;/workspace&quot;
readOnlyRoot
true
tmpfs
&quot;/tmp&quot;
&quot;/var/tmp&quot;
&quot;/run&quot;
network
&quot;none&quot;
user
&quot;1000:1000&quot;
capDrop
&quot;ALL&quot;
env
LANG
&quot;C.UTF-8&quot;
setupCommand
&quot;apt-get update &amp;&amp; apt-get install -y git curl jq&quot;
pidsLimit
256
memory
&quot;1g&quot;
memorySwap
&quot;2g&quot;
cpus
ulimits
nofile
soft
1024
hard
2048 }
nproc
256
seccompProfile
&quot;/path/to/seccomp.json&quot;
apparmorProfile
&quot;openclaw-sandbox&quot;
dns
&quot;1.1.1.1&quot;
&quot;8.8.8.8&quot;
extraHosts
&quot;internal.service:10.0.0.5&quot;
binds
&quot;/home/user/source:/source:rw&quot;
browser
enabled
false
image
&quot;openclaw-sandbox-browser:bookworm-slim&quot;
cdpPort
9222
vncPort
5900
noVncPort
6080
headless
false
enableNoVnc
true
allowHostControl
false
autoStart
true
autoStartTimeoutMs
12000
prune
idleHours
maxAgeDays
tools
sandbox
tools
allow
&quot;exec&quot;
&quot;process&quot;
&quot;read&quot;
&quot;write&quot;
&quot;edit&quot;
&quot;apply_patch&quot;
&quot;sessions_list&quot;
&quot;sessions_history&quot;
&quot;sessions_send&quot;
&quot;sessions_spawn&quot;
&quot;session_status&quot;
deny
&quot;browser&quot;
&quot;canvas&quot;
&quot;nodes&quot;
&quot;cron&quot;
&quot;discord&quot;
&quot;gateway&quot;
Sandbox details
Workspace access:
none
: per-scope sandbox workspace under
~/.openclaw/sandboxes
: sandbox workspace at
/workspace
, agent workspace mounted read-only at
/agent
: agent workspace mounted read/write at
/workspace
Scope:
session
: per-session container + workspace
agent
: one container + workspace per agent (default)
shared
: shared container and workspace (no cross-session isolation)
setupCommand
runs once after container creation (via
sh -lc
). Needs network egress, writable root, root user.
Containers default to
network: &quot;none&quot;
— set to
&quot;bridge&quot;
if the agent needs outbound access.
Inbound attachments
are staged into
media/inbound/*
in the active workspace.
docker.binds
mounts additional host directories; global and per-agent binds are merged.
Sandboxed browser
sandbox.browser.enabled
): Chromium + CDP in a container. noVNC URL injected into system prompt. Does not require
browser.enabled
in main config.
allowHostControl: false
(default) blocks sandboxed sessions from targeting the host browser.
sandbox.browser.binds
mounts additional host directories into the sandbox browser container only. When set (including
), it replaces
docker.binds
for the browser container.
Build images:
Copy
scripts/sandbox-setup.sh
# main sandbox image
scripts/sandbox-browser-setup.sh
# optional browser image
agents.list
(per-agent overrides)
Copy
agents
list
&quot;main&quot;
default
true
name
&quot;Main Agent&quot;
workspace
&quot;~/.openclaw/workspace&quot;
agentDir
&quot;~/.openclaw/agents/main/agent&quot;
model
&quot;anthropic/claude-opus-4-6&quot;
// or { primary, fallbacks }
identity
name
&quot;Samantha&quot;
theme
&quot;helpful sloth&quot;
emoji
&quot;🦥&quot;
avatar
&quot;avatars/samantha.png&quot;
groupChat
mentionPatterns
&quot;@openclaw&quot;
] }
sandbox
mode
&quot;off&quot;
subagents
allowAgents
&quot;*&quot;
] }
tools
profile
&quot;coding&quot;
allow
&quot;browser&quot;
deny
&quot;canvas&quot;
elevated
enabled
true
: stable agent id (required).
default
: when multiple are set, first wins (warning logged). If none set, first list entry is default.
model
: string form overrides
primary
only; object form
{ primary, fallbacks }
overrides both (
disables global fallbacks).
identity.avatar
: workspace-relative path,
http(s)
URL, or
data:
URI.
identity
derives defaults:
ackReaction
from
emoji
mentionPatterns
from
name
emoji
subagents.allowAgents
: allowlist of agent ids for
sessions_spawn
[&quot;*&quot;]
= any; default: same agent only).
Multi-agent routing
Run multiple isolated agents inside one Gateway. See
Multi-Agent
Copy
agents
list
&quot;home&quot;
default
true
workspace
&quot;~/.openclaw/workspace-home&quot;
&quot;work&quot;
workspace
&quot;~/.openclaw/workspace-work&quot;
bindings
agentId
&quot;home&quot;
match
channel
&quot;whatsapp&quot;
accountId
&quot;personal&quot;
} }
agentId
&quot;work&quot;
match
channel
&quot;whatsapp&quot;
accountId
&quot;biz&quot;
} }
Binding match fields
match.channel
(required)
match.accountId
(optional;
= any account; omitted = default account)
match.peer
(optional;
{ kind: direct|group|channel, id }
match.guildId
match.teamId
(optional; channel-specific)
Deterministic match order:
match.peer
match.guildId
match.teamId
match.accountId
(exact, no peer/guild/team)
match.accountId: &quot;*&quot;
(channel-wide)
Default agent
Within each tier, the first matching
bindings
entry wins.
Per-agent access profiles
Full access (no sandbox)
Copy
agents
list
&quot;personal&quot;
workspace
&quot;~/.openclaw/workspace-personal&quot;
sandbox
mode
&quot;off&quot;
Read-only tools + workspace
Copy
agents
list
&quot;family&quot;
workspace
&quot;~/.openclaw/workspace-family&quot;
sandbox
mode
&quot;all&quot;
scope
&quot;agent&quot;
workspaceAccess
&quot;ro&quot;
tools
allow
&quot;read&quot;
&quot;sessions_list&quot;
&quot;sessions_history&quot;
&quot;sessions_send&quot;
&quot;sessions_spawn&quot;
&quot;session_status&quot;
deny
&quot;write&quot;
&quot;edit&quot;
&quot;apply_patch&quot;
&quot;exec&quot;
&quot;process&quot;
&quot;browser&quot;
No filesystem access (messaging only)
Copy
agents
list
&quot;public&quot;
workspace
&quot;~/.openclaw/workspace-public&quot;
sandbox
mode
&quot;all&quot;
scope
&quot;agent&quot;
workspaceAccess
&quot;none&quot;
tools
allow
&quot;sessions_list&quot;
&quot;sessions_history&quot;
&quot;sessions_send&quot;
&quot;sessions_spawn&quot;
&quot;session_status&quot;
&quot;whatsapp&quot;
&quot;telegram&quot;
&quot;slack&quot;
&quot;discord&quot;
&quot;gateway&quot;
deny
&quot;read&quot;
&quot;write&quot;
&quot;edit&quot;
&quot;apply_patch&quot;
&quot;exec&quot;
&quot;process&quot;
&quot;browser&quot;
&quot;canvas&quot;
&quot;nodes&quot;
&quot;cron&quot;
&quot;gateway&quot;
&quot;image&quot;
See
Multi-Agent Sandbox &amp; Tools
for precedence details.
Session
Copy
session
scope
&quot;per-sender&quot;
dmScope
&quot;main&quot;
// main | per-peer | per-channel-peer | per-account-channel-peer
identityLinks
alice
&quot;telegram:123456789&quot;
&quot;discord:987654321012345678&quot;
reset
mode
&quot;daily&quot;
// daily | idle
atHour
idleMinutes
resetByType
thread
mode
&quot;daily&quot;
atHour
4 }
direct
mode
&quot;idle&quot;
idleMinutes
240 }
group
mode
&quot;idle&quot;
idleMinutes
120 }
resetTriggers
&quot;/new&quot;
&quot;/reset&quot;
store
&quot;~/.openclaw/agents/{agentId}/sessions/sessions.json&quot;
maintenance
mode
&quot;warn&quot;
// warn | enforce
pruneAfter
&quot;30d&quot;
maxEntries
500
rotateBytes
&quot;10mb&quot;
mainKey
&quot;main&quot;
// legacy (runtime always uses &quot;main&quot;)
agentToAgent
maxPingPongTurns
5 }
sendPolicy
rules
action
&quot;deny&quot;
match
channel
&quot;discord&quot;
chatType
&quot;group&quot;
} }]
default
&quot;allow&quot;
Session field details
dmScope
: how DMs are grouped.
main
: all DMs share the main session.
per-peer
: isolate by sender id across channels.
per-channel-peer
: isolate per channel + sender (recommended for multi-user inboxes).
per-account-channel-peer
: isolate per account + channel + sender (recommended for multi-account).
identityLinks
: map canonical ids to provider-prefixed peers for cross-channel session sharing.
reset
: primary reset policy.
daily
resets at
atHour
local time;
idle
resets after
idleMinutes
. When both configured, whichever expires first wins.
resetByType
: per-type overrides (
direct
group
thread
). Legacy
accepted as alias for
direct
mainKey
: legacy field. Runtime now always uses
&quot;main&quot;
for the main direct-chat bucket.
sendPolicy
: match by
channel
chatType
direct|group|channel
, with legacy
alias),
keyPrefix
, or
rawKeyPrefix
. First deny wins.
maintenance
warn
warns the active session on eviction;
enforce
applies pruning and rotation.
Messages
Copy
messages
responsePrefix
&quot;🦞&quot;
// or &quot;auto&quot;
ackReaction
&quot;👀&quot;
ackReactionScope
&quot;group-mentions&quot;
// group-mentions | group-all | direct | all
removeAckAfterReply
false
queue
mode
&quot;collect&quot;
// steer | followup | collect | steer-backlog | steer+backlog | queue | interrupt
debounceMs
1000
cap
drop
&quot;summarize&quot;
// old | new | summarize
byChannel
whatsapp
&quot;collect&quot;
telegram
&quot;collect&quot;
inbound
debounceMs
2000
// 0 disables
byChannel
whatsapp
5000
slack
1500
Response prefix
Per-channel/account overrides:
channels.&lt;channel&gt;.responsePrefix
channels.&lt;channel&gt;.accounts.&lt;id&gt;.responsePrefix
Resolution (most specific wins): account → channel → global.
&quot;&quot;
disables and stops cascade.
&quot;auto&quot;
derives
[{identity.name}]
Template variables:
Variable
Description
Example
{model}
Short model name
claude-opus-4-6
{modelFull}
Full model identifier
anthropic/claude-opus-4-6
{provider}
Provider name
anthropic
{thinkingLevel}
Current thinking level
high
low
off
{identity.name}
Agent identity name
(same as
&quot;auto&quot;
Variables are case-insensitive.
{think}
is an alias for
{thinkingLevel}
Ack reaction
Defaults to active agent’s
identity.emoji
, otherwise
&quot;👀&quot;
. Set
&quot;&quot;
to disable.
Per-channel overrides:
channels.&lt;channel&gt;.ackReaction
channels.&lt;channel&gt;.accounts.&lt;id&gt;.ackReaction
Resolution order: account → channel →
messages.ackReaction
→ identity fallback.
Scope:
group-mentions
(default),
group-all
direct
all
removeAckAfterReply
: removes ack after reply (Slack/Discord/Telegram/Google Chat only).
Inbound debounce
Batches rapid text-only messages from the same sender into a single agent turn. Media/attachments flush immediately. Control commands bypass debouncing.
TTS (text-to-speech)
Copy
messages
tts
auto
&quot;always&quot;
// off | always | inbound | tagged
mode
&quot;final&quot;
// final | all
provider
&quot;elevenlabs&quot;
summaryModel
&quot;openai/gpt-4.1-mini&quot;
modelOverrides
enabled
true
maxTextLength
4000
timeoutMs
30000
prefsPath
&quot;~/.openclaw/settings/tts.json&quot;
elevenlabs
apiKey
&quot;elevenlabs_api_key&quot;
baseUrl
&quot;https://api.elevenlabs.io&quot;
voiceId
&quot;voice_id&quot;
modelId
&quot;eleven_multilingual_v2&quot;
seed
applyTextNormalization
&quot;auto&quot;
languageCode
&quot;en&quot;
voiceSettings
stability
0.5
similarityBoost
0.75
style
0.0
useSpeakerBoost
true
speed
1.0
openai
apiKey
&quot;openai_api_key&quot;
model
&quot;gpt-4o-mini-tts&quot;
voice
&quot;alloy&quot;
auto
controls auto-TTS.
/tts off|always|inbound|tagged
overrides per session.
summaryModel
overrides
agents.defaults.model.primary
for auto-summary.
API keys fall back to
ELEVENLABS_API_KEY
XI_API_KEY
and
OPENAI_API_KEY
Talk
Defaults for Talk mode (macOS/iOS/Android).
Copy
talk
voiceId
&quot;elevenlabs_voice_id&quot;
voiceAliases
Clawd
&quot;EXAVITQu4vr4xnSDxMaL&quot;
Roger
&quot;CwhRBWXzGAHq8TQ4Fs17&quot;
modelId
&quot;eleven_v3&quot;
outputFormat
&quot;mp3_44100_128&quot;
apiKey
&quot;elevenlabs_api_key&quot;
interruptOnSpeech
true
Voice IDs fall back to
ELEVENLABS_VOICE_ID
SAG_VOICE_ID
apiKey
falls back to
ELEVENLABS_API_KEY
voiceAliases
lets Talk directives use friendly names.
Tools
Tool profiles
tools.profile
sets a base allowlist before
tools.allow
tools.deny
Profile
Includes
minimal
session_status
only
coding
group:fs
group:runtime
group:sessions
group:memory
image
messaging
group:messaging
sessions_list
sessions_history
sessions_send
session_status
full
No restriction (same as unset)
Tool groups
Group
Tools
group:runtime
exec
process
bash
is accepted as an alias for
exec
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
group:web
web_search
web_fetch
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
All built-in tools (excludes provider plugins)
tools.allow
tools.deny
Global tool allow/deny policy (deny wins). Case-insensitive, supports
wildcards. Applied even when Docker sandbox is off.
Copy
tools
deny
&quot;browser&quot;
&quot;canvas&quot;
] }
tools.byProvider
Further restrict tools for specific providers or models. Order: base profile → provider profile → allow/deny.
Copy
tools
profile
&quot;coding&quot;
byProvider
&quot;google-antigravity&quot;
profile
&quot;minimal&quot;
&quot;openai/gpt-5.2&quot;
allow
&quot;group:fs&quot;
&quot;sessions_list&quot;
] }
tools.elevated
Controls elevated (host) exec access:
Copy
tools
elevated
enabled
true
allowFrom
whatsapp
&quot;+15555550123&quot;
discord
&quot;steipete&quot;
&quot;1234567890123&quot;
Per-agent override (
agents.list[].tools.elevated
) can only further restrict.
/elevated on|off|ask|full
stores state per session; inline directives apply to single message.
Elevated
exec
runs on the host, bypasses sandboxing.
tools.exec
Copy
tools
exec
backgroundMs
10000
timeoutSec
1800
cleanupMs
1800000
notifyOnExit
true
notifyOnExitEmptySuccess
false
applyPatch
enabled
false
allowModels
&quot;gpt-5.2&quot;
tools.web
Copy
tools
web
search
enabled
true
apiKey
&quot;brave_api_key&quot;
// or BRAVE_API_KEY env
maxResults
timeoutSeconds
cacheTtlMinutes
fetch
enabled
true
maxChars
50000
maxCharsCap
50000
timeoutSeconds
cacheTtlMinutes
userAgent
&quot;custom-ua&quot;
tools.media
Configures inbound media understanding (image/audio/video):
Copy
tools
media
concurrency
audio
enabled
true
maxBytes
20971520
scope
default
&quot;deny&quot;
rules
action
&quot;allow&quot;
match
chatType
&quot;direct&quot;
} }]
models
provider
&quot;openai&quot;
model
&quot;gpt-4o-mini-transcribe&quot;
type
&quot;cli&quot;
command
&quot;whisper&quot;
args
&quot;--model&quot;
&quot;base&quot;
&quot;{{MediaPath}}&quot;
] }
video
enabled
true
maxBytes
52428800
models
provider
&quot;google&quot;
model
&quot;gemini-3-flash-preview&quot;
Media model entry fields
Provider entry
type: &quot;provider&quot;
or omitted):
provider
: API provider id (
openai
anthropic
google
gemini
groq
, etc.)
model
: model id override
profile
preferredProfile
: auth profile selection
CLI entry
type: &quot;cli&quot;
command
: executable to run
args
: templated args (supports
{{MediaPath}}
{{Prompt}}
{{MaxChars}}
, etc.)
Common fields:
capabilities
: optional list (
image
audio
video
). Defaults:
openai
anthropic
minimax
→ image,
google
→ image+audio+video,
groq
→ audio.
prompt
maxChars
maxBytes
timeoutSeconds
language
: per-entry overrides.
Failures fall back to the next entry.
Provider auth follows standard order: auth profiles → env vars →
models.providers.*.apiKey
tools.agentToAgent
Copy
tools
agentToAgent
enabled
false
allow
&quot;home&quot;
&quot;work&quot;
tools.sessions
Controls which sessions can be targeted by the session tools (
sessions_list
sessions_history
sessions_send
Default:
tree
(current session + sessions spawned by it, such as subagents).
Copy
tools
sessions
// &quot;self&quot; | &quot;tree&quot; | &quot;agent&quot; | &quot;all&quot;
visibility
&quot;tree&quot;
Notes:
self
: only the current session key.
tree
: current session + sessions spawned by the current session (subagents).
agent
: any session belonging to the current agent id (can include other users if you run per-sender sessions under the same agent id).
all
: any session. Cross-agent targeting still requires
tools.agentToAgent
Sandbox clamp: when the current session is sandboxed and
agents.defaults.sandbox.sessionToolsVisibility=&quot;spawned&quot;
, visibility is forced to
tree
even if
tools.sessions.visibility=&quot;all&quot;
tools.subagents
Copy
agents
defaults
subagents
model
&quot;minimax/MiniMax-M2.1&quot;
maxConcurrent
archiveAfterMinutes
model
: default model for spawned sub-agents. If omitted, sub-agents inherit the caller’s model.
Per-subagent tool policy:
tools.subagents.tools.allow
tools.subagents.tools.deny
Custom providers and base URLs
OpenClaw uses the pi-coding-agent model catalog. Add custom providers via
models.providers
in config or
~/.openclaw/agents/&lt;agentId&gt;/agent/models.json
Copy
models
mode
&quot;merge&quot;
// merge (default) | replace
providers
&quot;custom-proxy&quot;
baseUrl
&quot;http://localhost:4000/v1&quot;
apiKey
&quot;LITELLM_KEY&quot;
api
&quot;openai-completions&quot;
// openai-completions | openai-responses | anthropic-messages | google-generative-ai
models
&quot;llama-3.1-8b&quot;
name
&quot;Llama 3.1 8B&quot;
reasoning
false
input
&quot;text&quot;
cost
input
output
cacheRead
cacheWrite
0 }
contextWindow
128000
maxTokens
32000
Use
authHeader: true
headers
for custom auth needs.
Override agent config root with
OPENCLAW_AGENT_DIR
(or
PI_CODING_AGENT_DIR
Provider examples
Cerebras (GLM 4.6 / 4.7)
Copy
env
CEREBRAS_API_KEY
&quot;sk-...&quot;
agents
defaults
model
primary
&quot;cerebras/zai-glm-4.7&quot;
fallbacks
&quot;cerebras/zai-glm-4.6&quot;
models
&quot;cerebras/zai-glm-4.7&quot;
alias
&quot;GLM 4.7 (Cerebras)&quot;
&quot;cerebras/zai-glm-4.6&quot;
alias
&quot;GLM 4.6 (Cerebras)&quot;
models
mode
&quot;merge&quot;
providers
cerebras
baseUrl
&quot;https://api.cerebras.ai/v1&quot;
apiKey
&quot;${CEREBRAS_API_KEY}&quot;
api
&quot;openai-completions&quot;
models
&quot;zai-glm-4.7&quot;
name
&quot;GLM 4.7 (Cerebras)&quot;
&quot;zai-glm-4.6&quot;
name
&quot;GLM 4.6 (Cerebras)&quot;
Use
cerebras/zai-glm-4.7
for Cerebras;
zai/glm-4.7
for Z.AI direct.
OpenCode Zen
Copy
agents
defaults
model
primary
&quot;opencode/claude-opus-4-6&quot;
models
&quot;opencode/claude-opus-4-6&quot;
alias
&quot;Opus&quot;
} }
Set
OPENCODE_API_KEY
(or
OPENCODE_ZEN_API_KEY
). Shortcut:
openclaw onboard --auth-choice opencode-zen
Z.AI (GLM-4.7)
Copy
agents
defaults
model
primary
&quot;zai/glm-4.7&quot;
models
&quot;zai/glm-4.7&quot;
{} }
Set
ZAI_API_KEY
z.ai/*
and
z-ai/*
are accepted aliases. Shortcut:
openclaw onboard --auth-choice zai-api-key
General endpoint:
https://api.z.ai/api/paas/v4
Coding endpoint (default):
https://api.z.ai/api/coding/paas/v4
For the general endpoint, define a custom provider with the base URL override.
Moonshot AI (Kimi)
Copy
env
MOONSHOT_API_KEY
&quot;sk-...&quot;
agents
defaults
model
primary
&quot;moonshot/kimi-k2.5&quot;
models
&quot;moonshot/kimi-k2.5&quot;
alias
&quot;Kimi K2.5&quot;
} }
models
mode
&quot;merge&quot;
providers
moonshot
baseUrl
&quot;https://api.moonshot.ai/v1&quot;
apiKey
&quot;${MOONSHOT_API_KEY}&quot;
api
&quot;openai-completions&quot;
models
&quot;kimi-k2.5&quot;
name
&quot;Kimi K2.5&quot;
reasoning
false
input
&quot;text&quot;
cost
input
output
cacheRead
cacheWrite
0 }
contextWindow
256000
maxTokens
8192
For the China endpoint:
baseUrl: &quot;https://api.moonshot.cn/v1&quot;
openclaw onboard --auth-choice moonshot-api-key-cn
Kimi Coding
Copy
env
KIMI_API_KEY
&quot;sk-...&quot;
agents
defaults
model
primary
&quot;kimi-coding/k2p5&quot;
models
&quot;kimi-coding/k2p5&quot;
alias
&quot;Kimi K2.5&quot;
} }
Anthropic-compatible, built-in provider. Shortcut:
openclaw onboard --auth-choice kimi-code-api-key
Synthetic (Anthropic-compatible)
Copy
env
SYNTHETIC_API_KEY
&quot;sk-...&quot;
agents
defaults
model
primary
&quot;synthetic/hf:MiniMaxAI/MiniMax-M2.1&quot;
models
&quot;synthetic/hf:MiniMaxAI/MiniMax-M2.1&quot;
alias
&quot;MiniMax M2.1&quot;
} }
models
mode
&quot;merge&quot;
providers
synthetic
baseUrl
&quot;https://api.synthetic.new/anthropic&quot;
apiKey
&quot;${SYNTHETIC_API_KEY}&quot;
api
&quot;anthropic-messages&quot;
models
&quot;hf:MiniMaxAI/MiniMax-M2.1&quot;
name
&quot;MiniMax M2.1&quot;
reasoning
false
input
&quot;text&quot;
cost
input
output
cacheRead
cacheWrite
0 }
contextWindow
192000
maxTokens
65536
Base URL should omit
/v1
(Anthropic client appends it). Shortcut:
openclaw onboard --auth-choice synthetic-api-key
MiniMax M2.1 (direct)
Copy
agents
defaults
model
primary
&quot;minimax/MiniMax-M2.1&quot;
models
&quot;minimax/MiniMax-M2.1&quot;
alias
&quot;Minimax&quot;
models
mode
&quot;merge&quot;
providers
minimax
baseUrl
&quot;https://api.minimax.io/anthropic&quot;
apiKey
&quot;${MINIMAX_API_KEY}&quot;
api
&quot;anthropic-messages&quot;
models
&quot;MiniMax-M2.1&quot;
name
&quot;MiniMax M2.1&quot;
reasoning
false
input
&quot;text&quot;
cost
input
output
cacheRead
cacheWrite
10 }
contextWindow
200000
maxTokens
8192
Set
MINIMAX_API_KEY
. Shortcut:
openclaw onboard --auth-choice minimax-api
Local models (LM Studio)
See
Local Models
. TL;DR: run MiniMax M2.1 via LM Studio Responses API on serious hardware; keep hosted models merged for fallback.
Skills
Copy
skills
allowBundled
&quot;gemini&quot;
&quot;peekaboo&quot;
load
extraDirs
&quot;~/Projects/agent-scripts/skills&quot;
install
preferBrew
true
nodeManager
&quot;npm&quot;
// npm | pnpm | yarn
entries
&quot;nano-banana-pro&quot;
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
allowBundled
: optional allowlist for bundled skills only (managed/workspace skills unaffected).
entries.&lt;skillKey&gt;.enabled: false
disables a skill even if bundled/installed.
entries.&lt;skillKey&gt;.apiKey
: convenience for skills declaring a primary env var.
Plugins
Copy
plugins
enabled
true
allow
&quot;voice-call&quot;
deny
load
paths
&quot;~/Projects/oss/voice-call-extension&quot;
entries
&quot;voice-call&quot;
enabled
true
config
provider
&quot;twilio&quot;
Loaded from
~/.openclaw/extensions
&lt;workspace&gt;/.openclaw/extensions
, plus
plugins.load.paths
Config changes require a gateway restart.
allow
: optional allowlist (only listed plugins load).
deny
wins.
See
Plugins
Browser
Copy
browser
enabled
true
evaluateEnabled
true
defaultProfile
&quot;chrome&quot;
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
color
&quot;#FF4500&quot;
// headless: false,
// noSandbox: false,
// executablePath: &quot;/Applications/Brave Browser.app/Contents/MacOS/Brave Browser&quot;,
// attachOnly: false,
evaluateEnabled: false
disables
act:evaluate
and
wait --fn
Remote profiles are attach-only (start/stop/reset disabled).
Auto-detect order: default browser if Chromium-based → Chrome → Brave → Edge → Chromium → Chrome Canary.
Control service: loopback only (port derived from
gateway.port
, default
18791
Copy
seamColor
&quot;#FF4500&quot;
assistant
name
&quot;OpenClaw&quot;
avatar
&quot;CB&quot;
// emoji, short text, image URL, or data URI
seamColor
: accent color for native app UI chrome (Talk Mode bubble tint, etc.).
assistant
: Control UI identity override. Falls back to active agent identity.
Gateway
Copy
gateway
mode
&quot;local&quot;
// local | remote
port
18789
bind
&quot;loopback&quot;
auth
mode
&quot;token&quot;
// token | password | trusted-proxy
token
&quot;your-token&quot;
// password: &quot;your-password&quot;,
// or OPENCLAW_GATEWAY_PASSWORD
// trustedProxy: { userHeader: &quot;x-forwarded-user&quot; },
// for mode=trusted-proxy; see /gateway/trusted-proxy-auth
allowTailscale
true
rateLimit
maxAttempts
windowMs
60000
lockoutMs
300000
exemptLoopback
true
tailscale
mode
&quot;off&quot;
// off | serve | funnel
resetOnExit
false
controlUi
enabled
true
basePath
&quot;/openclaw&quot;
// root: &quot;dist/control-ui&quot;,
// allowInsecureAuth: false,
// dangerouslyDisableDeviceAuth: false,
remote
url
&quot;ws://gateway.tailnet:18789&quot;
transport
&quot;ssh&quot;
// ssh | direct
token
&quot;your-token&quot;
// password: &quot;your-password&quot;,
trustedProxies
&quot;10.0.0.1&quot;
tools
// Additional /tools/invoke HTTP denies
deny
&quot;browser&quot;
// Remove tools from the default HTTP deny list
allow
&quot;gateway&quot;
Gateway field details
mode
local
(run gateway) or
remote
(connect to remote gateway). Gateway refuses to start unless
local
port
: single multiplexed port for WS + HTTP. Precedence:
--port
&gt;
OPENCLAW_GATEWAY_PORT
&gt;
gateway.port
&gt;
18789
bind
auto
loopback
(default),
lan
0.0.0.0
tailnet
(Tailscale IP only), or
custom
Auth
: required by default. Non-loopback binds require a shared token/password. Onboarding wizard generates a token by default.
auth.mode: &quot;trusted-proxy&quot;
: delegate auth to an identity-aware reverse proxy and trust identity headers from
gateway.trustedProxies
(see
Trusted Proxy Auth
auth.allowTailscale
: when
true
, Tailscale Serve identity headers satisfy auth (verified via
tailscale whois
). Defaults to
true
when
tailscale.mode = &quot;serve&quot;
auth.rateLimit
: optional failed-auth limiter. Applies per client IP and per auth scope (shared-secret and device-token are tracked independently). Blocked attempts return
429
Retry-After
auth.rateLimit.exemptLoopback
defaults to
true
; set
false
when you intentionally want localhost traffic rate-limited too (for test setups or strict proxy deployments).
tailscale.mode
serve
(tailnet only, loopback bind) or
funnel
(public, requires auth).
remote.transport
ssh
(default) or
direct
(ws/wss). For
direct
remote.url
must be
ws://
wss://
gateway.remote.token
is for remote CLI calls only; does not enable local gateway auth.
trustedProxies
: reverse proxy IPs that terminate TLS. Only list proxies you control.
gateway.tools.deny
: extra tool names blocked for HTTP
POST /tools/invoke
(extends default deny list).
gateway.tools.allow
: remove tool names from the default HTTP deny list.
OpenAI-compatible endpoints
Chat Completions: disabled by default. Enable with
gateway.http.endpoints.chatCompletions.enabled: true
Responses API:
gateway.http.endpoints.responses.enabled
Responses URL-input hardening:
gateway.http.endpoints.responses.maxUrlParts
gateway.http.endpoints.responses.files.urlAllowlist
gateway.http.endpoints.responses.images.urlAllowlist
Multi-instance isolation
Run multiple gateways on one host with unique ports and state dirs:
Copy
OPENCLAW_CONFIG_PATH
~/.openclaw/a.json
OPENCLAW_STATE_DIR=~/.openclaw-a \
openclaw
gateway
--port
19001
Convenience flags:
--dev
(uses
~/.openclaw-dev
+ port
19001
--profile &lt;name&gt;
(uses
~/.openclaw-&lt;name&gt;
See
Multiple Gateways
Hooks
Copy
hooks
enabled
true
token
&quot;shared-secret&quot;
path
&quot;/hooks&quot;
maxBodyBytes
262144
defaultSessionKey
&quot;hook:ingress&quot;
allowRequestSessionKey
false
allowedSessionKeyPrefixes
&quot;hook:&quot;
allowedAgentIds
&quot;hooks&quot;
&quot;main&quot;
presets
&quot;gmail&quot;
transformsDir
&quot;~/.openclaw/hooks/transforms&quot;
mappings
match
path
&quot;gmail&quot;
action
&quot;agent&quot;
agentId
&quot;hooks&quot;
wakeMode
&quot;now&quot;
name
&quot;Gmail&quot;
sessionKey
&quot;hook:gmail:{{messages[0].id}}&quot;
messageTemplate
&quot;From: {{messages[0].from}}\nSubject: {{messages[0].subject}}\n{{messages[0].snippet}}&quot;
deliver
true
channel
&quot;last&quot;
model
&quot;openai/gpt-5.2-mini&quot;
Auth:
Authorization: Bearer &lt;token&gt;
x-openclaw-token: &lt;token&gt;
Endpoints:
POST /hooks/wake
{ text, mode?: &quot;now&quot;|&quot;next-heartbeat&quot; }
POST /hooks/agent
{ message, name?, agentId?, sessionKey?, wakeMode?, deliver?, channel?, to?, model?, thinking?, timeoutSeconds? }
sessionKey
from request payload is accepted only when
hooks.allowRequestSessionKey=true
(default:
false
POST /hooks/&lt;name&gt;
→ resolved via
hooks.mappings
Mapping details
match.path
matches sub-path after
/hooks
(e.g.
/hooks/gmail
gmail
match.source
matches a payload field for generic paths.
Templates like
{{messages[0].subject}}
read from the payload.
transform
can point to a JS/TS module returning a hook action.
transform.module
must be a relative path and stays within
hooks.transformsDir
(absolute paths and traversal are rejected).
agentId
routes to a specific agent; unknown IDs fall back to default.
allowedAgentIds
: restricts explicit routing (
or omitted = allow all,
= deny all).
defaultSessionKey
: optional fixed session key for hook agent runs without explicit
sessionKey
allowRequestSessionKey
: allow
/hooks/agent
callers to set
sessionKey
(default:
false
allowedSessionKeyPrefixes
: optional prefix allowlist for explicit
sessionKey
values (request + mapping), e.g.
[&quot;hook:&quot;]
deliver: true
sends final reply to a channel;
channel
defaults to
last
model
overrides LLM for this hook run (must be allowed if model catalog is set).
Gmail integration
Copy
hooks
gmail
account
&quot;
[email&#160;protected]
&quot;
topic
&quot;projects/&lt;project-id&gt;/topics/gog-gmail-watch&quot;
subscription
&quot;gog-gmail-watch-push&quot;
pushToken
&quot;shared-push-token&quot;
hookUrl
&quot;http://127.0.0.1:18789/hooks/gmail&quot;
includeBody
true
maxBytes
20000
renewEveryMinutes
720
serve
bind
&quot;127.0.0.1&quot;
port
8788
path
&quot;/&quot;
tailscale
mode
&quot;funnel&quot;
path
&quot;/gmail-pubsub&quot;
model
&quot;openrouter/meta-llama/llama-3.3-70b-instruct:free&quot;
thinking
&quot;off&quot;
Gateway auto-starts
gog gmail watch serve
on boot when configured. Set
OPENCLAW_SKIP_GMAIL_WATCHER=1
to disable.
Don’t run a separate
gog gmail watch serve
alongside the Gateway.
Canvas host
Copy
canvasHost
root
&quot;~/.openclaw/workspace/canvas&quot;
liveReload
true
// enabled: false,
// or OPENCLAW_SKIP_CANVAS_HOST=1
Serves agent-editable HTML/CSS/JS and A2UI over HTTP under the Gateway port:
http://&lt;gateway-host&gt;:&lt;gateway.port&gt;/__openclaw__/canvas/
http://&lt;gateway-host&gt;:&lt;gateway.port&gt;/__openclaw__/a2ui/
Local-only: keep
gateway.bind: &quot;loopback&quot;
(default).
Non-loopback binds: canvas routes require Gateway auth (token/password/trusted-proxy), same as other Gateway HTTP surfaces.
Node WebViews typically don’t send auth headers; after a node is paired and connected, the Gateway allows a private-IP fallback so the node can load canvas/A2UI without leaking secrets into URLs.
Injects live-reload client into served HTML.
Auto-creates starter
index.html
when empty.
Also serves A2UI at
/__openclaw__/a2ui/
Changes require a gateway restart.
Disable live reload for large directories or
EMFILE
errors.
Discovery
mDNS (Bonjour)
Copy
discovery
mdns
mode
&quot;minimal&quot;
// minimal | full | off
minimal
(default): omit
cliPath
sshPort
from TXT records.
full
: include
cliPath
sshPort
Hostname defaults to
openclaw
. Override with
OPENCLAW_MDNS_HOSTNAME
Wide-area (DNS-SD)
Copy
discovery
wideArea
enabled
true
Writes a unicast DNS-SD zone under
~/.openclaw/dns/
. For cross-network discovery, pair with a DNS server (CoreDNS recommended) + Tailscale split DNS.
Setup:
openclaw dns setup --apply
Environment
env
(inline env vars)
Copy
env
OPENROUTER_API_KEY
&quot;sk-or-...&quot;
vars
GROQ_API_KEY
&quot;gsk-...&quot;
shellEnv
enabled
true
timeoutMs
15000
Inline env vars are only applied if the process env is missing the key.
.env
files: CWD
.env
~/.openclaw/.env
(neither overrides existing vars).
shellEnv
: imports missing expected keys from your login shell profile.
See
Environment
for full precedence.
Env var substitution
Reference env vars in any config string with
${VAR_NAME}
Copy
gateway
auth
token
&quot;${OPENCLAW_GATEWAY_TOKEN}&quot;
Only uppercase names matched:
[A-Z_][A-Z0-9_]*
Missing/empty vars throw an error at config load.
Escape with
$${VAR}
for a literal
${VAR}
Works with
$include
Auth storage
Copy
auth
profiles
&quot;anthropic:
[email&#160;protected]
&quot;
provider
&quot;anthropic&quot;
mode
&quot;oauth&quot;
email
&quot;
[email&#160;protected]
&quot;
&quot;anthropic:work&quot;
provider
&quot;anthropic&quot;
mode
&quot;api_key&quot;
order
anthropic
&quot;anthropic:
[email&#160;protected]
&quot;
&quot;anthropic:work&quot;
Per-agent auth profiles stored at
&lt;agentDir&gt;/auth-profiles.json
Legacy OAuth imports from
~/.openclaw/credentials/oauth.json
See
OAuth
Logging
Copy
logging
level
&quot;info&quot;
file
&quot;/tmp/openclaw/openclaw.log&quot;
consoleLevel
&quot;info&quot;
consoleStyle
&quot;pretty&quot;
// pretty | compact | json
redactSensitive
&quot;tools&quot;
// off | tools
redactPatterns
&quot;\\bTOKEN\\b\\s*[=:]\\s*([\&quot;&#x27;]?)([^\\s\&quot;&#x27;]+)\\1&quot;
Default log file:
/tmp/openclaw/openclaw-YYYY-MM-DD.log
Set
logging.file
for a stable path.
consoleLevel
bumps to
debug
when
--verbose
Wizard
Metadata written by CLI wizards (
onboard
configure
doctor
Copy
wizard
lastRunAt
&quot;2026-01-01T00:00:00.000Z&quot;
lastRunVersion
&quot;2026.1.4&quot;
lastRunCommit
&quot;abc1234&quot;
lastRunCommand
&quot;configure&quot;
lastRunMode
&quot;local&quot;
Identity
Copy
agents
list
&quot;main&quot;
identity
name
&quot;Samantha&quot;
theme
&quot;helpful sloth&quot;
emoji
&quot;🦥&quot;
avatar
&quot;avatars/samantha.png&quot;
Written by the macOS onboarding assistant. Derives defaults:
messages.ackReaction
from
identity.emoji
(falls back to 👀)
mentionPatterns
from
identity.name
identity.emoji
avatar
accepts: workspace-relative path,
http(s)
URL, or
data:
URI
Bridge (legacy, removed)
Current builds no longer include the TCP bridge. Nodes connect over the Gateway WebSocket.
bridge.*
keys are no longer part of the config schema (validation fails until removed;
openclaw doctor --fix
can strip unknown keys).
Legacy bridge config (historical reference)
Copy
&quot;bridge&quot;
&quot;enabled&quot;
true
&quot;port&quot;
18790
&quot;bind&quot;
&quot;tailnet&quot;
&quot;tls&quot;
&quot;enabled&quot;
true
&quot;autoGenerate&quot;
true
Cron
Copy
cron
enabled
true
maxConcurrentRuns
webhook
&quot;https://example.invalid/cron-finished&quot;
// optional, must be http:// or https://
webhookToken
&quot;replace-with-dedicated-token&quot;
// optional bearer token for outbound webhook auth
sessionRetention
&quot;24h&quot;
// duration string or false
sessionRetention
: how long to keep completed cron sessions before pruning. Default:
24h
webhook
: finished-run webhook endpoint, only used when the job has
notify: true
webhookToken
: dedicated bearer token for webhook auth, if omitted no auth header is sent.
See
Cron Jobs
Media model template variables
Template placeholders expanded in
tools.media.*.models[].args
Variable
Description
{{Body}}
Full inbound message body
{{RawBody}}
Raw body (no history/sender wrappers)
{{BodyStripped}}
Body with group mentions stripped
{{From}}
Sender identifier
{{To}}
Destination identifier
{{MessageSid}}
Channel message id
{{SessionId}}
Current session UUID
{{IsNewSession}}
&quot;true&quot;
when new session created
{{MediaUrl}}
Inbound media pseudo-URL
{{MediaPath}}
Local media path
{{MediaType}}
Media type (image/audio/document/…)
{{Transcript}}
Audio transcript
{{Prompt}}
Resolved media prompt for CLI entries
{{MaxChars}}
Resolved max output chars for CLI entries
{{ChatType}}
&quot;direct&quot;
&quot;group&quot;
{{GroupSubject}}
Group subject (best effort)
{{GroupMembers}}
Group members preview (best effort)
{{SenderName}}
Sender display name (best effort)
{{SenderE164}}
Sender phone number (best effort)
{{Provider}}
Provider hint (whatsapp, telegram, discord, etc.)
Config includes (
$include
Split config into multiple files:
Copy
// ~/.openclaw/openclaw.json
gateway
port
18789 }
agents
{ $
include
&quot;./agents.json5&quot;
broadcast
include
&quot;./clients/mueller.json5&quot;
&quot;./clients/schmidt.json5&quot;
Merge behavior:
Single file: replaces the containing object.
Array of files: deep-merged in order (later overrides earlier).
Sibling keys: merged after includes (override included values).
Nested includes: up to 10 levels deep.
Paths: relative (to the including file), absolute, or
../
parent references.
Errors: clear messages for missing files, parse errors, and circular includes.
Related:
Configuration
Configuration Examples
Doctor
Configuration
Configuration Examples

---
## Gateway > Configuration

[Source: https://docs.openclaw.ai/gateway/configuration]

Configuration - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Configuration and operations
Configuration
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
Gateway
Gateway Runbook
Configuration and operations
Configuration
Configuration Reference
Configuration Examples
Authentication
Trusted proxy auth
Health Checks
Heartbeat
Doctor
Logging
Gateway Lock
Background Exec and Process Tool
Multiple Gateways
Troubleshooting
Security and sandboxing
Protocols and APIs
Networking and discovery
Remote access
Remote Access
Remote Gateway Setup
Tailscale
Security
Formal Verification (Security Models)
Web interfaces
Web
Control UI
Dashboard
WebChat
TUI
Configuration
Minimal config
Editing config
Strict validation
Common tasks
Config hot reload
Reload modes
What hot-applies vs what needs a restart
Config RPC (programmatic updates)
Environment variables
Full reference
Configuration and operations
Configuration
Configuration
OpenClaw reads an optional
JSON5
config from
~/.openclaw/openclaw.json
If the file is missing, OpenClaw uses safe defaults. Common reasons to add a config:
Connect channels and control who can message the bot
Set models, tools, sandboxing, or automation (cron, hooks)
Tune sessions, media, networking, or UI
See the
full reference
for every available field.
New to configuration?
Start with
openclaw onboard
for interactive setup, or check out the
Configuration Examples
guide for complete copy-paste configs.
Minimal config
Copy
// ~/.openclaw/openclaw.json
agents
defaults
workspace
&quot;~/.openclaw/workspace&quot;
} }
channels
whatsapp
allowFrom
&quot;+15555550123&quot;
] } }
Editing config
Interactive wizard
CLI (one-liners)
Control UI
Direct edit
Copy
openclaw
onboard
# full setup wizard
openclaw
configure
# config wizard
Copy
openclaw
config
get
agents.defaults.workspace
openclaw
config
set
agents.defaults.heartbeat.every
&quot;2h&quot;
openclaw
config
unset
tools.web.search.apiKey
Open
http://127.0.0.1:18789
and use the
Config
tab.
The Control UI renders a form from the config schema, with a
Raw JSON
editor as an escape hatch.
Edit
~/.openclaw/openclaw.json
directly. The Gateway watches the file and applies changes automatically (see
hot reload
Strict validation
OpenClaw only accepts configurations that fully match the schema. Unknown keys, malformed types, or invalid values cause the Gateway to
refuse to start
. The only root-level exception is
$schema
(string), so editors can attach JSON Schema metadata.
When validation fails:
The Gateway does not boot
Only diagnostic commands work (
openclaw doctor
openclaw logs
openclaw health
openclaw status
Run
openclaw doctor
to see exact issues
Run
openclaw doctor --fix
(or
--yes
) to apply repairs
Common tasks
Set up a channel (WhatsApp, Telegram, Discord, etc.)
Each channel has its own config section under
channels.&lt;provider&gt;
. See the dedicated channel page for setup steps:
WhatsApp
channels.whatsapp
Telegram
channels.telegram
Discord
channels.discord
Slack
channels.slack
Signal
channels.signal
iMessage
channels.imessage
Google Chat
channels.googlechat
Mattermost
channels.mattermost
MS Teams
channels.msteams
All channels share the same DM policy pattern:
Copy
channels
telegram
enabled
true
botToken
&quot;123:abc&quot;
dmPolicy
&quot;pairing&quot;
// pairing | allowlist | open | disabled
allowFrom
&quot;tg:123&quot;
// only for allowlist/open
Choose and configure models
Set the primary model and optional fallbacks:
Copy
agents
defaults
model
primary
&quot;anthropic/claude-sonnet-4-5&quot;
fallbacks
&quot;openai/gpt-5.2&quot;
models
&quot;anthropic/claude-sonnet-4-5&quot;
alias
&quot;Sonnet&quot;
&quot;openai/gpt-5.2&quot;
alias
&quot;GPT&quot;
agents.defaults.models
defines the model catalog and acts as the allowlist for
/model
Model refs use
provider/model
format (e.g.
anthropic/claude-opus-4-6
See
Models CLI
for switching models in chat and
Model Failover
for auth rotation and fallback behavior.
For custom/self-hosted providers, see
Custom providers
in the reference.
Control who can message the bot
DM access is controlled per channel via
dmPolicy
&quot;pairing&quot;
(default): unknown senders get a one-time pairing code to approve
&quot;allowlist&quot;
: only senders in
allowFrom
(or the paired allow store)
&quot;open&quot;
: allow all inbound DMs (requires
allowFrom: [&quot;*&quot;]
&quot;disabled&quot;
: ignore all DMs
For groups, use
groupPolicy
groupAllowFrom
or channel-specific allowlists.
See the
full reference
for per-channel details.
Set up group chat mention gating
Group messages default to
require mention
. Configure patterns per agent:
Copy
agents
list
&quot;main&quot;
groupChat
mentionPatterns
&quot;@openclaw&quot;
&quot;openclaw&quot;
channels
whatsapp
groups
&quot;*&quot;
requireMention
true
} }
Metadata mentions
: native @-mentions (WhatsApp tap-to-mention, Telegram @bot, etc.)
Text patterns
: regex patterns in
mentionPatterns
See
full reference
for per-channel overrides and self-chat mode.
Configure sessions and resets
Sessions control conversation continuity and isolation:
Copy
session
dmScope
&quot;per-channel-peer&quot;
// recommended for multi-user
reset
mode
&quot;daily&quot;
atHour
idleMinutes
120
dmScope
main
(shared) |
per-peer
per-channel-peer
per-account-channel-peer
See
Session Management
for scoping, identity links, and send policy.
See
full reference
for all fields.
Enable sandboxing
Run agent sessions in isolated Docker containers:
Copy
agents
defaults
sandbox
mode
&quot;non-main&quot;
// off | non-main | all
scope
&quot;agent&quot;
// session | agent | shared
Build the image first:
scripts/sandbox-setup.sh
See
Sandboxing
for the full guide and
full reference
for all options.
Set up heartbeat (periodic check-ins)
Copy
agents
defaults
heartbeat
every
&quot;30m&quot;
target
&quot;last&quot;
every
: duration string (
30m
). Set
to disable.
target
last
whatsapp
telegram
discord
none
See
Heartbeat
for the full guide.
Configure cron jobs
Copy
cron
enabled
true
maxConcurrentRuns
sessionRetention
&quot;24h&quot;
See
Cron jobs
for the feature overview and CLI examples.
Set up webhooks (hooks)
Enable HTTP webhook endpoints on the Gateway:
Copy
hooks
enabled
true
token
&quot;shared-secret&quot;
path
&quot;/hooks&quot;
defaultSessionKey
&quot;hook:ingress&quot;
allowRequestSessionKey
false
allowedSessionKeyPrefixes
&quot;hook:&quot;
mappings
match
path
&quot;gmail&quot;
action
&quot;agent&quot;
agentId
&quot;main&quot;
deliver
true
See
full reference
for all mapping options and Gmail integration.
Configure multi-agent routing
Run multiple isolated agents with separate workspaces and sessions:
Copy
agents
list
&quot;home&quot;
default
true
workspace
&quot;~/.openclaw/workspace-home&quot;
&quot;work&quot;
workspace
&quot;~/.openclaw/workspace-work&quot;
bindings
agentId
&quot;home&quot;
match
channel
&quot;whatsapp&quot;
accountId
&quot;personal&quot;
} }
agentId
&quot;work&quot;
match
channel
&quot;whatsapp&quot;
accountId
&quot;biz&quot;
} }
See
Multi-Agent
and
full reference
for binding rules and per-agent access profiles.
Split config into multiple files ($include)
Use
$include
to organize large configs:
Copy
// ~/.openclaw/openclaw.json
gateway
port
18789 }
agents
{ $
include
&quot;./agents.json5&quot;
broadcast
include
&quot;./clients/a.json5&quot;
&quot;./clients/b.json5&quot;
Single file
: replaces the containing object
Array of files
: deep-merged in order (later wins)
Sibling keys
: merged after includes (override included values)
Nested includes
: supported up to 10 levels deep
Relative paths
: resolved relative to the including file
Error handling
: clear errors for missing files, parse errors, and circular includes
Config hot reload
The Gateway watches
~/.openclaw/openclaw.json
and applies changes automatically — no manual restart needed for most settings.
Reload modes
Mode
Behavior
hybrid
(default)
Hot-applies safe changes instantly. Automatically restarts for critical ones.
hot
Hot-applies safe changes only. Logs a warning when a restart is needed — you handle it.
restart
Restarts the Gateway on any config change, safe or not.
off
Disables file watching. Changes take effect on the next manual restart.
Copy
gateway
reload
mode
&quot;hybrid&quot;
debounceMs
300 }
What hot-applies vs what needs a restart
Most fields hot-apply without downtime. In
hybrid
mode, restart-required changes are handled automatically.
Category
Fields
Restart needed?
Channels
channels.*
web
(WhatsApp) — all built-in and extension channels
Agent &amp; models
agent
agents
models
routing
Automation
hooks
cron
agent.heartbeat
Sessions &amp; messages
session
messages
Tools &amp; media
tools
browser
skills
audio
talk
UI &amp; misc
logging
identity
bindings
Gateway server
gateway.*
(port, bind, auth, tailscale, TLS, HTTP)
Yes
Infrastructure
discovery
canvasHost
plugins
Yes
gateway.reload
and
gateway.remote
are exceptions — changing them does
not
trigger a restart.
Config RPC (programmatic updates)
config.apply (full replace)
Validates + writes the full config and restarts the Gateway in one step.
config.apply
replaces the
entire config
. Use
config.patch
for partial updates, or
openclaw config set
for single keys.
Params:
raw
(string) — JSON5 payload for the entire config
baseHash
(optional) — config hash from
config.get
(required when config exists)
sessionKey
(optional) — session key for the post-restart wake-up ping
note
(optional) — note for the restart sentinel
restartDelayMs
(optional) — delay before restart (default 2000)
Copy
openclaw
gateway
call
config.get
--params
&#x27;{}&#x27;
# capture payload.hash
openclaw
gateway
call
config.apply
--params
&#x27;{
&quot;raw&quot;: &quot;{ agents: { defaults: { workspace: \&quot;~/.openclaw/workspace\&quot; } } }&quot;,
&quot;baseHash&quot;: &quot;&lt;hash&gt;&quot;,
&quot;sessionKey&quot;: &quot;agent:main:whatsapp:dm:+15555550123&quot;
}&#x27;
config.patch (partial update)
Merges a partial update into the existing config (JSON merge patch semantics):
Objects merge recursively
null
deletes a key
Arrays replace
Params:
raw
(string) — JSON5 with just the keys to change
baseHash
(required) — config hash from
config.get
sessionKey
note
restartDelayMs
— same as
config.apply
Copy
openclaw
gateway
call
config.patch
--params
&#x27;{
&quot;raw&quot;: &quot;{ channels: { telegram: { groups: { \&quot;*\&quot;: { requireMention: false } } } } }&quot;,
&quot;baseHash&quot;: &quot;&lt;hash&gt;&quot;
}&#x27;
Environment variables
OpenClaw reads env vars from the parent process plus:
.env
from the current working directory (if present)
~/.openclaw/.env
(global fallback)
Neither file overrides existing env vars. You can also set inline env vars in config:
Copy
env
OPENROUTER_API_KEY
&quot;sk-or-...&quot;
vars
GROQ_API_KEY
&quot;gsk-...&quot;
Shell env import (optional)
If enabled and expected keys aren’t set, OpenClaw runs your login shell and imports only the missing keys:
Copy
env
shellEnv
enabled
true
timeoutMs
15000 }
Env var equivalent:
OPENCLAW_LOAD_SHELL_ENV=1
Env var substitution in config values
Reference env vars in any config string value with
${VAR_NAME}
Copy
gateway
auth
token
&quot;${OPENCLAW_GATEWAY_TOKEN}&quot;
} }
models
providers
custom
apiKey
&quot;${CUSTOM_API_KEY}&quot;
} } }
Rules:
Only uppercase names matched:
[A-Z_][A-Z0-9_]*
Missing/empty vars throw an error at load time
Escape with
$${VAR}
for literal output
Works inside
$include
files
Inline substitution:
&quot;${BASE}/v1&quot;
&quot;https://api.example.com/v1&quot;
See
Environment
for full precedence and sources.
Full reference
For the complete field-by-field reference, see
Configuration Reference
Related:
Configuration Examples
Configuration Reference
Doctor
Gateway Runbook
Configuration Reference

---
## Gateway > Discovery

[Source: https://docs.openclaw.ai/gateway/discovery]

Discovery and Transports - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Networking and discovery
Discovery and Transports
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
Gateway
Gateway Runbook
Configuration and operations
Security and sandboxing
Protocols and APIs
Networking and discovery
Network model
Gateway-Owned Pairing
Discovery and Transports
Bonjour Discovery
Remote access
Remote Access
Remote Gateway Setup
Tailscale
Security
Formal Verification (Security Models)
Web interfaces
Web
Control UI
Dashboard
WebChat
TUI
Discovery &amp; transports
Terms
Why we keep both “direct” and SSH
Discovery inputs (how clients learn where the gateway is)
1) Bonjour / mDNS (LAN only)
Service beacon details
2) Tailnet (cross-network)
3) Manual / SSH target
Transport selection (client policy)
Pairing + auth (direct transport)
Responsibilities by component
Networking and discovery
Discovery and Transports
Discovery &amp; transports
OpenClaw has two distinct problems that look similar on the surface:
Operator remote control
: the macOS menu bar app controlling a gateway running elsewhere.
Node pairing
: iOS/Android (and future nodes) finding a gateway and pairing securely.
The design goal is to keep all network discovery/advertising in the
Node Gateway
openclaw gateway
) and keep clients (mac app, iOS) as consumers.
Terms
Gateway
: a single long-running gateway process that owns state (sessions, pairing, node registry) and runs channels. Most setups use one per host; isolated multi-gateway setups are possible.
Gateway WS (control plane)
: the WebSocket endpoint on
127.0.0.1:18789
by default; can be bound to LAN/tailnet via
gateway.bind
Direct WS transport
: a LAN/tailnet-facing Gateway WS endpoint (no SSH).
SSH transport (fallback)
: remote control by forwarding
127.0.0.1:18789
over SSH.
Legacy TCP bridge (deprecated/removed)
: older node transport (see
Bridge protocol
); no longer advertised for discovery.
Protocol details:
Gateway protocol
Bridge protocol (legacy)
Why we keep both “direct” and SSH
Direct WS
is the best UX on the same network and within a tailnet:
auto-discovery on LAN via Bonjour
pairing tokens + ACLs owned by the gateway
no shell access required; protocol surface can stay tight and auditable
SSH
remains the universal fallback:
works anywhere you have SSH access (even across unrelated networks)
survives multicast/mDNS issues
requires no new inbound ports besides SSH
Discovery inputs (how clients learn where the gateway is)
1) Bonjour / mDNS (LAN only)
Bonjour is best-effort and does not cross networks. It is only used for “same LAN” convenience.
Target direction:
The
gateway
advertises its WS endpoint via Bonjour.
Clients browse and show a “pick a gateway” list, then store the chosen endpoint.
Troubleshooting and beacon details:
Bonjour
Service beacon details
Service types:
_openclaw-gw._tcp
(gateway transport beacon)
TXT keys (non-secret):
role=gateway
lanHost=&lt;hostname&gt;.local
sshPort=22
(or whatever is advertised)
gatewayPort=18789
(Gateway WS + HTTP)
gatewayTls=1
(only when TLS is enabled)
gatewayTlsSha256=&lt;sha256&gt;
(only when TLS is enabled and fingerprint is available)
canvasPort=&lt;port&gt;
(canvas host port; currently the same as
gatewayPort
when the canvas host is enabled)
cliPath=&lt;path&gt;
(optional; absolute path to a runnable
openclaw
entrypoint or binary)
tailnetDns=&lt;magicdns&gt;
(optional hint; auto-detected when Tailscale is available)
Security notes:
Bonjour/mDNS TXT records are
unauthenticated
. Clients must treat TXT values as UX hints only.
Routing (host/port) should prefer the
resolved service endpoint
(SRV + A/AAAA) over TXT-provided
lanHost
tailnetDns
, or
gatewayPort
TLS pinning must never allow an advertised
gatewayTlsSha256
to override a previously stored pin.
iOS/Android nodes should treat discovery-based direct connects as
TLS-only
and require an explicit “trust this fingerprint” confirmation before storing a first-time pin (out-of-band verification).
Disable/override:
OPENCLAW_DISABLE_BONJOUR=1
disables advertising.
gateway.bind
~/.openclaw/openclaw.json
controls the Gateway bind mode.
OPENCLAW_SSH_PORT
overrides the SSH port advertised in TXT (defaults to 22).
OPENCLAW_TAILNET_DNS
publishes a
tailnetDns
hint (MagicDNS).
OPENCLAW_CLI_PATH
overrides the advertised CLI path.
2) Tailnet (cross-network)
For London/Vienna style setups, Bonjour won’t help. The recommended “direct” target is:
Tailscale MagicDNS name (preferred) or a stable tailnet IP.
If the gateway can detect it is running under Tailscale, it publishes
tailnetDns
as an optional hint for clients (including wide-area beacons).
3) Manual / SSH target
When there is no direct route (or direct is disabled), clients can always connect via SSH by forwarding the loopback gateway port.
See
Remote access
Transport selection (client policy)
Recommended client behavior:
If a paired direct endpoint is configured and reachable, use it.
Else, if Bonjour finds a gateway on LAN, offer a one-tap “Use this gateway” choice and save it as the direct endpoint.
Else, if a tailnet DNS/IP is configured, try direct.
Else, fall back to SSH.
Pairing + auth (direct transport)
The gateway is the source of truth for node/client admission.
Pairing requests are created/approved/rejected in the gateway (see
Gateway pairing
The gateway enforces:
auth (token / keypair)
scopes/ACLs (the gateway is not a raw proxy to every method)
rate limits
Responsibilities by component
Gateway
: advertises discovery beacons, owns pairing decisions, and hosts the WS endpoint.
macOS app
: helps you pick a gateway, shows pairing prompts, and uses SSH only as a fallback.
iOS/Android nodes
: browse Bonjour as a convenience and connect to the paired Gateway WS.
Gateway-Owned Pairing
Bonjour Discovery

---
## Gateway > Doctor

[Source: https://docs.openclaw.ai/gateway/doctor]

Doctor - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Configuration and operations
Doctor
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
Gateway
Gateway Runbook
Configuration and operations
Configuration
Configuration Reference
Configuration Examples
Authentication
Trusted proxy auth
Health Checks
Heartbeat
Doctor
Logging
Gateway Lock
Background Exec and Process Tool
Multiple Gateways
Troubleshooting
Security and sandboxing
Protocols and APIs
Networking and discovery
Remote access
Remote Access
Remote Gateway Setup
Tailscale
Security
Formal Verification (Security Models)
Web interfaces
Web
Control UI
Dashboard
WebChat
TUI
Doctor
Quick start
Headless / automation
What it does (summary)
Detailed behavior and rationale
0) Optional update (git installs)
1) Config normalization
2) Legacy config key migrations
2b) OpenCode Zen provider overrides
3) Legacy state migrations (disk layout)
4) State integrity checks (session persistence, routing, and safety)
5) Model auth health (OAuth expiry)
6) Hooks model validation
7) Sandbox image repair
8) Gateway service migrations and cleanup hints
9) Security warnings
10) systemd linger (Linux)
11) Skills status
12) Gateway auth checks (local token)
13) Gateway health check + restart
14) Channel status warnings
15) Supervisor config audit + repair
16) Gateway runtime + port diagnostics
17) Gateway runtime best practices
18) Config write + wizard metadata
19) Workspace tips (backup + memory system)
Configuration and operations
Doctor
Doctor
openclaw doctor
is the repair + migration tool for OpenClaw. It fixes stale
config/state, checks health, and provides actionable repair steps.
Quick start
Copy
openclaw
doctor
Headless / automation
Copy
openclaw
doctor
--yes
Accept defaults without prompting (including restart/service/sandbox repair steps when applicable).
Copy
openclaw
doctor
--repair
Apply recommended repairs without prompting (repairs + restarts where safe).
Copy
openclaw
doctor
--repair
--force
Apply aggressive repairs too (overwrites custom supervisor configs).
Copy
openclaw
doctor
--non-interactive
Run without prompts and only apply safe migrations (config normalization + on-disk state moves). Skips restart/service/sandbox actions that require human confirmation.
Legacy state migrations run automatically when detected.
Copy
openclaw
doctor
--deep
Scan system services for extra gateway installs (launchd/systemd/schtasks).
If you want to review changes before writing, open the config file first:
Copy
cat
~/.openclaw/openclaw.json
What it does (summary)
Optional pre-flight update for git installs (interactive only).
UI protocol freshness check (rebuilds Control UI when the protocol schema is newer).
Health check + restart prompt.
Skills status summary (eligible/missing/blocked).
Config normalization for legacy values.
OpenCode Zen provider override warnings (
models.providers.opencode
Legacy on-disk state migration (sessions/agent dir/WhatsApp auth).
State integrity and permissions checks (sessions, transcripts, state dir).
Config file permission checks (chmod 600) when running locally.
Model auth health: checks OAuth expiry, can refresh expiring tokens, and reports auth-profile cooldown/disabled states.
Extra workspace dir detection (
~/openclaw
Sandbox image repair when sandboxing is enabled.
Legacy service migration and extra gateway detection.
Gateway runtime checks (service installed but not running; cached launchd label).
Channel status warnings (probed from the running gateway).
Supervisor config audit (launchd/systemd/schtasks) with optional repair.
Gateway runtime best-practice checks (Node vs Bun, version-manager paths).
Gateway port collision diagnostics (default
18789
Security warnings for open DM policies.
Gateway auth warnings when no
gateway.auth.token
is set (local mode; offers token generation).
systemd linger check on Linux.
Source install checks (pnpm workspace mismatch, missing UI assets, missing tsx binary).
Writes updated config + wizard metadata.
Detailed behavior and rationale
0) Optional update (git installs)
If this is a git checkout and doctor is running interactively, it offers to
update (fetch/rebase/build) before running doctor.
1) Config normalization
If the config contains legacy value shapes (for example
messages.ackReaction
without a channel-specific override), doctor normalizes them into the current
schema.
2) Legacy config key migrations
When the config contains deprecated keys, other commands refuse to run and ask
you to run
openclaw doctor
Doctor will:
Explain which legacy keys were found.
Show the migration it applied.
Rewrite
~/.openclaw/openclaw.json
with the updated schema.
The Gateway also auto-runs doctor migrations on startup when it detects a
legacy config format, so stale configs are repaired without manual intervention.
Current migrations:
routing.allowFrom
channels.whatsapp.allowFrom
routing.groupChat.requireMention
channels.whatsapp/telegram/imessage.groups.&quot;*&quot;.requireMention
routing.groupChat.historyLimit
messages.groupChat.historyLimit
routing.groupChat.mentionPatterns
messages.groupChat.mentionPatterns
routing.queue
messages.queue
routing.bindings
→ top-level
bindings
routing.agents
routing.defaultAgentId
agents.list
agents.list[].default
routing.agentToAgent
tools.agentToAgent
routing.transcribeAudio
tools.media.audio.models
bindings[].match.accountID
bindings[].match.accountId
identity
agents.list[].identity
agent.*
agents.defaults
tools.*
(tools/elevated/exec/sandbox/subagents)
agent.model
allowedModels
modelAliases
modelFallbacks
imageModelFallbacks
agents.defaults.models
agents.defaults.model.primary/fallbacks
agents.defaults.imageModel.primary/fallbacks
2b) OpenCode Zen provider overrides
If you’ve added
models.providers.opencode
(or
opencode-zen
) manually, it
overrides the built-in OpenCode Zen catalog from
@mariozechner/pi-ai
. That can
force every model onto a single API or zero out costs. Doctor warns so you can
remove the override and restore per-model API routing + costs.
3) Legacy state migrations (disk layout)
Doctor can migrate older on-disk layouts into the current structure:
Sessions store + transcripts:
from
~/.openclaw/sessions/
~/.openclaw/agents/&lt;agentId&gt;/sessions/
Agent dir:
from
~/.openclaw/agent/
~/.openclaw/agents/&lt;agentId&gt;/agent/
WhatsApp auth state (Baileys):
from legacy
~/.openclaw/credentials/*.json
(except
oauth.json
~/.openclaw/credentials/whatsapp/&lt;accountId&gt;/...
(default account id:
default
These migrations are best-effort and idempotent; doctor will emit warnings when
it leaves any legacy folders behind as backups. The Gateway/CLI also auto-migrates
the legacy sessions + agent dir on startup so history/auth/models land in the
per-agent path without a manual doctor run. WhatsApp auth is intentionally only
migrated via
openclaw doctor
4) State integrity checks (session persistence, routing, and safety)
The state directory is the operational brainstem. If it vanishes, you lose
sessions, credentials, logs, and config (unless you have backups elsewhere).
Doctor checks:
State dir missing
: warns about catastrophic state loss, prompts to recreate
the directory, and reminds you that it cannot recover missing data.
State dir permissions
: verifies writability; offers to repair permissions
(and emits a
chown
hint when owner/group mismatch is detected).
Session dirs missing
sessions/
and the session store directory are
required to persist history and avoid
ENOENT
crashes.
Transcript mismatch
: warns when recent session entries have missing
transcript files.
Main session “1-line JSONL”
: flags when the main transcript has only one
line (history is not accumulating).
Multiple state dirs
: warns when multiple
~/.openclaw
folders exist across
home directories or when
OPENCLAW_STATE_DIR
points elsewhere (history can
split between installs).
Remote mode reminder
: if
gateway.mode=remote
, doctor reminds you to run
it on the remote host (the state lives there).
Config file permissions
: warns if
~/.openclaw/openclaw.json
group/world readable and offers to tighten to
600
5) Model auth health (OAuth expiry)
Doctor inspects OAuth profiles in the auth store, warns when tokens are
expiring/expired, and can refresh them when safe. If the Anthropic Claude Code
profile is stale, it suggests running
claude setup-token
(or pasting a setup-token).
Refresh prompts only appear when running interactively (TTY);
--non-interactive
skips refresh attempts.
Doctor also reports auth profiles that are temporarily unusable due to:
short cooldowns (rate limits/timeouts/auth failures)
longer disables (billing/credit failures)
6) Hooks model validation
hooks.gmail.model
is set, doctor validates the model reference against the
catalog and allowlist and warns when it won’t resolve or is disallowed.
7) Sandbox image repair
When sandboxing is enabled, doctor checks Docker images and offers to build or
switch to legacy names if the current image is missing.
8) Gateway service migrations and cleanup hints
Doctor detects legacy gateway services (launchd/systemd/schtasks) and
offers to remove them and install the OpenClaw service using the current gateway
port. It can also scan for extra gateway-like services and print cleanup hints.
Profile-named OpenClaw gateway services are considered first-class and are not
flagged as “extra.”
9) Security warnings
Doctor emits warnings when a provider is open to DMs without an allowlist, or
when a policy is configured in a dangerous way.
10) systemd linger (Linux)
If running as a systemd user service, doctor ensures lingering is enabled so the
gateway stays alive after logout.
11) Skills status
Doctor prints a quick summary of eligible/missing/blocked skills for the current
workspace.
12) Gateway auth checks (local token)
Doctor warns when
gateway.auth
is missing on a local gateway and offers to
generate a token. Use
openclaw doctor --generate-gateway-token
to force token
creation in automation.
13) Gateway health check + restart
Doctor runs a health check and offers to restart the gateway when it looks
unhealthy.
14) Channel status warnings
If the gateway is healthy, doctor runs a channel status probe and reports
warnings with suggested fixes.
15) Supervisor config audit + repair
Doctor checks the installed supervisor config (launchd/systemd/schtasks) for
missing or outdated defaults (e.g., systemd network-online dependencies and
restart delay). When it finds a mismatch, it recommends an update and can
rewrite the service file/task to the current defaults.
Notes:
openclaw doctor
prompts before rewriting supervisor config.
openclaw doctor --yes
accepts the default repair prompts.
openclaw doctor --repair
applies recommended fixes without prompts.
openclaw doctor --repair --force
overwrites custom supervisor configs.
You can always force a full rewrite via
openclaw gateway install --force
16) Gateway runtime + port diagnostics
Doctor inspects the service runtime (PID, last exit status) and warns when the
service is installed but not actually running. It also checks for port collisions
on the gateway port (default
18789
) and reports likely causes (gateway already
running, SSH tunnel).
17) Gateway runtime best practices
Doctor warns when the gateway service runs on Bun or a version-managed Node path
nvm
fnm
volta
asdf
, etc.). WhatsApp + Telegram channels require Node,
and version-manager paths can break after upgrades because the service does not
load your shell init. Doctor offers to migrate to a system Node install when
available (Homebrew/apt/choco).
18) Config write + wizard metadata
Doctor persists any config changes and stamps wizard metadata to record the
doctor run.
19) Workspace tips (backup + memory system)
Doctor suggests a workspace memory system when missing and prints a backup tip
if the workspace is not already under git.
See
/concepts/agent-workspace
for a full guide to
workspace structure and git backup (recommended private GitHub or GitLab).
Heartbeat
Logging

---
## Gateway > Gateway Lock

[Source: https://docs.openclaw.ai/gateway/gateway-lock]

Gateway Lock - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Configuration and operations
Gateway Lock
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
Gateway
Gateway Runbook
Configuration and operations
Configuration
Configuration Reference
Configuration Examples
Authentication
Trusted proxy auth
Health Checks
Heartbeat
Doctor
Logging
Gateway Lock
Background Exec and Process Tool
Multiple Gateways
Troubleshooting
Security and sandboxing
Protocols and APIs
Networking and discovery
Remote access
Remote Access
Remote Gateway Setup
Tailscale
Security
Formal Verification (Security Models)
Web interfaces
Web
Control UI
Dashboard
WebChat
TUI
Gateway lock
Why
Mechanism
Error surface
Operational notes
Configuration and operations
Gateway Lock
Gateway lock
Last updated: 2025-12-11
Why
Ensure only one gateway instance runs per base port on the same host; additional gateways must use isolated profiles and unique ports.
Survive crashes/SIGKILL without leaving stale lock files.
Fail fast with a clear error when the control port is already occupied.
Mechanism
The gateway binds the WebSocket listener (default
ws://127.0.0.1:18789
) immediately on startup using an exclusive TCP listener.
If the bind fails with
EADDRINUSE
, startup throws
GatewayLockError(&quot;another gateway instance is already listening on ws://127.0.0.1:&lt;port&gt;&quot;)
The OS releases the listener automatically on any process exit, including crashes and SIGKILL—no separate lock file or cleanup step is needed.
On shutdown the gateway closes the WebSocket server and underlying HTTP server to free the port promptly.
Error surface
If another process holds the port, startup throws
GatewayLockError(&quot;another gateway instance is already listening on ws://127.0.0.1:&lt;port&gt;&quot;)
Other bind failures surface as
GatewayLockError(&quot;failed to bind gateway socket on ws://127.0.0.1:&lt;port&gt;: …&quot;)
Operational notes
If the port is occupied by
another
process, the error is the same; free the port or choose another with
openclaw gateway --port &lt;port&gt;
The macOS app still maintains its own lightweight PID guard before spawning the gateway; the runtime lock is enforced by the WebSocket bind.
Logging
Background Exec and Process Tool

---
## Gateway > Health

[Source: https://docs.openclaw.ai/gateway/health]

Health Checks - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Configuration and operations
Health Checks
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
Gateway
Gateway Runbook
Configuration and operations
Configuration
Configuration Reference
Configuration Examples
Authentication
Trusted proxy auth
Health Checks
Heartbeat
Doctor
Logging
Gateway Lock
Background Exec and Process Tool
Multiple Gateways
Troubleshooting
Security and sandboxing
Protocols and APIs
Networking and discovery
Remote access
Remote Access
Remote Gateway Setup
Tailscale
Security
Formal Verification (Security Models)
Web interfaces
Web
Control UI
Dashboard
WebChat
TUI
Health Checks (CLI)
Quick checks
Deep diagnostics
When something fails
Dedicated “health” command
Configuration and operations
Health Checks
Health Checks (CLI)
Short guide to verify channel connectivity without guessing.
Quick checks
openclaw status
— local summary: gateway reachability/mode, update hint, linked channel auth age, sessions + recent activity.
openclaw status --all
— full local diagnosis (read-only, color, safe to paste for debugging).
openclaw status --deep
— also probes the running Gateway (per-channel probes when supported).
openclaw health --json
— asks the running Gateway for a full health snapshot (WS-only; no direct Baileys socket).
Send
/status
as a standalone message in WhatsApp/WebChat to get a status reply without invoking the agent.
Logs: tail
/tmp/openclaw/openclaw-*.log
and filter for
web-heartbeat
web-reconnect
web-auto-reply
web-inbound
Deep diagnostics
Creds on disk:
ls -l ~/.openclaw/credentials/whatsapp/&lt;accountId&gt;/creds.json
(mtime should be recent).
Session store:
ls -l ~/.openclaw/agents/&lt;agentId&gt;/sessions/sessions.json
(path can be overridden in config). Count and recent recipients are surfaced via
status
Relink flow:
openclaw channels logout &amp;&amp; openclaw channels login --verbose
when status codes 409–515 or
loggedOut
appear in logs. (Note: the QR login flow auto-restarts once for status 515 after pairing.)
When something fails
logged out
or status 409–515 → relink with
openclaw channels logout
then
openclaw channels login
Gateway unreachable → start it:
openclaw gateway --port 18789
(use
--force
if the port is busy).
No inbound messages → confirm linked phone is online and the sender is allowed (
channels.whatsapp.allowFrom
); for group chats, ensure allowlist + mention rules match (
channels.whatsapp.groups
agents.list[].groupChat.mentionPatterns
Dedicated “health” command
openclaw health --json
asks the running Gateway for its health snapshot (no direct channel sockets from the CLI). It reports linked creds/auth age when available, per-channel probe summaries, session-store summary, and a probe duration. It exits non-zero if the Gateway is unreachable or the probe fails/timeouts. Use
--timeout &lt;ms&gt;
to override the 10s default.
Trusted proxy auth
Heartbeat

---
## Gateway > Heartbeat

[Source: https://docs.openclaw.ai/gateway/heartbeat]

# Heartbeat Documentation Summary

## Overview

Heartbeat enables **periodic agent turns** in the main session, allowing models to surface urgent matters without excessive notifications. The feature distinguishes itself from cron jobs through different use cases.

## Quick Start

Basic setup involves:
1. Keeping heartbeats enabled (default: 30 minutes, or 1 hour with Anthropic OAuth)
2. Optionally creating a `HEARTBEAT.md` checklist in the workspace
3. Configuring message routing via the `target` parameter
4. Enabling reasoning delivery for transparency (optional)
5. Restricting to active hours if desired

Key configuration example:
```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m",
        target: "last",
        // activeHours: { start: "08:00", end: "24:00" },
        // includeReasoning: true,
      },
    },
  },
}
```

## Core Defaults

- **Interval**: "30m" by default (adjustable or disable with "0m")
- **Prompt**: Reads `HEARTBEAT.md` and replies with "HEARTBEAT_OK" if nothing requires attention
- **Active Hours**: Checked against configured timezone; skipped outside windows
- **Response Contract**: Return "HEARTBEAT_OK" when no action needed; omit it for alerts

## Response Handling

The system recognizes "HEARTBEAT_OK" appearing at message start or end (≤300 characters by default) as acknowledgment and suppresses delivery. Mid-message instances are treated as regular text. Alerts should exclude this token entirely.

## Configuration Scope

Settings cascade through hierarchy: global defaults → per-agent overrides → channel-level settings → multi-account refinements. If any agent has heartbeat configuration, only those agents run heartbeats.

## Active Hours Setup

Business-hours restriction example:
```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m",
        activeHours: {
          start: "09:00",
          end: "22:00",
          timezone: "America/New_York",
        },
      },
    },
  },
}
```

For 24/7 operation, omit `activeHours` or set "00:00" to "24:00". Avoid identical start/end times.

## HEARTBEAT.md (Optional Checklist)

This workspace file serves as a stable reminder list included with each heartbeat. The agent references it strictly and ignores inferred prior tasks. Empty files trigger API call optimization by skipping the run.

The file is updatable through normal chat requests.

## Advanced Features

- **Reasoning Delivery**: Enable `includeReasoning: true` for transparency
- **Manual Wake**: Trigger immediate heartbeats via `openclaw system event`
- **Multi-Account Channels**: Use `accountId` to target specific accounts (Telegram, etc.)
- **Visibility Controls**: Configure `showOk`, `showAlerts`, and `useIndicator` per-channel or per-account

## Cost Considerations

Heartbeats consume full agent turns. Shorter intervals increase token usage. Maintaining minimal `HEARTBEAT.md` files and selecting appropriate models helps optimize costs.

---
## Gateway > Local Models

[Source: https://docs.openclaw.ai/gateway/local-models]

Local Models - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Protocols and APIs
Local Models
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
Gateway
Gateway Runbook
Configuration and operations
Security and sandboxing
Protocols and APIs
Gateway Protocol
Bridge Protocol
OpenAI Chat Completions
Tools Invoke API
CLI Backends
Local Models
Networking and discovery
Remote access
Remote Access
Remote Gateway Setup
Tailscale
Security
Formal Verification (Security Models)
Web interfaces
Web
Control UI
Dashboard
WebChat
TUI
Local models
Recommended: LM Studio + MiniMax M2.1 (Responses API, full-size)
Hybrid config: hosted primary, local fallback
Local-first with hosted safety net
Regional hosting / data routing
Other OpenAI-compatible local proxies
Troubleshooting
Protocols and APIs
Local Models
Local models
Local is doable, but OpenClaw expects large context + strong defenses against prompt injection. Small cards truncate context and leak safety. Aim high:
≥2 maxed-out Mac Studios or equivalent GPU rig (~$30k+)
. A single
24 GB
GPU works only for lighter prompts with higher latency. Use the
largest / full-size model variant you can run
; aggressively quantized or “small” checkpoints raise prompt-injection risk (see
Security
Recommended: LM Studio + MiniMax M2.1 (Responses API, full-size)
Best current local stack. Load MiniMax M2.1 in LM Studio, enable the local server (default
http://127.0.0.1:1234
), and use Responses API to keep reasoning separate from final text.
Copy
agents
defaults
model
primary
&quot;lmstudio/minimax-m2.1-gs32&quot;
models
&quot;anthropic/claude-opus-4-6&quot;
alias
&quot;Opus&quot;
&quot;lmstudio/minimax-m2.1-gs32&quot;
alias
&quot;Minimax&quot;
models
mode
&quot;merge&quot;
providers
lmstudio
baseUrl
&quot;http://127.0.0.1:1234/v1&quot;
apiKey
&quot;lmstudio&quot;
api
&quot;openai-responses&quot;
models
&quot;minimax-m2.1-gs32&quot;
name
&quot;MiniMax M2.1 GS32&quot;
reasoning
false
input
&quot;text&quot;
cost
input
output
cacheRead
cacheWrite
0 }
contextWindow
196608
maxTokens
8192
Setup checklist
Install LM Studio:
https://lmstudio.ai
In LM Studio, download the
largest MiniMax M2.1 build available
(avoid “small”/heavily quantized variants), start the server, confirm
http://127.0.0.1:1234/v1/models
lists it.
Keep the model loaded; cold-load adds startup latency.
Adjust
contextWindow
maxTokens
if your LM Studio build differs.
For WhatsApp, stick to Responses API so only final text is sent.
Keep hosted models configured even when running local; use
models.mode: &quot;merge&quot;
so fallbacks stay available.
Hybrid config: hosted primary, local fallback
Copy
agents
defaults
model
primary
&quot;anthropic/claude-sonnet-4-5&quot;
fallbacks
&quot;lmstudio/minimax-m2.1-gs32&quot;
&quot;anthropic/claude-opus-4-6&quot;
models
&quot;anthropic/claude-sonnet-4-5&quot;
alias
&quot;Sonnet&quot;
&quot;lmstudio/minimax-m2.1-gs32&quot;
alias
&quot;MiniMax Local&quot;
&quot;anthropic/claude-opus-4-6&quot;
alias
&quot;Opus&quot;
models
mode
&quot;merge&quot;
providers
lmstudio
baseUrl
&quot;http://127.0.0.1:1234/v1&quot;
apiKey
&quot;lmstudio&quot;
api
&quot;openai-responses&quot;
models
&quot;minimax-m2.1-gs32&quot;
name
&quot;MiniMax M2.1 GS32&quot;
reasoning
false
input
&quot;text&quot;
cost
input
output
cacheRead
cacheWrite
0 }
contextWindow
196608
maxTokens
8192
Local-first with hosted safety net
Swap the primary and fallback order; keep the same providers block and
models.mode: &quot;merge&quot;
so you can fall back to Sonnet or Opus when the local box is down.
Regional hosting / data routing
Hosted MiniMax/Kimi/GLM variants also exist on OpenRouter with region-pinned endpoints (e.g., US-hosted). Pick the regional variant there to keep traffic in your chosen jurisdiction while still using
models.mode: &quot;merge&quot;
for Anthropic/OpenAI fallbacks.
Local-only remains the strongest privacy path; hosted regional routing is the middle ground when you need provider features but want control over data flow.
Other OpenAI-compatible local proxies
vLLM, LiteLLM, OAI-proxy, or custom gateways work if they expose an OpenAI-style
/v1
endpoint. Replace the provider block above with your endpoint and model ID:
Copy
models
mode
&quot;merge&quot;
providers
local
baseUrl
&quot;http://127.0.0.1:8000/v1&quot;
apiKey
&quot;sk-local&quot;
api
&quot;openai-responses&quot;
models
&quot;my-local-model&quot;
name
&quot;Local Model&quot;
reasoning
false
input
&quot;text&quot;
cost
input
output
cacheRead
cacheWrite
0 }
contextWindow
120000
maxTokens
8192
Keep
models.mode: &quot;merge&quot;
so hosted models stay available as fallbacks.
Troubleshooting
Gateway can reach the proxy?
curl http://127.0.0.1:1234/v1/models
LM Studio model unloaded? Reload; cold start is a common “hanging” cause.
Context errors? Lower
contextWindow
or raise your server limit.
Safety: local models skip provider-side filters; keep agents narrow and compaction on to limit prompt injection blast radius.
CLI Backends
Network model

---
## Gateway > Logging

[Source: https://docs.openclaw.ai/gateway/logging]

Logging - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Configuration and operations
Logging
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
Gateway
Gateway Runbook
Configuration and operations
Configuration
Configuration Reference
Configuration Examples
Authentication
Trusted proxy auth
Health Checks
Heartbeat
Doctor
Logging
Gateway Lock
Background Exec and Process Tool
Multiple Gateways
Troubleshooting
Security and sandboxing
Protocols and APIs
Networking and discovery
Remote access
Remote Access
Remote Gateway Setup
Tailscale
Security
Formal Verification (Security Models)
Web interfaces
Web
Control UI
Dashboard
WebChat
TUI
Logging
File-based logger
Console capture
Tool summary redaction
Gateway WebSocket logs
WS log style
Console formatting (subsystem logging)
Configuration and operations
Logging
Logging
For a user-facing overview (CLI + Control UI + config), see
/logging
OpenClaw has two log “surfaces”:
Console output
(what you see in the terminal / Debug UI).
File logs
(JSON lines) written by the gateway logger.
File-based logger
Default rolling log file is under
/tmp/openclaw/
(one file per day):
openclaw-YYYY-MM-DD.log
Date uses the gateway host’s local timezone.
The log file path and level can be configured via
~/.openclaw/openclaw.json
logging.file
logging.level
The file format is one JSON object per line.
The Control UI Logs tab tails this file via the gateway (
logs.tail
CLI can do the same:
Copy
openclaw
logs
--follow
Verbose vs. log levels
File logs
are controlled exclusively by
logging.level
--verbose
only affects
console verbosity
(and WS log style); it does
not
raise the file log level.
To capture verbose-only details in file logs, set
logging.level
debug
trace
Console capture
The CLI captures
console.log/info/warn/error/debug/trace
and writes them to file logs,
while still printing to stdout/stderr.
You can tune console verbosity independently via:
logging.consoleLevel
(default
info
logging.consoleStyle
pretty
compact
json
Tool summary redaction
Verbose tool summaries (e.g.
🛠️ Exec: ...
) can mask sensitive tokens before they hit the
console stream. This is
tools-only
and does not alter file logs.
logging.redactSensitive
off
tools
(default:
tools
logging.redactPatterns
: array of regex strings (overrides defaults)
Use raw regex strings (auto
), or
/pattern/flags
if you need custom flags.
Matches are masked by keeping the first 6 + last 4 chars (length &gt;= 18), otherwise
***
Defaults cover common key assignments, CLI flags, JSON fields, bearer headers, PEM blocks, and popular token prefixes.
Gateway WebSocket logs
The gateway prints WebSocket protocol logs in two modes:
Normal mode (no
--verbose
: only “interesting” RPC results are printed:
errors (
ok=false
slow calls (default threshold:
&gt;= 50ms
parse errors
Verbose mode (
--verbose
: prints all WS request/response traffic.
WS log style
openclaw gateway
supports a per-gateway style switch:
--ws-log auto
(default): normal mode is optimized; verbose mode uses compact output
--ws-log compact
: compact output (paired request/response) when verbose
--ws-log full
: full per-frame output when verbose
--compact
: alias for
--ws-log compact
Examples:
Copy
# optimized (only errors/slow)
openclaw
gateway
# show all WS traffic (paired)
openclaw
gateway
--verbose
--ws-log
compact
# show all WS traffic (full meta)
openclaw
gateway
--verbose
--ws-log
full
Console formatting (subsystem logging)
The console formatter is
TTY-aware
and prints consistent, prefixed lines.
Subsystem loggers keep output grouped and scannable.
Behavior:
Subsystem prefixes
on every line (e.g.
[gateway]
[canvas]
[tailscale]
Subsystem colors
(stable per subsystem) plus level coloring
Color when output is a TTY or the environment looks like a rich terminal
TERM
COLORTERM
TERM_PROGRAM
), respects
NO_COLOR
Shortened subsystem prefixes
: drops leading
gateway/
channels/
, keeps last 2 segments (e.g.
whatsapp/outbound
Sub-loggers by subsystem
(auto prefix + structured field
{ subsystem }
logRaw()
for QR/UX output (no prefix, no formatting)
Console styles
(e.g.
pretty | compact | json
Console log level
separate from file log level (file keeps full detail when
logging.level
is set to
debug
trace
WhatsApp message bodies
are logged at
debug
(use
--verbose
to see them)
This keeps existing file logs stable while making interactive output scannable.
Doctor
Gateway Lock

---
## Gateway > Multiple Gateways

[Source: https://docs.openclaw.ai/gateway/multiple-gateways]

Multiple Gateways - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Configuration and operations
Multiple Gateways
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
Gateway
Gateway Runbook
Configuration and operations
Configuration
Configuration Reference
Configuration Examples
Authentication
Trusted proxy auth
Health Checks
Heartbeat
Doctor
Logging
Gateway Lock
Background Exec and Process Tool
Multiple Gateways
Troubleshooting
Security and sandboxing
Protocols and APIs
Networking and discovery
Remote access
Remote Access
Remote Gateway Setup
Tailscale
Security
Formal Verification (Security Models)
Web interfaces
Web
Control UI
Dashboard
WebChat
TUI
Multiple Gateways (same host)
Isolation checklist (required)
Recommended: profiles (--profile)
Rescue-bot guide
How to install (rescue bot)
Port mapping (derived)
Browser/CDP notes (common footgun)
Manual env example
Quick checks
Configuration and operations
Multiple Gateways
Multiple Gateways (same host)
Most setups should use one Gateway because a single Gateway can handle multiple messaging connections and agents. If you need stronger isolation or redundancy (e.g., a rescue bot), run separate Gateways with isolated profiles/ports.
Isolation checklist (required)
OPENCLAW_CONFIG_PATH
— per-instance config file
OPENCLAW_STATE_DIR
— per-instance sessions, creds, caches
agents.defaults.workspace
— per-instance workspace root
gateway.port
(or
--port
) — unique per instance
Derived ports (browser/canvas) must not overlap
If these are shared, you will hit config races and port conflicts.
Recommended: profiles (
--profile
Profiles auto-scope
OPENCLAW_STATE_DIR
OPENCLAW_CONFIG_PATH
and suffix service names.
Copy
# main
openclaw
--profile
main
setup
openclaw
--profile
main
gateway
--port
18789
# rescue
openclaw
--profile
rescue
setup
openclaw
--profile
rescue
gateway
--port
19001
Per-profile services:
Copy
openclaw
--profile
main
gateway
install
openclaw
--profile
rescue
gateway
install
Rescue-bot guide
Run a second Gateway on the same host with its own:
profile/config
state dir
workspace
base port (plus derived ports)
This keeps the rescue bot isolated from the main bot so it can debug or apply config changes if the primary bot is down.
Port spacing: leave at least 20 ports between base ports so the derived browser/canvas/CDP ports never collide.
How to install (rescue bot)
Copy
# Main bot (existing or fresh, without --profile param)
# Runs on port 18789 + Chrome CDC/Canvas/... Ports
openclaw
onboard
openclaw
gateway
install
# Rescue bot (isolated profile + ports)
openclaw
--profile
rescue
onboard
# Notes:
# - workspace name will be postfixed with -rescue per default
# - Port should be at least 18789 + 20 Ports,
# better choose completely different base port, like 19789,
# - rest of the onboarding is the same as normal
# To install the service (if not happened automatically during onboarding)
openclaw
--profile
rescue
gateway
install
Port mapping (derived)
Base port =
gateway.port
(or
OPENCLAW_GATEWAY_PORT
--port
browser control service port = base + 2 (loopback only)
canvas host is served on the Gateway HTTP server (same port as
gateway.port
Browser profile CDP ports auto-allocate from
browser.controlPort + 9 .. + 108
If you override any of these in config or env, you must keep them unique per instance.
Browser/CDP notes (common footgun)
not
pin
browser.cdpUrl
to the same values on multiple instances.
Each instance needs its own browser control port and CDP range (derived from its gateway port).
If you need explicit CDP ports, set
browser.profiles.&lt;name&gt;.cdpPort
per instance.
Remote Chrome: use
browser.profiles.&lt;name&gt;.cdpUrl
(per profile, per instance).
Manual env example
Copy
OPENCLAW_CONFIG_PATH
~/.openclaw/main.json
OPENCLAW_STATE_DIR=~/.openclaw-main \
openclaw
gateway
--port
18789
OPENCLAW_CONFIG_PATH
~/.openclaw/rescue.json
OPENCLAW_STATE_DIR=~/.openclaw-rescue \
openclaw
gateway
--port
19001
Quick checks
Copy
openclaw
--profile
main
status
openclaw
--profile
rescue
status
openclaw
--profile
rescue
browser
status
Background Exec and Process Tool
Troubleshooting

---
## Gateway > Network Model

[Source: https://docs.openclaw.ai/gateway/network-model]

Network model - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Networking and discovery
Network model
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
Gateway
Gateway Runbook
Configuration and operations
Security and sandboxing
Protocols and APIs
Networking and discovery
Network model
Gateway-Owned Pairing
Discovery and Transports
Bonjour Discovery
Remote access
Remote Access
Remote Gateway Setup
Tailscale
Security
Formal Verification (Security Models)
Web interfaces
Web
Control UI
Dashboard
WebChat
TUI
Core rules
Networking and discovery
Network model
Most operations flow through the Gateway (
openclaw gateway
), a single long-running
process that owns channel connections and the WebSocket control plane.
Core rules
One Gateway per host is recommended. It is the only process allowed to own the WhatsApp Web session. For rescue bots or strict isolation, run multiple gateways with isolated profiles and ports. See
Multiple gateways
Loopback first: the Gateway WS defaults to
ws://127.0.0.1:18789
. The wizard generates a gateway token by default, even for loopback. For tailnet access, run
openclaw gateway --bind tailnet --token ...
because tokens are required for non-loopback binds.
Nodes connect to the Gateway WS over LAN, tailnet, or SSH as needed. The legacy TCP bridge is deprecated.
Canvas host is served by the Gateway HTTP server on the
same port
as the Gateway (default
18789
/__openclaw__/canvas/
/__openclaw__/a2ui/
When
gateway.auth
is configured and the Gateway binds beyond loopback, these routes are protected by Gateway auth (loopback requests are exempt). See
Gateway configuration
canvasHost
gateway
Remote use is typically SSH tunnel or tailnet VPN. See
Remote access
and
Discovery
Local Models
Gateway-Owned Pairing

---
## Gateway > Openai Http Api

[Source: https://docs.openclaw.ai/gateway/openai-http-api]

OpenAI Chat Completions - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Protocols and APIs
OpenAI Chat Completions
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
Gateway
Gateway Runbook
Configuration and operations
Security and sandboxing
Protocols and APIs
Gateway Protocol
Bridge Protocol
OpenAI Chat Completions
Tools Invoke API
CLI Backends
Local Models
Networking and discovery
Remote access
Remote Access
Remote Gateway Setup
Tailscale
Security
Formal Verification (Security Models)
Web interfaces
Web
Control UI
Dashboard
WebChat
TUI
OpenAI Chat Completions (HTTP)
Authentication
Choosing an agent
Enabling the endpoint
Disabling the endpoint
Session behavior
Streaming (SSE)
Examples
Protocols and APIs
OpenAI Chat Completions
OpenAI Chat Completions (HTTP)
OpenClaw’s Gateway can serve a small OpenAI-compatible Chat Completions endpoint.
This endpoint is
disabled by default
. Enable it in config first.
POST /v1/chat/completions
Same port as the Gateway (WS + HTTP multiplex):
http://&lt;gateway-host&gt;:&lt;port&gt;/v1/chat/completions
Under the hood, requests are executed as a normal Gateway agent run (same codepath as
openclaw agent
), so routing/permissions/config match your Gateway.
Authentication
Uses the Gateway auth configuration. Send a bearer token:
Authorization: Bearer &lt;token&gt;
Notes:
When
gateway.auth.mode=&quot;token&quot;
, use
gateway.auth.token
(or
OPENCLAW_GATEWAY_TOKEN
When
gateway.auth.mode=&quot;password&quot;
, use
gateway.auth.password
(or
OPENCLAW_GATEWAY_PASSWORD
gateway.auth.rateLimit
is configured and too many auth failures occur, the endpoint returns
429
with
Retry-After
Choosing an agent
No custom headers required: encode the agent id in the OpenAI
model
field:
model: &quot;openclaw:&lt;agentId&gt;&quot;
(example:
&quot;openclaw:main&quot;
&quot;openclaw:beta&quot;
model: &quot;agent:&lt;agentId&gt;&quot;
(alias)
Or target a specific OpenClaw agent by header:
x-openclaw-agent-id: &lt;agentId&gt;
(default:
main
Advanced:
x-openclaw-session-key: &lt;sessionKey&gt;
to fully control session routing.
Enabling the endpoint
Set
gateway.http.endpoints.chatCompletions.enabled
true
Copy
gateway
http
endpoints
chatCompletions
enabled
true
Disabling the endpoint
Set
gateway.http.endpoints.chatCompletions.enabled
false
Copy
gateway
http
endpoints
chatCompletions
enabled
false
Session behavior
By default the endpoint is
stateless per request
(a new session key is generated each call).
If the request includes an OpenAI
user
string, the Gateway derives a stable session key from it, so repeated calls can share an agent session.
Streaming (SSE)
Set
stream: true
to receive Server-Sent Events (SSE):
Content-Type: text/event-stream
Each event line is
data: &lt;json&gt;
Stream ends with
data: [DONE]
Examples
Non-streaming:
Copy
curl
-sS
http://127.0.0.1:18789/v1/chat/completions
&#x27;Authorization: Bearer YOUR_TOKEN&#x27;
&#x27;Content-Type: application/json&#x27;
&#x27;x-openclaw-agent-id: main&#x27;
&#x27;{
&quot;model&quot;: &quot;openclaw&quot;,
&quot;messages&quot;: [{&quot;role&quot;:&quot;user&quot;,&quot;content&quot;:&quot;hi&quot;}]
}&#x27;
Streaming:
Copy
curl
http://127.0.0.1:18789/v1/chat/completions
&#x27;Authorization: Bearer YOUR_TOKEN&#x27;
&#x27;Content-Type: application/json&#x27;
&#x27;x-openclaw-agent-id: main&#x27;
&#x27;{
&quot;model&quot;: &quot;openclaw&quot;,
&quot;stream&quot;: true,
&quot;messages&quot;: [{&quot;role&quot;:&quot;user&quot;,&quot;content&quot;:&quot;hi&quot;}]
}&#x27;
Bridge Protocol
Tools Invoke API

---
## Gateway > Pairing

[Source: https://docs.openclaw.ai/gateway/pairing]

Gateway-Owned Pairing - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Networking and discovery
Gateway-Owned Pairing
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
Gateway
Gateway Runbook
Configuration and operations
Security and sandboxing
Protocols and APIs
Networking and discovery
Network model
Gateway-Owned Pairing
Discovery and Transports
Bonjour Discovery
Remote access
Remote Access
Remote Gateway Setup
Tailscale
Security
Formal Verification (Security Models)
Web interfaces
Web
Control UI
Dashboard
WebChat
TUI
Gateway-owned pairing (Option B)
Concepts
How pairing works
CLI workflow (headless friendly)
API surface (gateway protocol)
Auto-approval (macOS app)
Storage (local, private)
Transport behavior
Networking and discovery
Gateway-Owned Pairing
Gateway-owned pairing (Option B)
In Gateway-owned pairing, the
Gateway
is the source of truth for which nodes
are allowed to join. UIs (macOS app, future clients) are just frontends that
approve or reject pending requests.
Important:
WS nodes use
device pairing
(role
node
) during
connect
node.pair.*
is a separate pairing store and does
not
gate the WS handshake.
Only clients that explicitly call
node.pair.*
use this flow.
Concepts
Pending request
: a node asked to join; requires approval.
Paired node
: approved node with an issued auth token.
Transport
: the Gateway WS endpoint forwards requests but does not decide
membership. (Legacy TCP bridge support is deprecated/removed.)
How pairing works
A node connects to the Gateway WS and requests pairing.
The Gateway stores a
pending request
and emits
node.pair.requested
You approve or reject the request (CLI or UI).
On approval, the Gateway issues a
new token
(tokens are rotated on re‑pair).
The node reconnects using the token and is now “paired”.
Pending requests expire automatically after
5 minutes
CLI workflow (headless friendly)
Copy
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
reject
&lt;
requestI
&gt;
openclaw
nodes
status
openclaw
nodes
rename
--node
&lt;
name
&gt;
--name
&quot;Living Room iPad&quot;
nodes status
shows paired/connected nodes and their capabilities.
API surface (gateway protocol)
Events:
node.pair.requested
— emitted when a new pending request is created.
node.pair.resolved
— emitted when a request is approved/rejected/expired.
Methods:
node.pair.request
— create or reuse a pending request.
node.pair.list
— list pending + paired nodes.
node.pair.approve
— approve a pending request (issues token).
node.pair.reject
— reject a pending request.
node.pair.verify
— verify
{ nodeId, token }
Notes:
node.pair.request
is idempotent per node: repeated calls return the same
pending request.
Approval
always
generates a fresh token; no token is ever returned from
node.pair.request
Requests may include
silent: true
as a hint for auto-approval flows.
Auto-approval (macOS app)
The macOS app can optionally attempt a
silent approval
when:
the request is marked
silent
, and
the app can verify an SSH connection to the gateway host using the same user.
If silent approval fails, it falls back to the normal “Approve/Reject” prompt.
Storage (local, private)
Pairing state is stored under the Gateway state directory (default
~/.openclaw
~/.openclaw/nodes/paired.json
~/.openclaw/nodes/pending.json
If you override
OPENCLAW_STATE_DIR
, the
nodes/
folder moves with it.
Security notes:
Tokens are secrets; treat
paired.json
as sensitive.
Rotating a token requires re-approval (or deleting the node entry).
Transport behavior
The transport is
stateless
; it does not store membership.
If the Gateway is offline or pairing is disabled, nodes cannot pair.
If the Gateway is in remote mode, pairing still happens against the remote Gateway’s store.
Network model
Discovery and Transports

---
## Gateway > Protocol

[Source: https://docs.openclaw.ai/gateway/protocol]

Gateway Protocol - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Protocols and APIs
Gateway Protocol
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
Gateway
Gateway Runbook
Configuration and operations
Security and sandboxing
Protocols and APIs
Gateway Protocol
Bridge Protocol
OpenAI Chat Completions
Tools Invoke API
CLI Backends
Local Models
Networking and discovery
Remote access
Remote Access
Remote Gateway Setup
Tailscale
Security
Formal Verification (Security Models)
Web interfaces
Web
Control UI
Dashboard
WebChat
TUI
Gateway protocol (WebSocket)
Transport
Handshake (connect)
Node example
Framing
Roles + scopes
Roles
Scopes (operator)
Caps/commands/permissions (node)
Presence
Node helper methods
Exec approvals
Versioning
Auth
Device identity + pairing
TLS + pinning
Scope
Protocols and APIs
Gateway Protocol
Gateway protocol (WebSocket)
The Gateway WS protocol is the
single control plane + node transport
for
OpenClaw. All clients (CLI, web UI, macOS app, iOS/Android nodes, headless
nodes) connect over WebSocket and declare their
role
scope
handshake time.
Transport
WebSocket, text frames with JSON payloads.
First frame
must
be a
connect
request.
Handshake (connect)
Gateway → Client (pre-connect challenge):
Copy
&quot;type&quot;
&quot;event&quot;
&quot;event&quot;
&quot;connect.challenge&quot;
&quot;payload&quot;
&quot;nonce&quot;
&quot;…&quot;
&quot;ts&quot;
1737264000000
Client → Gateway:
Copy
&quot;type&quot;
&quot;req&quot;
&quot;id&quot;
&quot;…&quot;
&quot;method&quot;
&quot;connect&quot;
&quot;params&quot;
&quot;minProtocol&quot;
&quot;maxProtocol&quot;
&quot;client&quot;
&quot;id&quot;
&quot;cli&quot;
&quot;version&quot;
&quot;1.2.3&quot;
&quot;platform&quot;
&quot;macos&quot;
&quot;mode&quot;
&quot;operator&quot;
&quot;role&quot;
&quot;operator&quot;
&quot;scopes&quot;
&quot;operator.read&quot;
&quot;operator.write&quot;
&quot;caps&quot;
&quot;commands&quot;
&quot;permissions&quot;
&quot;auth&quot;
&quot;token&quot;
&quot;…&quot;
&quot;locale&quot;
&quot;en-US&quot;
&quot;userAgent&quot;
&quot;openclaw-cli/1.2.3&quot;
&quot;device&quot;
&quot;id&quot;
&quot;device_fingerprint&quot;
&quot;publicKey&quot;
&quot;…&quot;
&quot;signature&quot;
&quot;…&quot;
&quot;signedAt&quot;
1737264000000
&quot;nonce&quot;
&quot;…&quot;
Gateway → Client:
Copy
&quot;type&quot;
&quot;res&quot;
&quot;id&quot;
&quot;…&quot;
&quot;ok&quot;
true
&quot;payload&quot;
&quot;type&quot;
&quot;hello-ok&quot;
&quot;protocol&quot;
&quot;policy&quot;
&quot;tickIntervalMs&quot;
15000
} }
When a device token is issued,
hello-ok
also includes:
Copy
&quot;auth&quot;
&quot;deviceToken&quot;
&quot;…&quot;
&quot;role&quot;
&quot;operator&quot;
&quot;scopes&quot;
&quot;operator.read&quot;
&quot;operator.write&quot;
Node example
Copy
&quot;type&quot;
&quot;req&quot;
&quot;id&quot;
&quot;…&quot;
&quot;method&quot;
&quot;connect&quot;
&quot;params&quot;
&quot;minProtocol&quot;
&quot;maxProtocol&quot;
&quot;client&quot;
&quot;id&quot;
&quot;ios-node&quot;
&quot;version&quot;
&quot;1.2.3&quot;
&quot;platform&quot;
&quot;ios&quot;
&quot;mode&quot;
&quot;node&quot;
&quot;role&quot;
&quot;node&quot;
&quot;scopes&quot;
&quot;caps&quot;
&quot;camera&quot;
&quot;canvas&quot;
&quot;screen&quot;
&quot;location&quot;
&quot;voice&quot;
&quot;commands&quot;
&quot;camera.snap&quot;
&quot;canvas.navigate&quot;
&quot;screen.record&quot;
&quot;location.get&quot;
&quot;permissions&quot;
&quot;camera.capture&quot;
true
&quot;screen.record&quot;
false
&quot;auth&quot;
&quot;token&quot;
&quot;…&quot;
&quot;locale&quot;
&quot;en-US&quot;
&quot;userAgent&quot;
&quot;openclaw-ios/1.2.3&quot;
&quot;device&quot;
&quot;id&quot;
&quot;device_fingerprint&quot;
&quot;publicKey&quot;
&quot;…&quot;
&quot;signature&quot;
&quot;…&quot;
&quot;signedAt&quot;
1737264000000
&quot;nonce&quot;
&quot;…&quot;
Framing
Request
{type:&quot;req&quot;, id, method, params}
Response
{type:&quot;res&quot;, id, ok, payload|error}
Event
{type:&quot;event&quot;, event, payload, seq?, stateVersion?}
Side-effecting methods require
idempotency keys
(see schema).
Roles + scopes
Roles
operator
= control plane client (CLI/UI/automation).
node
= capability host (camera/screen/canvas/system.run).
Scopes (operator)
Common scopes:
operator.read
operator.write
operator.admin
operator.approvals
operator.pairing
Caps/commands/permissions (node)
Nodes declare capability claims at connect time:
caps
: high-level capability categories.
commands
: command allowlist for invoke.
permissions
: granular toggles (e.g.
screen.record
camera.capture
The Gateway treats these as
claims
and enforces server-side allowlists.
Presence
system-presence
returns entries keyed by device identity.
Presence entries include
deviceId
roles
, and
scopes
so UIs can show a single row per device
even when it connects as both
operator
and
node
Node helper methods
Nodes may call
skills.bins
to fetch the current list of skill executables
for auto-allow checks.
Exec approvals
When an exec request needs approval, the gateway broadcasts
exec.approval.requested
Operator clients resolve by calling
exec.approval.resolve
(requires
operator.approvals
scope).
Versioning
PROTOCOL_VERSION
lives in
src/gateway/protocol/schema.ts
Clients send
minProtocol
maxProtocol
; the server rejects mismatches.
Schemas + models are generated from TypeBox definitions:
pnpm protocol:gen
pnpm protocol:gen:swift
pnpm protocol:check
Auth
OPENCLAW_GATEWAY_TOKEN
(or
--token
) is set,
connect.params.auth.token
must match or the socket is closed.
After pairing, the Gateway issues a
device token
scoped to the connection
role + scopes. It is returned in
hello-ok.auth.deviceToken
and should be
persisted by the client for future connects.
Device tokens can be rotated/revoked via
device.token.rotate
and
device.token.revoke
(requires
operator.pairing
scope).
Device identity + pairing
Nodes should include a stable device identity (
device.id
) derived from a
keypair fingerprint.
Gateways issue tokens per device + role.
Pairing approvals are required for new device IDs unless local auto-approval
is enabled.
Local
connects include loopback and the gateway host’s own tailnet address
(so same‑host tailnet binds can still auto‑approve).
All WS clients must include
device
identity during
connect
(operator + node).
Control UI can omit it
only
when
gateway.controlUi.allowInsecureAuth
is enabled
(or
gateway.controlUi.dangerouslyDisableDeviceAuth
for break-glass use).
Non-local connections must sign the server-provided
connect.challenge
nonce.
TLS + pinning
TLS is supported for WS connections.
Clients may optionally pin the gateway cert fingerprint (see
gateway.tls
config plus
gateway.remote.tlsFingerprint
or CLI
--tls-fingerprint
Scope
This protocol exposes the
full gateway API
(status, channels, models, chat,
agent, sessions, nodes, approvals, etc.). The exact surface is defined by the
TypeBox schemas in
src/gateway/protocol/schema.ts
Sandbox vs Tool Policy vs Elevated
Bridge Protocol

---
## Gateway > Remote Gateway Readme

[Source: https://docs.openclaw.ai/gateway/remote-gateway-readme]

Remote Gateway Setup - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Remote access
Remote Gateway Setup
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
Gateway
Gateway Runbook
Configuration and operations
Security and sandboxing
Protocols and APIs
Networking and discovery
Remote access
Remote Access
Remote Gateway Setup
Tailscale
Security
Formal Verification (Security Models)
Web interfaces
Web
Control UI
Dashboard
WebChat
TUI
Running OpenClaw.app with a Remote Gateway
Overview
Quick Setup
Step 1: Add SSH Config
Step 2: Copy SSH Key
Step 3: Set Gateway Token
Step 4: Start SSH Tunnel
Step 5: Restart OpenClaw.app
Auto-Start Tunnel on Login
Create the PLIST file
Load the Launch Agent
Troubleshooting
How It Works
Remote access
Remote Gateway Setup
Running OpenClaw.app with a Remote Gateway
OpenClaw.app uses SSH tunneling to connect to a remote gateway. This guide shows you how to set it up.
Overview
Quick Setup
Step 1: Add SSH Config
Edit
~/.ssh/config
and add:
Copy
Host remote-gateway
HostName &lt;REMOTE_IP&gt; # e.g., 172.27.187.184
User &lt;REMOTE_USER&gt; # e.g., jefferson
LocalForward 18789 127.0.0.1:18789
IdentityFile ~/.ssh/id_rsa
Replace
&lt;REMOTE_IP&gt;
and
&lt;REMOTE_USER&gt;
with your values.
Step 2: Copy SSH Key
Copy your public key to the remote machine (enter password once):
Copy
ssh-copy-id
~/.ssh/id_rsa
&lt;
REMOTE_USE
&gt;
&lt;
REMOTE_I
&gt;
Step 3: Set Gateway Token
Copy
launchctl
setenv
OPENCLAW_GATEWAY_TOKEN
&quot;&lt;your-token&gt;&quot;
Step 4: Start SSH Tunnel
Copy
ssh
remote-gateway
&amp;
Step 5: Restart OpenClaw.app
Copy
# Quit OpenClaw.app (⌘Q), then reopen:
open
/path/to/OpenClaw.app
The app will now connect to the remote gateway through the SSH tunnel.
Auto-Start Tunnel on Login
To have the SSH tunnel start automatically when you log in, create a Launch Agent.
Create the PLIST file
Save this as
~/Library/LaunchAgents/bot.molt.ssh-tunnel.plist
Copy
&lt;?
xml
version
&quot;1.0&quot;
encoding
&quot;UTF-8&quot;
?&gt;
&lt;!
DOCTYPE
plist PUBLIC &quot;-//Apple//DTD PLIST 1.0//EN&quot; &quot;http://www.apple.com/DTDs/PropertyList-1.0.dtd&quot;&gt;
&lt;
plist
version
&quot;1.0&quot;
&gt;
&lt;
dict
&gt;
&lt;
key
&gt;Label&lt;/
key
&gt;
&lt;
string
&gt;bot.molt.ssh-tunnel&lt;/
string
&gt;
&lt;
key
&gt;ProgramArguments&lt;/
key
&gt;
&lt;
array
&gt;
&lt;
string
&gt;/usr/bin/ssh&lt;/
string
&gt;
&lt;
string
&gt;-N&lt;/
string
&gt;
&lt;
string
&gt;remote-gateway&lt;/
string
&gt;
&lt;/
array
&gt;
&lt;
key
&gt;KeepAlive&lt;/
key
&gt;
&lt;
true
/&gt;
&lt;
key
&gt;RunAtLoad&lt;/
key
&gt;
&lt;
true
/&gt;
&lt;/
dict
&gt;
&lt;/
plist
&gt;
Load the Launch Agent
Copy
launchctl
bootstrap
gui/
$UID
~/Library/LaunchAgents/bot.molt.ssh-tunnel.plist
The tunnel will now:
Start automatically when you log in
Restart if it crashes
Keep running in the background
Legacy note: remove any leftover
com.openclaw.ssh-tunnel
LaunchAgent if present.
Troubleshooting
Check if tunnel is running:
Copy
aux
grep
&quot;ssh -N remote-gateway&quot;
grep
grep
lsof
:18789
Restart the tunnel:
Copy
launchctl
kickstart
gui/
$UID
/bot.molt.ssh-tunnel
Stop the tunnel:
Copy
launchctl
bootout
gui/
$UID
/bot.molt.ssh-tunnel
How It Works
Component
What It Does
LocalForward 18789 127.0.0.1:18789
Forwards local port 18789 to remote port 18789
ssh -N
SSH without executing remote commands (just port forwarding)
KeepAlive
Automatically restarts tunnel if it crashes
RunAtLoad
Starts tunnel when the agent loads
OpenClaw.app connects to
ws://127.0.0.1:18789
on your client machine. The SSH tunnel forwards that connection to port 18789 on the remote machine where the Gateway is running.
Remote Access
Tailscale

---
## Gateway > Remote

[Source: https://docs.openclaw.ai/gateway/remote]

Remote Access - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Remote access
Remote Access
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
Gateway
Gateway Runbook
Configuration and operations
Security and sandboxing
Protocols and APIs
Networking and discovery
Remote access
Remote Access
Remote Gateway Setup
Tailscale
Security
Formal Verification (Security Models)
Web interfaces
Web
Control UI
Dashboard
WebChat
TUI
Remote access (SSH, tunnels, and tailnets)
The core idea
Common VPN/tailnet setups (where the agent lives)
1) Always-on Gateway in your tailnet (VPS or home server)
2) Home desktop runs the Gateway, laptop is remote control
3) Laptop runs the Gateway, remote access from other machines
Command flow (what runs where)
SSH tunnel (CLI + tools)
CLI remote defaults
Chat UI over SSH
macOS app “Remote over SSH”
Security rules (remote/VPN)
Remote access
Remote Access
Remote access (SSH, tunnels, and tailnets)
This repo supports “remote over SSH” by keeping a single Gateway (the master) running on a dedicated host (desktop/server) and connecting clients to it.
For
operators (you / the macOS app)
: SSH tunneling is the universal fallback.
For
nodes (iOS/Android and future devices)
: connect to the Gateway
WebSocket
(LAN/tailnet or SSH tunnel as needed).
The core idea
The Gateway WebSocket binds to
loopback
on your configured port (defaults to 18789).
For remote use, you forward that loopback port over SSH (or use a tailnet/VPN and tunnel less).
Common VPN/tailnet setups (where the agent lives)
Think of the
Gateway host
as “where the agent lives.” It owns sessions, auth profiles, channels, and state.
Your laptop/desktop (and nodes) connect to that host.
1) Always-on Gateway in your tailnet (VPS or home server)
Run the Gateway on a persistent host and reach it via
Tailscale
or SSH.
Best UX:
keep
gateway.bind: &quot;loopback&quot;
and use
Tailscale Serve
for the Control UI.
Fallback:
keep loopback + SSH tunnel from any machine that needs access.
Examples:
exe.dev
(easy VM) or
Hetzner
(production VPS).
This is ideal when your laptop sleeps often but you want the agent always-on.
2) Home desktop runs the Gateway, laptop is remote control
The laptop does
not
run the agent. It connects remotely:
Use the macOS app’s
Remote over SSH
mode (Settings → General → “OpenClaw runs”).
The app opens and manages the tunnel, so WebChat + health checks “just work.”
Runbook:
macOS remote access
3) Laptop runs the Gateway, remote access from other machines
Keep the Gateway local but expose it safely:
SSH tunnel to the laptop from other machines, or
Tailscale Serve the Control UI and keep the Gateway loopback-only.
Guide:
Tailscale
and
Web overview
Command flow (what runs where)
One gateway service owns state + channels. Nodes are peripherals.
Flow example (Telegram → node):
Telegram message arrives at the
Gateway
Gateway runs the
agent
and decides whether to call a node tool.
Gateway calls the
node
over the Gateway WebSocket (
node.*
RPC).
Node returns the result; Gateway replies back out to Telegram.
Notes:
Nodes do not run the gateway service.
Only one gateway should run per host unless you intentionally run isolated profiles (see
Multiple gateways
macOS app “node mode” is just a node client over the Gateway WebSocket.
SSH tunnel (CLI + tools)
Create a local tunnel to the remote Gateway WS:
Copy
ssh
18789:127.0.0.1:18789
user@host
With the tunnel up:
openclaw health
and
openclaw status --deep
now reach the remote gateway via
ws://127.0.0.1:18789
openclaw gateway {status,health,send,agent,call}
can also target the forwarded URL via
--url
when needed.
Note: replace
18789
with your configured
gateway.port
(or
--port
OPENCLAW_GATEWAY_PORT
Note: when you pass
--url
, the CLI does not fall back to config or environment credentials.
Include
--token
--password
explicitly. Missing explicit credentials is an error.
CLI remote defaults
You can persist a remote target so CLI commands use it by default:
Copy
gateway
mode
&quot;remote&quot;
remote
url
&quot;ws://127.0.0.1:18789&quot;
token
&quot;your-token&quot;
When the gateway is loopback-only, keep the URL at
ws://127.0.0.1:18789
and open the SSH tunnel first.
Chat UI over SSH
WebChat no longer uses a separate HTTP port. The SwiftUI chat UI connects directly to the Gateway WebSocket.
Forward
18789
over SSH (see above), then connect clients to
ws://127.0.0.1:18789
On macOS, prefer the app’s “Remote over SSH” mode, which manages the tunnel automatically.
macOS app “Remote over SSH”
The macOS menu bar app can drive the same setup end-to-end (remote status checks, WebChat, and Voice Wake forwarding).
Runbook:
macOS remote access
Security rules (remote/VPN)
Short version:
keep the Gateway loopback-only
unless you’re sure you need a bind.
Loopback + SSH/Tailscale Serve
is the safest default (no public exposure).
Non-loopback binds
lan
tailnet
custom
, or
auto
when loopback is unavailable) must use auth tokens/passwords.
gateway.remote.token
only
for remote CLI calls — it does
not
enable local auth.
gateway.remote.tlsFingerprint
pins the remote TLS cert when using
wss://
Tailscale Serve
can authenticate via identity headers when
gateway.auth.allowTailscale: true
Set it to
false
if you want tokens/passwords instead.
Treat browser control like operator access: tailnet-only + deliberate node pairing.
Deep dive:
Security
Bonjour Discovery
Remote Gateway Setup

---
## Gateway > Sandbox Vs Tool Policy Vs Elevated

[Source: https://docs.openclaw.ai/gateway/sandbox-vs-tool-policy-vs-elevated]

Sandbox vs Tool Policy vs Elevated - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Security and sandboxing
Sandbox vs Tool Policy vs Elevated
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
Gateway
Gateway Runbook
Configuration and operations
Security and sandboxing
Security
Sandboxing
Sandbox vs Tool Policy vs Elevated
Protocols and APIs
Networking and discovery
Remote access
Remote Access
Remote Gateway Setup
Tailscale
Security
Formal Verification (Security Models)
Web interfaces
Web
Control UI
Dashboard
WebChat
TUI
Sandbox vs Tool Policy vs Elevated
Quick debug
Sandbox: where tools run
Bind mounts (security quick check)
Tool policy: which tools exist/are callable
Tool groups (shorthands)
Elevated: exec-only “run on host”
Common “sandbox jail” fixes
“Tool X blocked by sandbox tool policy”
“I thought this was main, why is it sandboxed?”
Security and sandboxing
Sandbox vs Tool Policy vs Elevated
Sandbox vs Tool Policy vs Elevated
OpenClaw has three related (but different) controls:
Sandbox
agents.defaults.sandbox.*
agents.list[].sandbox.*
) decides
where tools run
(Docker vs host).
Tool policy
tools.*
tools.sandbox.tools.*
agents.list[].tools.*
) decides
which tools are available/allowed
Elevated
tools.elevated.*
agents.list[].tools.elevated.*
) is an
exec-only escape hatch
to run on the host when you’re sandboxed.
Quick debug
Use the inspector to see what OpenClaw is
actually
doing:
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
It prints:
effective sandbox mode/scope/workspace access
whether the session is currently sandboxed (main vs non-main)
effective sandbox tool allow/deny (and whether it came from agent/global/default)
elevated gates and fix-it key paths
Sandbox: where tools run
Sandboxing is controlled by
agents.defaults.sandbox.mode
&quot;off&quot;
: everything runs on the host.
&quot;non-main&quot;
: only non-main sessions are sandboxed (common “surprise” for groups/channels).
&quot;all&quot;
: everything is sandboxed.
See
Sandboxing
for the full matrix (scope, workspace mounts, images).
Bind mounts (security quick check)
docker.binds
pierces
the sandbox filesystem: whatever you mount is visible inside the container with the mode you set (
:ro
:rw
Default is read-write if you omit the mode; prefer
:ro
for source/secrets.
scope: &quot;shared&quot;
ignores per-agent binds (only global binds apply).
Binding
/var/run/docker.sock
effectively hands host control to the sandbox; only do this intentionally.
Workspace access (
workspaceAccess: &quot;ro&quot;
&quot;rw&quot;
) is independent of bind modes.
Tool policy: which tools exist/are callable
Two layers matter:
Tool profile
tools.profile
and
agents.list[].tools.profile
(base allowlist)
Provider tool profile
tools.byProvider[provider].profile
and
agents.list[].tools.byProvider[provider].profile
Global/per-agent tool policy
tools.allow
tools.deny
and
agents.list[].tools.allow
agents.list[].tools.deny
Provider tool policy
tools.byProvider[provider].allow/deny
and
agents.list[].tools.byProvider[provider].allow/deny
Sandbox tool policy
(only applies when sandboxed):
tools.sandbox.tools.allow
tools.sandbox.tools.deny
and
agents.list[].tools.sandbox.tools.*
Rules of thumb:
deny
always wins.
allow
is non-empty, everything else is treated as blocked.
Tool policy is the hard stop:
/exec
cannot override a denied
exec
tool.
/exec
only changes session defaults for authorized senders; it does not grant tool access.
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
entries that expand to multiple tools:
Copy
tools
sandbox
tools
allow
&quot;group:runtime&quot;
&quot;group:fs&quot;
&quot;group:sessions&quot;
&quot;group:memory&quot;
Available groups:
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
Elevated: exec-only “run on host”
Elevated does
not
grant extra tools; it only affects
exec
If you’re sandboxed,
/elevated on
(or
exec
with
elevated: true
) runs on the host (approvals may still apply).
Use
/elevated full
to skip exec approvals for the session.
If you’re already running direct, elevated is effectively a no-op (still gated).
Elevated is
not
skill-scoped and does
not
override tool allow/deny.
/exec
is separate from elevated. It only adjusts per-session exec defaults for authorized senders.
Gates:
Enablement:
tools.elevated.enabled
(and optionally
agents.list[].tools.elevated.enabled
Sender allowlists:
tools.elevated.allowFrom.&lt;provider&gt;
(and optionally
agents.list[].tools.elevated.allowFrom.&lt;provider&gt;
See
Elevated Mode
Common “sandbox jail” fixes
“Tool X blocked by sandbox tool policy”
Fix-it keys (pick one):
Disable sandbox:
agents.defaults.sandbox.mode=off
(or per-agent
agents.list[].sandbox.mode=off
Allow the tool inside sandbox:
remove it from
tools.sandbox.tools.deny
(or per-agent
agents.list[].tools.sandbox.tools.deny
or add it to
tools.sandbox.tools.allow
(or per-agent allow)
“I thought this was main, why is it sandboxed?”
&quot;non-main&quot;
mode, group/channel keys are
not
main. Use the main session key (shown by
sandbox explain
) or switch mode to
&quot;off&quot;
Sandboxing
Gateway Protocol

---
## Gateway > Sandboxing

[Source: https://docs.openclaw.ai/gateway/sandboxing]

Sandboxing - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Security and sandboxing
Sandboxing
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
Gateway
Gateway Runbook
Configuration and operations
Security and sandboxing
Security
Sandboxing
Sandbox vs Tool Policy vs Elevated
Protocols and APIs
Networking and discovery
Remote access
Remote Access
Remote Gateway Setup
Tailscale
Security
Formal Verification (Security Models)
Web interfaces
Web
Control UI
Dashboard
WebChat
TUI
Sandboxing
What gets sandboxed
Modes
Scope
Workspace access
Custom bind mounts
Images + setup
setupCommand (one-time container setup)
Tool policy + escape hatches
Multi-agent overrides
Minimal enable example
Related docs
Security and sandboxing
Sandboxing
Sandboxing
OpenClaw can run
tools inside Docker containers
to reduce blast radius.
This is
optional
and controlled by configuration (
agents.defaults.sandbox
agents.list[].sandbox
). If sandboxing is off, tools run on the host.
The Gateway stays on the host; tool execution runs in an isolated sandbox
when enabled.
This is not a perfect security boundary, but it materially limits filesystem
and process access when the model does something dumb.
What gets sandboxed
Tool execution (
exec
read
write
edit
apply_patch
process
, etc.).
Optional sandboxed browser (
agents.defaults.sandbox.browser
By default, the sandbox browser auto-starts (ensures CDP is reachable) when the browser tool needs it.
Configure via
agents.defaults.sandbox.browser.autoStart
and
agents.defaults.sandbox.browser.autoStartTimeoutMs
agents.defaults.sandbox.browser.allowHostControl
lets sandboxed sessions target the host browser explicitly.
Optional allowlists gate
target: &quot;custom&quot;
allowedControlUrls
allowedControlHosts
allowedControlPorts
Not sandboxed:
The Gateway process itself.
Any tool explicitly allowed to run on the host (e.g.
tools.elevated
Elevated exec runs on the host and bypasses sandboxing.
If sandboxing is off,
tools.elevated
does not change execution (already on host). See
Elevated Mode
Modes
agents.defaults.sandbox.mode
controls
when
sandboxing is used:
&quot;off&quot;
: no sandboxing.
&quot;non-main&quot;
: sandbox only
non-main
sessions (default if you want normal chats on host).
&quot;all&quot;
: every session runs in a sandbox.
Note:
&quot;non-main&quot;
is based on
session.mainKey
(default
&quot;main&quot;
), not agent id.
Group/channel sessions use their own keys, so they count as non-main and will be sandboxed.
Scope
agents.defaults.sandbox.scope
controls
how many containers
are created:
&quot;session&quot;
(default): one container per session.
&quot;agent&quot;
: one container per agent.
&quot;shared&quot;
: one container shared by all sandboxed sessions.
Workspace access
agents.defaults.sandbox.workspaceAccess
controls
what the sandbox can see
&quot;none&quot;
(default): tools see a sandbox workspace under
~/.openclaw/sandboxes
&quot;ro&quot;
: mounts the agent workspace read-only at
/agent
(disables
write
edit
apply_patch
&quot;rw&quot;
: mounts the agent workspace read/write at
/workspace
Inbound media is copied into the active sandbox workspace (
media/inbound/*
Skills note: the
read
tool is sandbox-rooted. With
workspaceAccess: &quot;none&quot;
OpenClaw mirrors eligible skills into the sandbox workspace (
.../skills
) so
they can be read. With
&quot;rw&quot;
, workspace skills are readable from
/workspace/skills
Custom bind mounts
agents.defaults.sandbox.docker.binds
mounts additional host directories into the container.
Format:
host:container:mode
(e.g.,
&quot;/home/user/source:/source:rw&quot;
Global and per-agent binds are
merged
(not replaced). Under
scope: &quot;shared&quot;
, per-agent binds are ignored.
agents.defaults.sandbox.browser.binds
mounts additional host directories into the
sandbox browser
container only.
When set (including
), it replaces
agents.defaults.sandbox.docker.binds
for the browser container.
When omitted, the browser container falls back to
agents.defaults.sandbox.docker.binds
(backwards compatible).
Example (read-only source + an extra data directory):
Copy
agents
defaults
sandbox
docker
binds
&quot;/home/user/source:/source:ro&quot;
&quot;/var/data/myapp:/data:ro&quot;
list
&quot;build&quot;
sandbox
docker
binds
&quot;/mnt/cache:/cache:rw&quot;
Security notes:
Binds bypass the sandbox filesystem: they expose host paths with whatever mode you set (
:ro
:rw
OpenClaw blocks dangerous bind sources (for example:
docker.sock
/etc
/proc
/sys
/dev
, and parent mounts that would expose them).
Sensitive mounts (secrets, SSH keys, service credentials) should be
:ro
unless absolutely required.
Combine with
workspaceAccess: &quot;ro&quot;
if you only need read access to the workspace; bind modes stay independent.
See
Sandbox vs Tool Policy vs Elevated
for how binds interact with tool policy and elevated exec.
Images + setup
Default image:
openclaw-sandbox:bookworm-slim
Build it once:
Copy
scripts/sandbox-setup.sh
Note: the default image does
not
include Node. If a skill needs Node (or
other runtimes), either bake a custom image or install via
sandbox.docker.setupCommand
(requires network egress + writable root +
root user).
Sandboxed browser image:
Copy
scripts/sandbox-browser-setup.sh
By default, sandbox containers run with
no network
Override with
agents.defaults.sandbox.docker.network
Docker installs and the containerized gateway live here:
Docker
setupCommand (one-time container setup)
setupCommand
runs
once
after the sandbox container is created (not on every run).
It executes inside the container via
sh -lc
Paths:
Global:
agents.defaults.sandbox.docker.setupCommand
Per-agent:
agents.list[].sandbox.docker.setupCommand
Common pitfalls:
Default
docker.network
&quot;none&quot;
(no egress), so package installs will fail.
readOnlyRoot: true
prevents writes; set
readOnlyRoot: false
or bake a custom image.
user
must be root for package installs (omit
user
or set
user: &quot;0:0&quot;
Sandbox exec does
not
inherit host
process.env
. Use
agents.defaults.sandbox.docker.env
(or a custom image) for skill API keys.
Tool policy + escape hatches
Tool allow/deny policies still apply before sandbox rules. If a tool is denied
globally or per-agent, sandboxing doesn’t bring it back.
tools.elevated
is an explicit escape hatch that runs
exec
on the host.
/exec
directives only apply for authorized senders and persist per session; to hard-disable
exec
, use tool policy deny (see
Sandbox vs Tool Policy vs Elevated
Debugging:
Use
openclaw sandbox explain
to inspect effective sandbox mode, tool policy, and fix-it config keys.
See
Sandbox vs Tool Policy vs Elevated
for the “why is this blocked?” mental model.
Keep it locked down.
Multi-agent overrides
Each agent can override sandbox + tools:
agents.list[].sandbox
and
agents.list[].tools
(plus
agents.list[].tools.sandbox.tools
for sandbox tool policy).
See
Multi-Agent Sandbox &amp; Tools
for precedence.
Minimal enable example
Copy
agents
defaults
sandbox
mode
&quot;non-main&quot;
scope
&quot;session&quot;
workspaceAccess
&quot;none&quot;
Related docs
Sandbox Configuration
Multi-Agent Sandbox &amp; Tools
Security
Security
Sandbox vs Tool Policy vs Elevated

---
## Gateway > Security

[Source: https://docs.openclaw.ai/gateway/security]

# OpenClaw Security Documentation Summary

## Core Security Model

OpenClaw operates under a **personal assistant trust model**, not multi-tenant isolation. The documentation states: *"one trusted operator boundary per gateway (single-user/personal assistant model)"* rather than hostile multi-user separation.

Key distinction: *"If you need mixed-trust or adversarial-user operation, split trust boundaries (separate gateway + credentials, ideally separate OS users/hosts)."*

## Quick Security Audit

Run regularly to identify configuration issues:

```bash
openclaw security audit
openclaw security audit --deep
openclaw security audit --fix
```

This flags common vulnerabilities including authentication exposure, elevated tool allowlists, and filesystem permission problems.

## Hardened 60-Second Baseline

Essential starting configuration:

```json5
{
  gateway: {
    mode: "local",
    bind: "loopback",
    auth: { mode: "token", token: "replace-with-long-random-token" },
  },
  tools: {
    profile: "messaging",
    deny: ["group:automation", "group:runtime", "group:fs"],
    exec: { security: "deny", ask: "always" },
    elevated: { enabled: false },
  },
  channels: {
    whatsapp: { dmPolicy: "pairing", groups: { "*": { requireMention: true } } },
  },
}
```

## Critical Trust Boundaries

| Control | Purpose | Common Misunderstanding |
|---------|---------|------------------------|
| `gateway.auth` | Authenticates callers | Not per-message signatures |
| `sessionKey` | Routes context/sessions | Not user authorization |
| Prompt guardrails | Reduce model abuse | Prompt injection alone isn't auth bypass |
| Node pairing | Remote device execution | Operator-level access, not untrusted |

## Not Vulnerabilities (By Design)

The documentation explicitly excludes from security considerations:
- Prompt injection without policy/auth bypass
- Claims assuming hostile multi-tenant operation on shared hosts
- IDOR findings treating `sessionKey` as auth tokens
- Localhost-only deployment security findings

## DM Access Model

Three strategies for managing direct messages:

- **Pairing** (default): Unknown senders receive codes; messages ignored until approved
- **Allowlist**: Block unknown senders entirely
- **Open**: Allow anyone; requires explicit channel allowlist including `"*"`

Activate secure DM mode: `session.dmScope: "per-channel-peer"` prevents cross-user context leakage.

## Credential Storage Locations

Sensitive data stored under `~/.openclaw/credentials/`:

- WhatsApp credentials: `whatsapp/<accountId>/creds.json`
- Channel allowlists: `<channel>-allowFrom.json`
- Model auth profiles: `agents/<agentId>/agent/auth-profiles.json`
- Legacy OAuth: `oauth.json`

Session transcripts live in `agents/<agentId>/sessions/*.jsonl`—treat disk access as your trust boundary.

## High-Risk Security Findings

Priority remediation order from `openclaw security audit`:

1. **Open groups + enabled tools**: Lock down DMs/groups first (pairing/allowlists)
2. **Public network exposure**: Fix missing authentication immediately
3. **Browser control remote exposure**: Treat like operator access
4. **File permissions**: Ensure state/config aren't group/world-readable
5. **Plugin/extension oversight**: Only load explicitly trusted code
6. **Model selection**: Prefer modern, hardened models for tool-enabled bots

## Deployment Assumptions

The security model requires:
- *"If someone can modify Gateway host state/config (`~/.openclaw`), treat them as a trusted operator"*
- One OS user per machine for multi-user scenarios
- Separate gateways for adversarial trust boundaries

Config changes made by authenticated operators are trusted control-plane actions, not per-user tenant operations.

## Prompt Injection & Model Strength

Risk factors extend beyond sender identity:
- Untrusted content (web results, attachments, pasted logs) carries adversarial instructions
- Smaller models more susceptible to instruction hijacking
- Recommendation: *"Use the latest generation, best-tier model for any bot that can run tools"*

Mitigation: read-only reader agent → summary → main agent workflow.

## Sandboxing & Tool Policy

Two complementary approaches:

- **Full Gateway containerization**: Run entire Gateway in Docker
- **Tool sandboxing**: `agents.defaults.sandbox` isolates tool execution with Docker

Configure workspace access:
- `workspaceAccess: "none"` (default): sandbox workspace only
- `workspaceAccess: "ro"`: mount agent workspace read-only
- `workspaceAccess: "rw"`: full read/write access

## Browser Control Risks

*"If that browser profile already contains logged-in sessions, the model can access those accounts and data."*

Hardening measures:
- Dedicated agent profile (not personal daily-driver)
- Keep Gateway/node hosts tailnet-only
- Disable browser sync/password managers in agent profile
- SSRF policy: set `dangerouslyAllowPrivateNetwork: false` for strict validation

## Reverse Proxy Configuration

When running behind proxies:

```yaml
gateway:
  trustedProxies:
    - "127.0.0.1"
  allowRealIpFallback: false
  auth:
    mode: password
```

Critical: Proxy must **overwrite** `X-Forwarded-For` (not append) to prevent IP spoofing.

## Incident Response

**Containment steps:**
1. Stop the Gateway process
2. Set `gateway.bind: "loopback"` or disable Tailscale exposure
3. Switch risky channels to `dmPolicy: "disabled"` temporarily

**Rotation:**
1. Rotate `gateway.auth.token` and restart
2. Rotate remote client credentials
3. Rotate provider credentials (WhatsApp, Slack, API keys)

**Audit:**
- Check logs: `/tmp/openclaw/openclaw-YYYY-MM-DD.log`
- Review transcripts: `~/.openclaw/agents/<agentId>/sessions/`
- Rerun `openclaw security audit --deep`

## Multi-Agent Access Profiles

Example read-only agent:

```json5
{
  agents: {
    list: [
      {
        id: "family",
        sandbox: {
          mode: "all",
          workspaceAccess: "ro",
        },
        tools: {
          allow: ["read"],
          deny: ["write", "exec", "browser"],
        },
      },
    ],
  },
}
```

## Secrets Management

Keep these practices:
- `~/.openclaw/openclaw.json`: `600` permissions (user only)
- `~/.openclaw`: `700` permissions (user only)
- Use full-disk encryption on gateway host
- Dedicated OS user for Gateway if host is shared

Enable log redaction: `logging.redactSensitive: "tools"` (default active).

## Research Disclosure

Before reporting vulnerabilities, verify:
1. Repro works on latest `main` or release
2. Includes exact code path and version/commit
3. Crosses documented trust boundary (not just prompt injection)
4. Not listed in out-of-scope findings
5. Explicit deployment assumptions (loopback vs exposed, trusted vs untrusted)

Contact: [security@openclaw.ai](mailto:security@openclaw.ai)

---
## Gateway > Tailscale

[Source: https://docs.openclaw.ai/gateway/tailscale]

Tailscale - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Remote access
Tailscale
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
Gateway
Gateway Runbook
Configuration and operations
Security and sandboxing
Protocols and APIs
Networking and discovery
Remote access
Remote Access
Remote Gateway Setup
Tailscale
Security
Formal Verification (Security Models)
Web interfaces
Web
Control UI
Dashboard
WebChat
TUI
Tailscale (Gateway dashboard)
Modes
Auth
Config examples
Tailnet-only (Serve)
Tailnet-only (bind to Tailnet IP)
Public internet (Funnel + shared password)
CLI examples
Notes
Browser control (remote Gateway + local browser)
Tailscale prerequisites + limits
Learn more
Remote access
Tailscale
Tailscale (Gateway dashboard)
OpenClaw can auto-configure Tailscale
Serve
(tailnet) or
Funnel
(public) for the
Gateway dashboard and WebSocket port. This keeps the Gateway bound to loopback while
Tailscale provides HTTPS, routing, and (for Serve) identity headers.
Modes
serve
: Tailnet-only Serve via
tailscale serve
. The gateway stays on
127.0.0.1
funnel
: Public HTTPS via
tailscale funnel
. OpenClaw requires a shared password.
off
: Default (no Tailscale automation).
Auth
Set
gateway.auth.mode
to control the handshake:
token
(default when
OPENCLAW_GATEWAY_TOKEN
is set)
password
(shared secret via
OPENCLAW_GATEWAY_PASSWORD
or config)
When
tailscale.mode = &quot;serve&quot;
and
gateway.auth.allowTailscale
true
valid Serve proxy requests can authenticate via Tailscale identity headers
tailscale-user-login
) without supplying a token/password. OpenClaw verifies
the identity by resolving the
x-forwarded-for
address via the local Tailscale
daemon (
tailscale whois
) and matching it to the header before accepting it.
OpenClaw only treats a request as Serve when it arrives from loopback with
Tailscale’s
x-forwarded-for
x-forwarded-proto
, and
x-forwarded-host
headers.
To require explicit credentials, set
gateway.auth.allowTailscale: false
force
gateway.auth.mode: &quot;password&quot;
Config examples
Tailnet-only (Serve)
Copy
gateway
bind
&quot;loopback&quot;
tailscale
mode
&quot;serve&quot;
Open:
https://&lt;magicdns&gt;/
(or your configured
gateway.controlUi.basePath
Tailnet-only (bind to Tailnet IP)
Use this when you want the Gateway to listen directly on the Tailnet IP (no Serve/Funnel).
Copy
gateway
bind
&quot;tailnet&quot;
auth
mode
&quot;token&quot;
token
&quot;your-token&quot;
Connect from another Tailnet device:
Control UI:
http://&lt;tailscale-ip&gt;:18789/
WebSocket:
ws://&lt;tailscale-ip&gt;:18789
Note: loopback (
http://127.0.0.1:18789
) will
not
work in this mode.
Public internet (Funnel + shared password)
Copy
gateway
bind
&quot;loopback&quot;
tailscale
mode
&quot;funnel&quot;
auth
mode
&quot;password&quot;
password
&quot;replace-me&quot;
Prefer
OPENCLAW_GATEWAY_PASSWORD
over committing a password to disk.
CLI examples
Copy
openclaw
gateway
--tailscale
serve
openclaw
gateway
--tailscale
funnel
--auth
password
Notes
Tailscale Serve/Funnel requires the
tailscale
CLI to be installed and logged in.
tailscale.mode: &quot;funnel&quot;
refuses to start unless auth mode is
password
to avoid public exposure.
Set
gateway.tailscale.resetOnExit
if you want OpenClaw to undo
tailscale serve
tailscale funnel
configuration on shutdown.
gateway.bind: &quot;tailnet&quot;
is a direct Tailnet bind (no HTTPS, no Serve/Funnel).
gateway.bind: &quot;auto&quot;
prefers loopback; use
tailnet
if you want Tailnet-only.
Serve/Funnel only expose the
Gateway control UI + WS
. Nodes connect over
the same Gateway WS endpoint, so Serve can work for node access.
Browser control (remote Gateway + local browser)
If you run the Gateway on one machine but want to drive a browser on another machine,
run a
node host
on the browser machine and keep both on the same tailnet.
The Gateway will proxy browser actions to the node; no separate control server or Serve URL needed.
Avoid Funnel for browser control; treat node pairing like operator access.
Tailscale prerequisites + limits
Serve requires HTTPS enabled for your tailnet; the CLI prompts if it is missing.
Serve injects Tailscale identity headers; Funnel does not.
Funnel requires Tailscale v1.38.3+, MagicDNS, HTTPS enabled, and a funnel node attribute.
Funnel only supports ports
443
8443
, and
10000
over TLS.
Funnel on macOS requires the open-source Tailscale app variant.
Learn more
Tailscale Serve overview:
https://tailscale.com/kb/1312/serve
tailscale serve
command:
https://tailscale.com/kb/1242/tailscale-serve
Tailscale Funnel overview:
https://tailscale.com/kb/1223/tailscale-funnel
tailscale funnel
command:
https://tailscale.com/kb/1311/tailscale-funnel
Remote Gateway Setup
Formal Verification (Security Models)

---
## Gateway > Tools Invoke Http Api

[Source: https://docs.openclaw.ai/gateway/tools-invoke-http-api]

Tools Invoke API - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Protocols and APIs
Tools Invoke API
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
Gateway
Gateway Runbook
Configuration and operations
Security and sandboxing
Protocols and APIs
Gateway Protocol
Bridge Protocol
OpenAI Chat Completions
Tools Invoke API
CLI Backends
Local Models
Networking and discovery
Remote access
Remote Access
Remote Gateway Setup
Tailscale
Security
Formal Verification (Security Models)
Web interfaces
Web
Control UI
Dashboard
WebChat
TUI
Tools Invoke (HTTP)
Authentication
Request body
Policy + routing behavior
Responses
Example
Protocols and APIs
Tools Invoke API
Tools Invoke (HTTP)
OpenClaw’s Gateway exposes a simple HTTP endpoint for invoking a single tool directly. It is always enabled, but gated by Gateway auth and tool policy.
POST /tools/invoke
Same port as the Gateway (WS + HTTP multiplex):
http://&lt;gateway-host&gt;:&lt;port&gt;/tools/invoke
Default max payload size is 2 MB.
Authentication
Uses the Gateway auth configuration. Send a bearer token:
Authorization: Bearer &lt;token&gt;
Notes:
When
gateway.auth.mode=&quot;token&quot;
, use
gateway.auth.token
(or
OPENCLAW_GATEWAY_TOKEN
When
gateway.auth.mode=&quot;password&quot;
, use
gateway.auth.password
(or
OPENCLAW_GATEWAY_PASSWORD
gateway.auth.rateLimit
is configured and too many auth failures occur, the endpoint returns
429
with
Retry-After
Request body
Copy
&quot;tool&quot;
&quot;sessions_list&quot;
&quot;action&quot;
&quot;json&quot;
&quot;args&quot;
&quot;sessionKey&quot;
&quot;main&quot;
&quot;dryRun&quot;
false
Fields:
tool
(string, required): tool name to invoke.
action
(string, optional): mapped into args if the tool schema supports
action
and the args payload omitted it.
args
(object, optional): tool-specific arguments.
sessionKey
(string, optional): target session key. If omitted or
&quot;main&quot;
, the Gateway uses the configured main session key (honors
session.mainKey
and default agent, or
global
in global scope).
dryRun
(boolean, optional): reserved for future use; currently ignored.
Policy + routing behavior
Tool availability is filtered through the same policy chain used by Gateway agents:
tools.profile
tools.byProvider.profile
tools.allow
tools.byProvider.allow
agents.&lt;id&gt;.tools.allow
agents.&lt;id&gt;.tools.byProvider.allow
group policies (if the session key maps to a group or channel)
subagent policy (when invoking with a subagent session key)
If a tool is not allowed by policy, the endpoint returns
404
Gateway HTTP also applies a hard deny list by default (even if session policy allows the tool):
sessions_spawn
sessions_send
gateway
whatsapp_login
You can customize this deny list via
gateway.tools
Copy
gateway
tools
// Additional tools to block over HTTP /tools/invoke
deny
&quot;browser&quot;
// Remove tools from the default deny list
allow
&quot;gateway&quot;
To help group policies resolve context, you can optionally set:
x-openclaw-message-channel: &lt;channel&gt;
(example:
slack
telegram
x-openclaw-account-id: &lt;accountId&gt;
(when multiple accounts exist)
Responses
200
{ ok: true, result }
400
{ ok: false, error: { type, message } }
(invalid request or tool input error)
401
→ unauthorized
429
→ auth rate-limited (
Retry-After
set)
404
→ tool not available (not found or not allowlisted)
405
→ method not allowed
500
{ ok: false, error: { type, message } }
(unexpected tool execution error; sanitized message)
Example
Copy
curl
-sS
http://127.0.0.1:18789/tools/invoke
&#x27;Authorization: Bearer YOUR_TOKEN&#x27;
&#x27;Content-Type: application/json&#x27;
&#x27;{
&quot;tool&quot;: &quot;sessions_list&quot;,
&quot;action&quot;: &quot;json&quot;,
&quot;args&quot;: {}
}&#x27;
OpenAI Chat Completions
CLI Backends

---
## Gateway > Troubleshooting

[Source: https://docs.openclaw.ai/gateway/troubleshooting]

Troubleshooting - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Configuration and operations
Troubleshooting
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
Gateway
Gateway Runbook
Configuration and operations
Configuration
Configuration Reference
Configuration Examples
Authentication
Trusted proxy auth
Health Checks
Heartbeat
Doctor
Logging
Gateway Lock
Background Exec and Process Tool
Multiple Gateways
Troubleshooting
Security and sandboxing
Protocols and APIs
Networking and discovery
Remote access
Remote Access
Remote Gateway Setup
Tailscale
Security
Formal Verification (Security Models)
Web interfaces
Web
Control UI
Dashboard
WebChat
TUI
Gateway troubleshooting
Command ladder
No replies
Dashboard control ui connectivity
Gateway service not running
Channel connected messages not flowing
Cron and heartbeat delivery
Node paired tool fails
Browser tool fails
If you upgraded and something suddenly broke
1) Auth and URL override behavior changed
2) Bind and auth guardrails are stricter
3) Pairing and device identity state changed
Configuration and operations
Troubleshooting
Gateway troubleshooting
This page is the deep runbook.
Start at
/help/troubleshooting
if you want the fast triage flow first.
Command ladder
Run these first, in this order:
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
Expected healthy signals:
openclaw gateway status
shows
Runtime: running
and
RPC probe: ok
openclaw doctor
reports no blocking config/service issues.
openclaw channels status --probe
shows connected/ready channels.
No replies
If channels are up but nothing answers, check routing and policy before reconnecting anything.
Copy
openclaw
status
openclaw
channels
status
--probe
openclaw
pairing
list
&lt;
channe
&gt;
openclaw
config
get
channels
openclaw
logs
--follow
Look for:
Pairing pending for DM senders.
Group mention gating (
requireMention
mentionPatterns
Channel/group allowlist mismatches.
Common signatures:
drop guild message (mention required
→ group message ignored until mention.
pairing request
→ sender needs approval.
blocked
allowlist
→ sender/channel was filtered by policy.
Related:
/channels/troubleshooting
/channels/pairing
/channels/groups
Dashboard control ui connectivity
When dashboard/control UI will not connect, validate URL, auth mode, and secure context assumptions.
Copy
openclaw
gateway
status
openclaw
status
openclaw
logs
--follow
openclaw
doctor
openclaw
gateway
status
--json
Look for:
Correct probe URL and dashboard URL.
Auth mode/token mismatch between client and gateway.
HTTP usage where device identity is required.
Common signatures:
device identity required
→ non-secure context or missing device auth.
unauthorized
/ reconnect loop → token/password mismatch.
gateway connect failed:
→ wrong host/port/url target.
Related:
/web/control-ui
/gateway/authentication
/gateway/remote
Gateway service not running
Use this when service is installed but process does not stay up.
Copy
openclaw
gateway
status
openclaw
status
openclaw
logs
--follow
openclaw
doctor
openclaw
gateway
status
--deep
Look for:
Runtime: stopped
with exit hints.
Service config mismatch (
Config (cli)
Config (service)
Port/listener conflicts.
Common signatures:
Gateway start blocked: set gateway.mode=local
→ local gateway mode is not enabled. Fix: set
gateway.mode=&quot;local&quot;
in your config (or run
openclaw configure
). If you are running OpenClaw via Podman using the dedicated
openclaw
user, the config lives at
~openclaw/.openclaw/openclaw.json
refusing to bind gateway ... without auth
→ non-loopback bind without token/password.
another gateway instance is already listening
EADDRINUSE
→ port conflict.
Related:
/gateway/background-process
/gateway/configuration
/gateway/doctor
Channel connected messages not flowing
If channel state is connected but message flow is dead, focus on policy, permissions, and channel specific delivery rules.
Copy
openclaw
channels
status
--probe
openclaw
pairing
list
&lt;
channe
&gt;
openclaw
status
--deep
openclaw
logs
--follow
openclaw
config
get
channels
Look for:
DM policy (
pairing
allowlist
open
disabled
Group allowlist and mention requirements.
Missing channel API permissions/scopes.
Common signatures:
mention required
→ message ignored by group mention policy.
pairing
/ pending approval traces → sender is not approved.
missing_scope
not_in_channel
Forbidden
401/403
→ channel auth/permissions issue.
Related:
/channels/troubleshooting
/channels/whatsapp
/channels/telegram
/channels/discord
Cron and heartbeat delivery
If cron or heartbeat did not run or did not deliver, verify scheduler state first, then delivery target.
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
system
heartbeat
last
openclaw
logs
--follow
Look for:
Cron enabled and next wake present.
Job run history status (
skipped
error
Heartbeat skip reasons (
quiet-hours
requests-in-flight
alerts-disabled
Common signatures:
cron: scheduler disabled; jobs will not run automatically
→ cron disabled.
cron: timer tick failed
→ scheduler tick failed; check file/log/runtime errors.
heartbeat skipped
with
reason=quiet-hours
→ outside active hours window.
heartbeat: unknown accountId
→ invalid account id for heartbeat delivery target.
Related:
/automation/troubleshooting
/automation/cron-jobs
/gateway/heartbeat
Node paired tool fails
If a node is paired but tools fail, isolate foreground, permission, and approval state.
Copy
openclaw
nodes
status
openclaw
nodes
describe
--node
&lt;
idOrNameOrI
&gt;
openclaw
approvals
get
--node
&lt;
idOrNameOrI
&gt;
openclaw
logs
--follow
openclaw
status
Look for:
Node online with expected capabilities.
OS permission grants for camera/mic/location/screen.
Exec approvals and allowlist state.
Common signatures:
NODE_BACKGROUND_UNAVAILABLE
→ node app must be in foreground.
*_PERMISSION_REQUIRED
LOCATION_PERMISSION_REQUIRED
→ missing OS permission.
SYSTEM_RUN_DENIED: approval required
→ exec approval pending.
SYSTEM_RUN_DENIED: allowlist miss
→ command blocked by allowlist.
Related:
/nodes/troubleshooting
/nodes/index
/tools/exec-approvals
Browser tool fails
Use this when browser tool actions fail even though the gateway itself is healthy.
Copy
openclaw
browser
status
openclaw
browser
start
--browser-profile
openclaw
openclaw
browser
profiles
openclaw
logs
--follow
openclaw
doctor
Look for:
Valid browser executable path.
CDP profile reachability.
Extension relay tab attachment for
profile=&quot;chrome&quot;
Common signatures:
Failed to start Chrome CDP on port
→ browser process failed to launch.
browser.executablePath not found
→ configured path is invalid.
Chrome extension relay is running, but no tab is connected
→ extension relay not attached.
Browser attachOnly is enabled ... not reachable
→ attach-only profile has no reachable target.
Related:
/tools/browser-linux-troubleshooting
/tools/chrome-extension
/tools/browser
If you upgraded and something suddenly broke
Most post-upgrade breakage is config drift or stricter defaults now being enforced.
1) Auth and URL override behavior changed
Copy
openclaw
gateway
status
openclaw
config
get
gateway.mode
openclaw
config
get
gateway.remote.url
openclaw
config
get
gateway.auth.mode
What to check:
gateway.mode=remote
, CLI calls may be targeting remote while your local service is fine.
Explicit
--url
calls do not fall back to stored credentials.
Common signatures:
gateway connect failed:
→ wrong URL target.
unauthorized
→ endpoint reachable but wrong auth.
2) Bind and auth guardrails are stricter
Copy
openclaw
config
get
gateway.bind
openclaw
config
get
gateway.auth.token
openclaw
gateway
status
openclaw
logs
--follow
What to check:
Non-loopback binds (
lan
tailnet
custom
) need auth configured.
Old keys like
gateway.token
do not replace
gateway.auth.token
Common signatures:
refusing to bind gateway ... without auth
→ bind+auth mismatch.
RPC probe: failed
while runtime is running → gateway alive but inaccessible with current auth/url.
3) Pairing and device identity state changed
Copy
openclaw
devices
list
openclaw
pairing
list
&lt;
channe
&gt;
openclaw
logs
--follow
openclaw
doctor
What to check:
Pending device approvals for dashboard/nodes.
Pending DM pairing approvals after policy or identity changes.
Common signatures:
device identity required
→ device auth not satisfied.
pairing required
→ sender/device must be approved.
If the service config and runtime still disagree after checks, reinstall service metadata from the same profile/state directory:
Copy
openclaw
gateway
install
--force
openclaw
gateway
restart
Related:
/gateway/pairing
/gateway/authentication
/gateway/background-process
Multiple Gateways
Security

---
## Gateway > Trusted Proxy Auth

[Source: https://docs.openclaw.ai/gateway/trusted-proxy-auth]

Trusted proxy auth - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
Gateway
Gateway Runbook
Configuration and operations
Configuration
Configuration Reference
Configuration Examples
Authentication
Trusted proxy auth
Health Checks
Heartbeat
Doctor
Logging
Gateway Lock
Background Exec and Process Tool
Multiple Gateways
Troubleshooting
Security and sandboxing
Protocols and APIs
Networking and discovery
Remote access
Remote Access
Remote Gateway Setup
Tailscale
Security
Formal Verification (Security Models)
Web interfaces
Web
Control UI
Dashboard
WebChat
TUI
Trusted Proxy Auth
When to Use
When NOT to Use
How It Works
Configuration
Configuration Reference
Proxy Setup Examples
Pomerium
Caddy with OAuth
nginx + oauth2-proxy
Traefik with Forward Auth
Security Checklist
Security Audit
Troubleshooting
”trusted_proxy_untrusted_source”
”trusted_proxy_user_missing”
“trustedproxy_missing_header*”
”trusted_proxy_user_not_allowed”
WebSocket Still Failing
Migration from Token Auth
Related
Configuration and operations
Trusted proxy auth
Trusted Proxy Auth
Security-sensitive feature.
This mode delegates authentication entirely to your reverse proxy. Misconfiguration can expose your Gateway to unauthorized access. Read this page carefully before enabling.
When to Use
Use
trusted-proxy
auth mode when:
You run OpenClaw behind an
identity-aware proxy
(Pomerium, Caddy + OAuth, nginx + oauth2-proxy, Traefik + forward auth)
Your proxy handles all authentication and passes user identity via headers
You’re in a Kubernetes or container environment where the proxy is the only path to the Gateway
You’re hitting WebSocket
1008 unauthorized
errors because browsers can’t pass tokens in WS payloads
When NOT to Use
If your proxy doesn’t authenticate users (just a TLS terminator or load balancer)
If there’s any path to the Gateway that bypasses the proxy (firewall holes, internal network access)
If you’re unsure whether your proxy correctly strips/overwrites forwarded headers
If you only need personal single-user access (consider Tailscale Serve + loopback for simpler setup)
How It Works
Your reverse proxy authenticates users (OAuth, OIDC, SAML, etc.)
Proxy adds a header with the authenticated user identity (e.g.,
x-forwarded-user:
[email&#160;protected]
OpenClaw checks that the request came from a
trusted proxy IP
(configured in
gateway.trustedProxies
OpenClaw extracts the user identity from the configured header
If everything checks out, the request is authorized
Configuration
Copy
gateway
// Must bind to network interface (not loopback)
bind
&quot;lan&quot;
// CRITICAL: Only add your proxy&#x27;s IP(s) here
trustedProxies
&quot;10.0.0.1&quot;
&quot;172.17.0.1&quot;
auth
mode
&quot;trusted-proxy&quot;
trustedProxy
// Header containing authenticated user identity (required)
userHeader
&quot;x-forwarded-user&quot;
// Optional: headers that MUST be present (proxy verification)
requiredHeaders
&quot;x-forwarded-proto&quot;
&quot;x-forwarded-host&quot;
// Optional: restrict to specific users (empty = allow all)
allowUsers
&quot;
[email&#160;protected]
&quot;
&quot;
[email&#160;protected]
&quot;
Configuration Reference
Field
Required
Description
gateway.trustedProxies
Yes
Array of proxy IP addresses to trust. Requests from other IPs are rejected.
gateway.auth.mode
Yes
Must be
&quot;trusted-proxy&quot;
gateway.auth.trustedProxy.userHeader
Yes
Header name containing the authenticated user identity
gateway.auth.trustedProxy.requiredHeaders
Additional headers that must be present for the request to be trusted
gateway.auth.trustedProxy.allowUsers
Allowlist of user identities. Empty means allow all authenticated users.
Proxy Setup Examples
Pomerium
Pomerium passes identity in
x-pomerium-claim-email
(or other claim headers) and a JWT in
x-pomerium-jwt-assertion
Copy
gateway
bind
&quot;lan&quot;
trustedProxies
&quot;10.0.0.1&quot;
// Pomerium&#x27;s IP
auth
mode
&quot;trusted-proxy&quot;
trustedProxy
userHeader
&quot;x-pomerium-claim-email&quot;
requiredHeaders
&quot;x-pomerium-jwt-assertion&quot;
Pomerium config snippet:
Copy
routes
from
https://openclaw.example.com
http://openclaw-gateway:18789
policy
allow
email
[email&#160;protected]
pass_identity_headers
true
Caddy with OAuth
Caddy with the
caddy-security
plugin can authenticate users and pass identity headers.
Copy
gateway
bind
&quot;lan&quot;
trustedProxies
&quot;127.0.0.1&quot;
// Caddy&#x27;s IP (if on same host)
auth
mode
&quot;trusted-proxy&quot;
trustedProxy
userHeader
&quot;x-forwarded-user&quot;
Caddyfile snippet:
Copy
openclaw.example.com {
authenticate with oauth2_provider
authorize with policy1
reverse_proxy openclaw:18789 {
header_up X-Forwarded-User {http.auth.user.email}
nginx + oauth2-proxy
oauth2-proxy authenticates users and passes identity in
x-auth-request-email
Copy
gateway
bind
&quot;lan&quot;
trustedProxies
&quot;10.0.0.1&quot;
// nginx/oauth2-proxy IP
auth
mode
&quot;trusted-proxy&quot;
trustedProxy
userHeader
&quot;x-auth-request-email&quot;
nginx config snippet:
Copy
location
/ {
auth_request
/oauth2/auth;
auth_request_set
$user $upstream_http_x_auth_request_email;
proxy_pass
http://openclaw:18789;
proxy_set_header
X-Auth-Request-Email $user;
proxy_http_version
1.1
proxy_set_header
Upgrade $http_upgrade;
proxy_set_header
Connection
&quot;upgrade&quot;
Traefik with Forward Auth
Copy
gateway
bind
&quot;lan&quot;
trustedProxies
&quot;172.17.0.1&quot;
// Traefik container IP
auth
mode
&quot;trusted-proxy&quot;
trustedProxy
userHeader
&quot;x-forwarded-user&quot;
Security Checklist
Before enabling trusted-proxy auth, verify:
Proxy is the only path
: The Gateway port is firewalled from everything except your proxy
trustedProxies is minimal
: Only your actual proxy IPs, not entire subnets
Proxy strips headers
: Your proxy overwrites (not appends)
x-forwarded-*
headers from clients
TLS termination
: Your proxy handles TLS; users connect via HTTPS
allowUsers is set
(recommended): Restrict to known users rather than allowing anyone authenticated
Security Audit
openclaw security audit
will flag trusted-proxy auth with a
critical
severity finding. This is intentional — it’s a reminder that you’re delegating security to your proxy setup.
The audit checks for:
Missing
trustedProxies
configuration
Missing
userHeader
configuration
Empty
allowUsers
(allows any authenticated user)
Troubleshooting
”trusted_proxy_untrusted_source”
The request didn’t come from an IP in
gateway.trustedProxies
. Check:
Is the proxy IP correct? (Docker container IPs can change)
Is there a load balancer in front of your proxy?
Use
docker inspect
kubectl get pods -o wide
to find actual IPs
”trusted_proxy_user_missing”
The user header was empty or missing. Check:
Is your proxy configured to pass identity headers?
Is the header name correct? (case-insensitive, but spelling matters)
Is the user actually authenticated at the proxy?
“trusted
proxy_missing_header
A required header wasn’t present. Check:
Your proxy configuration for those specific headers
Whether headers are being stripped somewhere in the chain
”trusted_proxy_user_not_allowed”
The user is authenticated but not in
allowUsers
. Either add them or remove the allowlist.
WebSocket Still Failing
Make sure your proxy:
Supports WebSocket upgrades (
Upgrade: websocket
Connection: upgrade
Passes the identity headers on WebSocket upgrade requests (not just HTTP)
Doesn’t have a separate auth path for WebSocket connections
Migration from Token Auth
If you’re moving from token auth to trusted-proxy:
Configure your proxy to authenticate users and pass headers
Test the proxy setup independently (curl with headers)
Update OpenClaw config with trusted-proxy auth
Restart the Gateway
Test WebSocket connections from the Control UI
Run
openclaw security audit
and review findings
Related
Security
— full security guide
Configuration
— config reference
Remote Access
— other remote access patterns
Tailscale
— simpler alternative for tailnet-only access
Authentication
Health Checks

---
## Web > Control Ui

[Source: https://docs.openclaw.ai/web/control-ui]

Control UI - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Web interfaces
Control UI
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
Gateway
Gateway Runbook
Configuration and operations
Security and sandboxing
Protocols and APIs
Networking and discovery
Remote access
Remote Access
Remote Gateway Setup
Tailscale
Security
Formal Verification (Security Models)
Web interfaces
Web
Control UI
Dashboard
WebChat
TUI
Control UI (browser)
Quick open (local)
Device pairing (first connection)
What it can do (today)
Chat behavior
Tailnet access (recommended)
Integrated Tailscale Serve (preferred)
Bind to tailnet + token
Insecure HTTP
Building the UI
Debugging/testing: dev server + remote Gateway
Web interfaces
Control UI
Control UI (browser)
The Control UI is a small
Vite + Lit
single-page app served by the Gateway:
default:
http://&lt;host&gt;:18789/
optional prefix: set
gateway.controlUi.basePath
(e.g.
/openclaw
It speaks
directly to the Gateway WebSocket
on the same port.
Quick open (local)
If the Gateway is running on the same computer, open:
http://127.0.0.1:18789/
(or
http://localhost:18789/
If the page fails to load, start the Gateway first:
openclaw gateway
Auth is supplied during the WebSocket handshake via:
connect.params.auth.token
connect.params.auth.password
The dashboard settings panel lets you store a token; passwords are not persisted.
The onboarding wizard generates a gateway token by default, so paste it here on first connect.
Device pairing (first connection)
When you connect to the Control UI from a new browser or device, the Gateway
requires a
one-time pairing approval
— even if you’re on the same Tailnet
with
gateway.auth.allowTailscale: true
. This is a security measure to prevent
unauthorized access.
What you’ll see:
“disconnected (1008): pairing required”
To approve the device:
Copy
# List pending requests
openclaw
devices
list
# Approve by request ID
openclaw
devices
approve
&lt;
requestI
&gt;
Once approved, the device is remembered and won’t require re-approval unless
you revoke it with
openclaw devices revoke --device &lt;id&gt; --role &lt;role&gt;
. See
Devices CLI
for token rotation and revocation.
Notes:
Local connections (
127.0.0.1
) are auto-approved.
Remote connections (LAN, Tailnet, etc.) require explicit approval.
Each browser profile generates a unique device ID, so switching browsers or
clearing browser data will require re-pairing.
What it can do (today)
Chat with the model via Gateway WS (
chat.history
chat.send
chat.abort
chat.inject
Stream tool calls + live tool output cards in Chat (agent events)
Channels: WhatsApp/Telegram/Discord/Slack + plugin channels (Mattermost, etc.) status + QR login + per-channel config (
channels.status
web.login.*
config.patch
Instances: presence list + refresh (
system-presence
Sessions: list + per-session thinking/verbose overrides (
sessions.list
sessions.patch
Cron jobs: list/add/run/enable/disable + run history (
cron.*
Skills: status, enable/disable, install, API key updates (
skills.*
Nodes: list + caps (
node.list
Exec approvals: edit gateway or node allowlists + ask policy for
exec host=gateway/node
exec.approvals.*
Config: view/edit
~/.openclaw/openclaw.json
config.get
config.set
Config: apply + restart with validation (
config.apply
) and wake the last active session
Config writes include a base-hash guard to prevent clobbering concurrent edits
Config schema + form rendering (
config.schema
, including plugin + channel schemas); Raw JSON editor remains available
Debug: status/health/models snapshots + event log + manual RPC calls (
status
health
models.list
Logs: live tail of gateway file logs with filter/export (
logs.tail
Update: run a package/git update + restart (
update.run
) with a restart report
Cron jobs panel notes:
For isolated jobs, delivery defaults to announce summary. You can switch to none if you want internal-only runs.
Channel/target fields appear when announce is selected.
New job form includes a
Notify webhook
toggle (
notify
on the job).
Gateway webhook posting requires both
notify: true
on the job and
cron.webhook
in config.
Set
cron.webhookToken
to send a dedicated bearer token, if omitted the webhook is sent without an auth header.
Chat behavior
chat.send
non-blocking
: it acks immediately with
{ runId, status: &quot;started&quot; }
and the response streams via
chat
events.
Re-sending with the same
idempotencyKey
returns
{ status: &quot;in_flight&quot; }
while running, and
{ status: &quot;ok&quot; }
after completion.
chat.inject
appends an assistant note to the session transcript and broadcasts a
chat
event for UI-only updates (no agent run, no channel delivery).
Stop:
Click
Stop
(calls
chat.abort
Type
/stop
(or
stop|esc|abort|wait|exit|interrupt
) to abort out-of-band
chat.abort
supports
{ sessionKey }
(no
runId
) to abort all active runs for that session
Abort partial retention:
When a run is aborted, partial assistant text can still be shown in the UI
Gateway persists aborted partial assistant text into transcript history when buffered output exists
Persisted entries include abort metadata so transcript consumers can tell abort partials from normal completion output
Tailnet access (recommended)
Integrated Tailscale Serve (preferred)
Keep the Gateway on loopback and let Tailscale Serve proxy it with HTTPS:
Copy
openclaw
gateway
--tailscale
serve
Open:
https://&lt;magicdns&gt;/
(or your configured
gateway.controlUi.basePath
By default, Serve requests can authenticate via Tailscale identity headers
tailscale-user-login
) when
gateway.auth.allowTailscale
true
. OpenClaw
verifies the identity by resolving the
x-forwarded-for
address with
tailscale whois
and matching it to the header, and only accepts these when the
request hits loopback with Tailscale’s
x-forwarded-*
headers. Set
gateway.auth.allowTailscale: false
(or force
gateway.auth.mode: &quot;password&quot;
if you want to require a token/password even for Serve traffic.
Bind to tailnet + token
Copy
openclaw
gateway
--bind
tailnet
--token
&quot;$(
openssl
rand
-hex
)&quot;
Then open:
http://&lt;tailscale-ip&gt;:18789/
(or your configured
gateway.controlUi.basePath
Paste the token into the UI settings (sent as
connect.params.auth.token
Insecure HTTP
If you open the dashboard over plain HTTP (
http://&lt;lan-ip&gt;
http://&lt;tailscale-ip&gt;
the browser runs in a
non-secure context
and blocks WebCrypto. By default,
OpenClaw
blocks
Control UI connections without device identity.
Recommended fix:
use HTTPS (Tailscale Serve) or open the UI locally:
https://&lt;magicdns&gt;/
(Serve)
http://127.0.0.1:18789/
(on the gateway host)
Downgrade example (token-only over HTTP):
Copy
gateway
controlUi
allowInsecureAuth
true
bind
&quot;tailnet&quot;
auth
mode
&quot;token&quot;
token
&quot;replace-me&quot;
This disables device identity + pairing for the Control UI (even on HTTPS). Use
only if you trust the network.
See
Tailscale
for HTTPS setup guidance.
Building the UI
The Gateway serves static files from
dist/control-ui
. Build them with:
Copy
pnpm
ui:build
# auto-installs UI deps on first run
Optional absolute base (when you want fixed asset URLs):
Copy
OPENCLAW_CONTROL_UI_BASE_PATH
/openclaw/
pnpm
ui:build
For local development (separate dev server):
Copy
pnpm
ui:dev
# auto-installs UI deps on first run
Then point the UI at your Gateway WS URL (e.g.
ws://127.0.0.1:18789
Debugging/testing: dev server + remote Gateway
The Control UI is static files; the WebSocket target is configurable and can be
different from the HTTP origin. This is handy when you want the Vite dev server
locally but the Gateway runs elsewhere.
Start the UI dev server:
pnpm ui:dev
Open a URL like:
Copy
http://localhost:5173/?gatewayUrl=ws://&lt;gateway-host&gt;:18789
Optional one-time auth (if needed):
Copy
http://localhost:5173/?gatewayUrl=wss://&lt;gateway-host&gt;:18789&amp;token=&lt;gateway-token&gt;
Notes:
gatewayUrl
is stored in localStorage after load and removed from the URL.
token
is stored in localStorage;
password
is kept in memory only.
When
gatewayUrl
is set, the UI does not fall back to config or environment credentials.
Provide
token
(or
password
) explicitly. Missing explicit credentials is an error.
Use
wss://
when the Gateway is behind TLS (Tailscale Serve, HTTPS proxy, etc.).
gatewayUrl
is only accepted in a top-level window (not embedded) to prevent clickjacking.
For cross-origin dev setups (e.g.
pnpm ui:dev
to a remote Gateway), add the UI
origin to
gateway.controlUi.allowedOrigins
Example:
Copy
gateway
controlUi
allowedOrigins
&quot;http://localhost:5173&quot;
Remote access setup details:
Remote access
Web
Dashboard

---
## Web > Dashboard

[Source: https://docs.openclaw.ai/web/dashboard]

Dashboard - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Web interfaces
Dashboard
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
Gateway
Gateway Runbook
Configuration and operations
Security and sandboxing
Protocols and APIs
Networking and discovery
Remote access
Remote Access
Remote Gateway Setup
Tailscale
Security
Formal Verification (Security Models)
Web interfaces
Web
Control UI
Dashboard
WebChat
TUI
Dashboard (Control UI)
Fast path (recommended)
Token basics (local vs remote)
If you see “unauthorized” / 1008
Web interfaces
Dashboard
Dashboard (Control UI)
The Gateway dashboard is the browser Control UI served at
by default
(override with
gateway.controlUi.basePath
Quick open (local Gateway):
http://127.0.0.1:18789/
(or
http://localhost:18789/
Key references:
Control UI
for usage and UI capabilities.
Tailscale
for Serve/Funnel automation.
Web surfaces
for bind modes and security notes.
Authentication is enforced at the WebSocket handshake via
connect.params.auth
(token or password). See
gateway.auth
Gateway configuration
Security note: the Control UI is an
admin surface
(chat, config, exec approvals).
Do not expose it publicly. The UI stores the token in
localStorage
after first load.
Prefer localhost, Tailscale Serve, or an SSH tunnel.
Fast path (recommended)
After onboarding, the CLI auto-opens the dashboard and prints a clean (non-tokenized) link.
Re-open anytime:
openclaw dashboard
(copies link, opens browser if possible, shows SSH hint if headless).
If the UI prompts for auth, paste the token from
gateway.auth.token
(or
OPENCLAW_GATEWAY_TOKEN
) into Control UI settings.
Token basics (local vs remote)
Localhost
: open
http://127.0.0.1:18789/
Token source
gateway.auth.token
(or
OPENCLAW_GATEWAY_TOKEN
); the UI stores a copy in localStorage after you connect.
Not localhost
: use Tailscale Serve (tokenless if
gateway.auth.allowTailscale: true
), tailnet bind with a token, or an SSH tunnel. See
Web surfaces
If you see “unauthorized” / 1008
Ensure the gateway is reachable (local:
openclaw status
; remote: SSH tunnel
ssh -N -L 18789:127.0.0.1:18789 user@host
then open
http://127.0.0.1:18789/
Retrieve the token from the gateway host:
openclaw config get gateway.auth.token
(or generate one:
openclaw doctor --generate-gateway-token
In the dashboard settings, paste the token into the auth field, then connect.
Control UI
WebChat

---
## Web > Tui

[Source: https://docs.openclaw.ai/web/tui]

TUI - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Web interfaces
TUI
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
Gateway
Gateway Runbook
Configuration and operations
Security and sandboxing
Protocols and APIs
Networking and discovery
Remote access
Remote Access
Remote Gateway Setup
Tailscale
Security
Formal Verification (Security Models)
Web interfaces
Web
Control UI
Dashboard
WebChat
TUI
TUI (Terminal UI)
Quick start
What you see
Mental model: agents + sessions
Sending + delivery
Pickers + overlays
Keyboard shortcuts
Slash commands
Local shell commands
Tool output
History + streaming
Connection details
Options
Troubleshooting
Connection troubleshooting
Web interfaces
TUI
TUI (Terminal UI)
Quick start
Start the Gateway.
Copy
openclaw
gateway
Open the TUI.
Copy
openclaw
tui
Type a message and press Enter.
Remote Gateway:
Copy
openclaw
tui
--url
ws://
&lt;
hos
&gt;
&lt;
por
&gt;
--token
&lt;
gateway-toke
&gt;
Use
--password
if your Gateway uses password auth.
What you see
Header: connection URL, current agent, current session.
Chat log: user messages, assistant replies, system notices, tool cards.
Status line: connection/run state (connecting, running, streaming, idle, error).
Footer: connection state + agent + session + model + think/verbose/reasoning + token counts + deliver.
Input: text editor with autocomplete.
Mental model: agents + sessions
Agents are unique slugs (e.g.
main
research
). The Gateway exposes the list.
Sessions belong to the current agent.
Session keys are stored as
agent:&lt;agentId&gt;:&lt;sessionKey&gt;
If you type
/session main
, the TUI expands it to
agent:&lt;currentAgent&gt;:main
If you type
/session agent:other:main
, you switch to that agent session explicitly.
Session scope:
per-sender
(default): each agent has many sessions.
global
: the TUI always uses the
global
session (the picker may be empty).
The current agent + session are always visible in the footer.
Sending + delivery
Messages are sent to the Gateway; delivery to providers is off by default.
Turn delivery on:
/deliver on
or the Settings panel
or start with
openclaw tui --deliver
Pickers + overlays
Model picker: list available models and set the session override.
Agent picker: choose a different agent.
Session picker: shows only sessions for the current agent.
Settings: toggle deliver, tool output expansion, and thinking visibility.
Keyboard shortcuts
Enter: send message
Esc: abort active run
Ctrl+C: clear input (press twice to exit)
Ctrl+D: exit
Ctrl+L: model picker
Ctrl+G: agent picker
Ctrl+P: session picker
Ctrl+O: toggle tool output expansion
Ctrl+T: toggle thinking visibility (reloads history)
Slash commands
Core:
/help
/status
/agent &lt;id&gt;
(or
/agents
/session &lt;key&gt;
(or
/sessions
/model &lt;provider/model&gt;
(or
/models
Session controls:
/think &lt;off|minimal|low|medium|high&gt;
/verbose &lt;on|full|off&gt;
/reasoning &lt;on|off|stream&gt;
/usage &lt;off|tokens|full&gt;
/elevated &lt;on|off|ask|full&gt;
(alias:
/elev
/activation &lt;mention|always&gt;
/deliver &lt;on|off&gt;
Session lifecycle:
/new
/reset
(reset the session)
/abort
(abort the active run)
/settings
/exit
Other Gateway slash commands (for example,
/context
) are forwarded to the Gateway and shown as system output. See
Slash commands
Local shell commands
Prefix a line with
to run a local shell command on the TUI host.
The TUI prompts once per session to allow local execution; declining keeps
disabled for the session.
Commands run in a fresh, non-interactive shell in the TUI working directory (no persistent
/env).
A lone
is sent as a normal message; leading spaces do not trigger local exec.
Tool output
Tool calls show as cards with args + results.
Ctrl+O toggles between collapsed/expanded views.
While tools run, partial updates stream into the same card.
History + streaming
On connect, the TUI loads the latest history (default 200 messages).
Streaming responses update in place until finalized.
The TUI also listens to agent tool events for richer tool cards.
Connection details
The TUI registers with the Gateway as
mode: &quot;tui&quot;
Reconnects show a system message; event gaps are surfaced in the log.
Options
--url &lt;url&gt;
: Gateway WebSocket URL (defaults to config or
ws://127.0.0.1:&lt;port&gt;
--token &lt;token&gt;
: Gateway token (if required)
--password &lt;password&gt;
: Gateway password (if required)
--session &lt;key&gt;
: Session key (default:
main
, or
global
when scope is global)
--deliver
: Deliver assistant replies to the provider (default off)
--thinking &lt;level&gt;
: Override thinking level for sends
--timeout-ms &lt;ms&gt;
: Agent timeout in ms (defaults to
agents.defaults.timeoutSeconds
Note: when you set
--url
, the TUI does not fall back to config or environment credentials.
Pass
--token
--password
explicitly. Missing explicit credentials is an error.
Troubleshooting
No output after sending a message:
Run
/status
in the TUI to confirm the Gateway is connected and idle/busy.
Check the Gateway logs:
openclaw logs --follow
Confirm the agent can run:
openclaw status
and
openclaw models status
If you expect messages in a chat channel, enable delivery (
/deliver on
--deliver
--history-limit &lt;n&gt;
: History entries to load (default 200)
Connection troubleshooting
disconnected
: ensure the Gateway is running and your
--url/--token/--password
are correct.
No agents in picker: check
openclaw agents list
and your routing config.
Empty session picker: you might be in global scope or have no sessions yet.
WebChat

---
## Web > Webchat

[Source: https://docs.openclaw.ai/web/webchat]

WebChat - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Web interfaces
WebChat
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
Gateway
Gateway Runbook
Configuration and operations
Security and sandboxing
Protocols and APIs
Networking and discovery
Remote access
Remote Access
Remote Gateway Setup
Tailscale
Security
Formal Verification (Security Models)
Web interfaces
Web
Control UI
Dashboard
WebChat
TUI
WebChat (Gateway WebSocket UI)
What it is
Quick start
How it works (behavior)
Remote use
Configuration reference (WebChat)
Web interfaces
WebChat
WebChat (Gateway WebSocket UI)
Status: the macOS/iOS SwiftUI chat UI talks directly to the Gateway WebSocket.
What it is
A native chat UI for the gateway (no embedded browser and no local static server).
Uses the same sessions and routing rules as other channels.
Deterministic routing: replies always go back to WebChat.
Quick start
Start the gateway.
Open the WebChat UI (macOS/iOS app) or the Control UI chat tab.
Ensure gateway auth is configured (required by default, even on loopback).
How it works (behavior)
The UI connects to the Gateway WebSocket and uses
chat.history
chat.send
, and
chat.inject
chat.inject
appends an assistant note directly to the transcript and broadcasts it to the UI (no agent run).
Aborted runs can keep partial assistant output visible in the UI.
Gateway persists aborted partial assistant text into transcript history when buffered output exists, and marks those entries with abort metadata.
History is always fetched from the gateway (no local file watching).
If the gateway is unreachable, WebChat is read-only.
Remote use
Remote mode tunnels the gateway WebSocket over SSH/Tailscale.
You do not need to run a separate WebChat server.
Configuration reference (WebChat)
Full configuration:
Configuration
Channel options:
No dedicated
webchat.*
block. WebChat uses the gateway endpoint + auth settings below.
Related global options:
gateway.port
gateway.bind
: WebSocket host/port.
gateway.auth.mode
gateway.auth.token
gateway.auth.password
: WebSocket auth (token/password).
gateway.auth.mode: &quot;trusted-proxy&quot;
: reverse-proxy auth for browser clients (see
Trusted Proxy Auth
gateway.remote.url
gateway.remote.token
gateway.remote.password
: remote gateway target.
session.*
: session storage and main key defaults.
Dashboard
TUI

---
## Security > Formal Verification

[Source: https://docs.openclaw.ai/security/formal-verification]

Formal Verification (Security Models) - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Security
Formal Verification (Security Models)
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
Gateway
Gateway Runbook
Configuration and operations
Security and sandboxing
Protocols and APIs
Networking and discovery
Remote access
Remote Access
Remote Gateway Setup
Tailscale
Security
Formal Verification (Security Models)
Web interfaces
Web
Control UI
Dashboard
WebChat
TUI
Formal Verification (Security Models)
Where the models live
Important caveats
Reproducing results
Gateway exposure and open gateway misconfiguration
Nodes.run pipeline (highest-risk capability)
Pairing store (DM gating)
Ingress gating (mentions + control-command bypass)
Routing/session-key isolation
v1++: additional bounded models (concurrency, retries, trace correctness)
Pairing store concurrency / idempotency
Ingress trace correlation / idempotency
Routing dmScope precedence + identityLinks
Security
Formal Verification (Security Models)
Formal Verification (Security Models)
This page tracks OpenClaw’s
formal security models
(TLA+/TLC today; more as needed).
Note: some older links may refer to the previous project name.
Goal (north star):
provide a machine-checked argument that OpenClaw enforces its
intended security policy (authorization, session isolation, tool gating, and
misconfiguration safety), under explicit assumptions.
What this is (today):
an executable, attacker-driven
security regression suite
Each claim has a runnable model-check over a finite state space.
Many claims have a paired
negative model
that produces a counterexample trace for a realistic bug class.
What this is not (yet):
a proof that “OpenClaw is secure in all respects” or that the full TypeScript implementation is correct.
Where the models live
Models are maintained in a separate repo:
vignesh07/openclaw-formal-models
Important caveats
These are
models
, not the full TypeScript implementation. Drift between model and code is possible.
Results are bounded by the state space explored by TLC; “green” does not imply security beyond the modeled assumptions and bounds.
Some claims rely on explicit environmental assumptions (e.g., correct deployment, correct configuration inputs).
Reproducing results
Today, results are reproduced by cloning the models repo locally and running TLC (see below). A future iteration could offer:
CI-run models with public artifacts (counterexample traces, run logs)
a hosted “run this model” workflow for small, bounded checks
Getting started:
Copy
git
clone
https://github.com/vignesh07/openclaw-formal-models
openclaw-formal-models
# Java 11+ required (TLC runs on the JVM).
# The repo vendors a pinned `tla2tools.jar` (TLA+ tools) and provides `bin/tlc` + Make targets.
make
&lt;
targe
&gt;
Gateway exposure and open gateway misconfiguration
Claim:
binding beyond loopback without auth can make remote compromise possible / increases exposure; token/password blocks unauth attackers (per the model assumptions).
Green runs:
make gateway-exposure-v2
make gateway-exposure-v2-protected
Red (expected):
make gateway-exposure-v2-negative
See also:
docs/gateway-exposure-matrix.md
in the models repo.
Nodes.run pipeline (highest-risk capability)
Claim:
nodes.run
requires (a) node command allowlist plus declared commands and (b) live approval when configured; approvals are tokenized to prevent replay (in the model).
Green runs:
make nodes-pipeline
make approvals-token
Red (expected):
make nodes-pipeline-negative
make approvals-token-negative
Pairing store (DM gating)
Claim:
pairing requests respect TTL and pending-request caps.
Green runs:
make pairing
make pairing-cap
Red (expected):
make pairing-negative
make pairing-cap-negative
Ingress gating (mentions + control-command bypass)
Claim:
in group contexts requiring mention, an unauthorized “control command” cannot bypass mention gating.
Green:
make ingress-gating
Red (expected):
make ingress-gating-negative
Routing/session-key isolation
Claim:
DMs from distinct peers do not collapse into the same session unless explicitly linked/configured.
Green:
make routing-isolation
Red (expected):
make routing-isolation-negative
v1++: additional bounded models (concurrency, retries, trace correctness)
These are follow-on models that tighten fidelity around real-world failure modes (non-atomic updates, retries, and message fan-out).
Pairing store concurrency / idempotency
Claim:
a pairing store should enforce
MaxPending
and idempotency even under interleavings (i.e., “check-then-write” must be atomic / locked; refresh shouldn’t create duplicates).
What it means:
Under concurrent requests, you can’t exceed
MaxPending
for a channel.
Repeated requests/refreshes for the same
(channel, sender)
should not create duplicate live pending rows.
Green runs:
make pairing-race
(atomic/locked cap check)
make pairing-idempotency
make pairing-refresh
make pairing-refresh-race
Red (expected):
make pairing-race-negative
(non-atomic begin/commit cap race)
make pairing-idempotency-negative
make pairing-refresh-negative
make pairing-refresh-race-negative
Ingress trace correlation / idempotency
Claim:
ingestion should preserve trace correlation across fan-out and be idempotent under provider retries.
What it means:
When one external event becomes multiple internal messages, every part keeps the same trace/event identity.
Retries do not result in double-processing.
If provider event IDs are missing, dedupe falls back to a safe key (e.g., trace ID) to avoid dropping distinct events.
Green:
make ingress-trace
make ingress-trace2
make ingress-idempotency
make ingress-dedupe-fallback
Red (expected):
make ingress-trace-negative
make ingress-trace2-negative
make ingress-idempotency-negative
make ingress-dedupe-fallback-negative
Routing dmScope precedence + identityLinks
Claim:
routing must keep DM sessions isolated by default, and only collapse sessions when explicitly configured (channel precedence + identity links).
What it means:
Channel-specific dmScope overrides must win over global defaults.
identityLinks should collapse only within explicit linked groups, not across unrelated peers.
Green:
make routing-precedence
make routing-identitylinks
Red (expected):
make routing-precedence-negative
make routing-identitylinks-negative
Tailscale
Web