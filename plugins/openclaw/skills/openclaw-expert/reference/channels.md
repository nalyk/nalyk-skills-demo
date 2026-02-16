# OpenClaw Channels Reference

Complete configuration and setup for every supported messaging channel.


---
## Channels > Broadcast Groups

[Source: https://docs.openclaw.ai/channels/broadcast-groups]

Broadcast Groups - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Configuration
Broadcast Groups
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
Chat Channels
Messaging platforms
WhatsApp
Telegram
Discord
IRC
Slack
Feishu
Google Chat
Mattermost
Signal
iMessage
Microsoft Teams
LINE
Matrix
Zalo
Zalo Personal
Configuration
Pairing
Group Messages
Groups
Broadcast Groups
Channel Routing
Channel Location Parsing
Channel Troubleshooting
Broadcast Groups
Overview
Use Cases
1. Specialized Agent Teams
2. Multi-Language Support
3. Quality Assurance Workflows
4. Task Automation
Configuration
Basic Setup
Processing Strategy
Parallel (Default)
Sequential
Complete Example
How It Works
Message Flow
Session Isolation
Example: Isolated Sessions
Best Practices
1. Keep Agents Focused
2. Use Descriptive Names
3. Configure Different Tool Access
4. Monitor Performance
5. Handle Failures Gracefully
Compatibility
Providers
Routing
Troubleshooting
Agents Not Responding
Only One Agent Responding
Performance Issues
Examples
Example 1: Code Review Team
Example 2: Multi-Language Support
API Reference
Config Schema
Fields
Limitations
Future Enhancements
See Also
Configuration
Broadcast Groups
Broadcast Groups
Status:
Experimental
Version:
Added in 2026.1.9
Overview
Broadcast Groups enable multiple agents to process and respond to the same message simultaneously. This allows you to create specialized agent teams that work together in a single WhatsApp group or DM — all using one phone number.
Current scope:
WhatsApp only
(web channel).
Broadcast groups are evaluated after channel allowlists and group activation rules. In WhatsApp groups, this means broadcasts happen when OpenClaw would normally reply (for example: on mention, depending on your group settings).
Use Cases
1. Specialized Agent Teams
Deploy multiple agents with atomic, focused responsibilities:
Copy
Group: &quot;Development Team&quot;
Agents:
- CodeReviewer (reviews code snippets)
- DocumentationBot (generates docs)
- SecurityAuditor (checks for vulnerabilities)
- TestGenerator (suggests test cases)
Each agent processes the same message and provides its specialized perspective.
2. Multi-Language Support
Copy
Group: &quot;International Support&quot;
Agents:
- Agent_EN (responds in English)
- Agent_DE (responds in German)
- Agent_ES (responds in Spanish)
3. Quality Assurance Workflows
Copy
Group: &quot;Customer Support&quot;
Agents:
- SupportAgent (provides answer)
- QAAgent (reviews quality, only responds if issues found)
4. Task Automation
Copy
Group: &quot;Project Management&quot;
Agents:
- TaskTracker (updates task database)
- TimeLogger (logs time spent)
- ReportGenerator (creates summaries)
Configuration
Basic Setup
Add a top-level
broadcast
section (next to
bindings
). Keys are WhatsApp peer ids:
group chats: group JID (e.g.
[email&#160;protected]
DMs: E.164 phone number (e.g.
+15551234567
Copy
&quot;broadcast&quot;
&quot;
[email&#160;protected]
&quot;
&quot;alfred&quot;
&quot;baerbel&quot;
&quot;assistant3&quot;
Result:
When OpenClaw would reply in this chat, it will run all three agents.
Processing Strategy
Control how agents process messages:
Parallel (Default)
All agents process simultaneously:
Copy
&quot;broadcast&quot;
&quot;strategy&quot;
&quot;parallel&quot;
&quot;
[email&#160;protected]
&quot;
&quot;alfred&quot;
&quot;baerbel&quot;
Sequential
Agents process in order (one waits for previous to finish):
Copy
&quot;broadcast&quot;
&quot;strategy&quot;
&quot;sequential&quot;
&quot;
[email&#160;protected]
&quot;
&quot;alfred&quot;
&quot;baerbel&quot;
Complete Example
Copy
&quot;agents&quot;
&quot;list&quot;
&quot;id&quot;
&quot;code-reviewer&quot;
&quot;name&quot;
&quot;Code Reviewer&quot;
&quot;workspace&quot;
&quot;/path/to/code-reviewer&quot;
&quot;sandbox&quot;
&quot;mode&quot;
&quot;all&quot;
&quot;id&quot;
&quot;security-auditor&quot;
&quot;name&quot;
&quot;Security Auditor&quot;
&quot;workspace&quot;
&quot;/path/to/security-auditor&quot;
&quot;sandbox&quot;
&quot;mode&quot;
&quot;all&quot;
&quot;id&quot;
&quot;docs-generator&quot;
&quot;name&quot;
&quot;Documentation Generator&quot;
&quot;workspace&quot;
&quot;/path/to/docs-generator&quot;
&quot;sandbox&quot;
&quot;mode&quot;
&quot;all&quot;
&quot;broadcast&quot;
&quot;strategy&quot;
&quot;parallel&quot;
&quot;
[email&#160;protected]
&quot;
&quot;code-reviewer&quot;
&quot;security-auditor&quot;
&quot;docs-generator&quot;
&quot;
[email&#160;protected]
&quot;
&quot;support-en&quot;
&quot;support-de&quot;
&quot;+15555550123&quot;
&quot;assistant&quot;
&quot;logger&quot;
How It Works
Message Flow
Incoming message
arrives in a WhatsApp group
Broadcast check
: System checks if peer ID is in
broadcast
If in broadcast list
All listed agents process the message
Each agent has its own session key and isolated context
Agents process in parallel (default) or sequentially
If not in broadcast list
Normal routing applies (first matching binding)
Note: broadcast groups do not bypass channel allowlists or group activation rules (mentions/commands/etc). They only change
which agents run
when a message is eligible for processing.
Session Isolation
Each agent in a broadcast group maintains completely separate:
Session keys
agent:alfred:whatsapp:group:120363...
agent:baerbel:whatsapp:group:120363...
Conversation history
(agent doesn’t see other agents’ messages)
Workspace
(separate sandboxes if configured)
Tool access
(different allow/deny lists)
Memory/context
(separate IDENTITY.md, SOUL.md, etc.)
Group context buffer
(recent group messages used for context) is shared per peer, so all broadcast agents see the same context when triggered
This allows each agent to have:
Different personalities
Different tool access (e.g., read-only vs. read-write)
Different models (e.g., opus vs. sonnet)
Different skills installed
Example: Isolated Sessions
In group
[email&#160;protected]
with agents
[&quot;alfred&quot;, &quot;baerbel&quot;]
Alfred’s context:
Copy
Session: agent:alfred:whatsapp:group:
[email&#160;protected]
History: [user message, alfred&#x27;s previous responses]
Workspace: /Users/pascal/openclaw-alfred/
Tools: read, write, exec
Bärbel’s context:
Copy
Session: agent:baerbel:whatsapp:group:
[email&#160;protected]
History: [user message, baerbel&#x27;s previous responses]
Workspace: /Users/pascal/openclaw-baerbel/
Tools: read only
Best Practices
1. Keep Agents Focused
Design each agent with a single, clear responsibility:
Copy
&quot;broadcast&quot;
&quot;DEV_GROUP&quot;
&quot;formatter&quot;
&quot;linter&quot;
&quot;tester&quot;
Good:
Each agent has one job
Bad:
One generic “dev-helper” agent
2. Use Descriptive Names
Make it clear what each agent does:
Copy
&quot;agents&quot;
&quot;security-scanner&quot;
&quot;name&quot;
&quot;Security Scanner&quot;
&quot;code-formatter&quot;
&quot;name&quot;
&quot;Code Formatter&quot;
&quot;test-generator&quot;
&quot;name&quot;
&quot;Test Generator&quot;
3. Configure Different Tool Access
Give agents only the tools they need:
Copy
&quot;agents&quot;
&quot;reviewer&quot;
&quot;tools&quot;
&quot;allow&quot;
&quot;read&quot;
&quot;exec&quot;
] }
// Read-only
&quot;fixer&quot;
&quot;tools&quot;
&quot;allow&quot;
&quot;read&quot;
&quot;write&quot;
&quot;edit&quot;
&quot;exec&quot;
] }
// Read-write
4. Monitor Performance
With many agents, consider:
Using
&quot;strategy&quot;: &quot;parallel&quot;
(default) for speed
Limiting broadcast groups to 5-10 agents
Using faster models for simpler agents
5. Handle Failures Gracefully
Agents fail independently. One agent’s error doesn’t block others:
Copy
Message → [Agent A ✓, Agent B ✗ error, Agent C ✓]
Result: Agent A and C respond, Agent B logs error
Compatibility
Providers
Broadcast groups currently work with:
✅ WhatsApp (implemented)
🚧 Telegram (planned)
🚧 Discord (planned)
🚧 Slack (planned)
Routing
Broadcast groups work alongside existing routing:
Copy
&quot;bindings&quot;
&quot;match&quot;
&quot;channel&quot;
&quot;whatsapp&quot;
&quot;peer&quot;
&quot;kind&quot;
&quot;group&quot;
&quot;id&quot;
&quot;GROUP_A&quot;
} }
&quot;agentId&quot;
&quot;alfred&quot;
&quot;broadcast&quot;
&quot;GROUP_B&quot;
&quot;agent1&quot;
&quot;agent2&quot;
GROUP_A
: Only alfred responds (normal routing)
GROUP_B
: agent1 AND agent2 respond (broadcast)
Precedence:
broadcast
takes priority over
bindings
Troubleshooting
Agents Not Responding
Check:
Agent IDs exist in
agents.list
Peer ID format is correct (e.g.,
[email&#160;protected]
Agents are not in deny lists
Debug:
Copy
tail
~/.openclaw/logs/gateway.log
grep
broadcast
Only One Agent Responding
Cause:
Peer ID might be in
bindings
but not
broadcast
Fix:
Add to broadcast config or remove from bindings.
Performance Issues
If slow with many agents:
Reduce number of agents per group
Use lighter models (sonnet instead of opus)
Check sandbox startup time
Examples
Example 1: Code Review Team
Copy
&quot;broadcast&quot;
&quot;strategy&quot;
&quot;parallel&quot;
&quot;
[email&#160;protected]
&quot;
&quot;code-formatter&quot;
&quot;security-scanner&quot;
&quot;test-coverage&quot;
&quot;docs-checker&quot;
&quot;agents&quot;
&quot;list&quot;
&quot;id&quot;
&quot;code-formatter&quot;
&quot;workspace&quot;
&quot;~/agents/formatter&quot;
&quot;tools&quot;
&quot;allow&quot;
&quot;read&quot;
&quot;write&quot;
] }
&quot;id&quot;
&quot;security-scanner&quot;
&quot;workspace&quot;
&quot;~/agents/security&quot;
&quot;tools&quot;
&quot;allow&quot;
&quot;read&quot;
&quot;exec&quot;
] }
&quot;id&quot;
&quot;test-coverage&quot;
&quot;workspace&quot;
&quot;~/agents/testing&quot;
&quot;tools&quot;
&quot;allow&quot;
&quot;read&quot;
&quot;exec&quot;
] }
&quot;id&quot;
&quot;docs-checker&quot;
&quot;workspace&quot;
&quot;~/agents/docs&quot;
&quot;tools&quot;
&quot;allow&quot;
&quot;read&quot;
] } }
User sends:
Code snippet
Responses:
code-formatter: “Fixed indentation and added type hints”
security-scanner: “⚠️ SQL injection vulnerability in line 12”
test-coverage: “Coverage is 45%, missing tests for error cases”
docs-checker: “Missing docstring for function
process_data
Example 2: Multi-Language Support
Copy
&quot;broadcast&quot;
&quot;strategy&quot;
&quot;sequential&quot;
&quot;+15555550123&quot;
&quot;detect-language&quot;
&quot;translator-en&quot;
&quot;translator-de&quot;
&quot;agents&quot;
&quot;list&quot;
&quot;id&quot;
&quot;detect-language&quot;
&quot;workspace&quot;
&quot;~/agents/lang-detect&quot;
&quot;id&quot;
&quot;translator-en&quot;
&quot;workspace&quot;
&quot;~/agents/translate-en&quot;
&quot;id&quot;
&quot;translator-de&quot;
&quot;workspace&quot;
&quot;~/agents/translate-de&quot;
API Reference
Config Schema
Copy
interface
OpenClawConfig
broadcast
strategy
&quot;parallel&quot;
&quot;sequential&quot;
[peerId
string
string
[];
Fields
strategy
(optional): How to process agents
&quot;parallel&quot;
(default): All agents process simultaneously
&quot;sequential&quot;
: Agents process in array order
[peerId]
: WhatsApp group JID, E.164 number, or other peer ID
Value: Array of agent IDs that should process messages
Limitations
Max agents:
No hard limit, but 10+ agents may be slow
Shared context:
Agents don’t see each other’s responses (by design)
Message ordering:
Parallel responses may arrive in any order
Rate limits:
All agents count toward WhatsApp rate limits
Future Enhancements
Planned features:
Shared context mode (agents see each other’s responses)
Agent coordination (agents can signal each other)
Dynamic agent selection (choose agents based on message content)
Agent priorities (some agents respond before others)
See Also
Multi-Agent Configuration
Routing Configuration
Session Management
Groups
Channel Routing

---
## Channels > Channel Routing

[Source: https://docs.openclaw.ai/channels/channel-routing]

Channel Routing - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Configuration
Channel Routing
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
Chat Channels
Messaging platforms
WhatsApp
Telegram
Discord
IRC
Slack
Feishu
Google Chat
Mattermost
Signal
iMessage
Microsoft Teams
LINE
Matrix
Zalo
Zalo Personal
Configuration
Pairing
Group Messages
Groups
Broadcast Groups
Channel Routing
Channel Location Parsing
Channel Troubleshooting
Channels &amp; routing
Key terms
Session key shapes (examples)
Routing rules (how an agent is chosen)
Broadcast groups (run multiple agents)
Config overview
Session storage
WebChat behavior
Reply context
Configuration
Channel Routing
Channels &amp; routing
OpenClaw routes replies
back to the channel where a message came from
. The
model does not choose a channel; routing is deterministic and controlled by the
host configuration.
Key terms
Channel
whatsapp
telegram
discord
slack
signal
imessage
webchat
AccountId
: per‑channel account instance (when supported).
AgentId
: an isolated workspace + session store (“brain”).
SessionKey
: the bucket key used to store context and control concurrency.
Session key shapes (examples)
Direct messages collapse to the agent’s
main
session:
agent:&lt;agentId&gt;:&lt;mainKey&gt;
(default:
agent:main:main
Groups and channels remain isolated per channel:
Groups:
agent:&lt;agentId&gt;:&lt;channel&gt;:group:&lt;id&gt;
Channels/rooms:
agent:&lt;agentId&gt;:&lt;channel&gt;:channel:&lt;id&gt;
Threads:
Slack/Discord threads append
:thread:&lt;threadId&gt;
to the base key.
Telegram forum topics embed
:topic:&lt;topicId&gt;
in the group key.
Examples:
agent:main:telegram:group:-1001234567890:topic:42
agent:main:discord:channel:123456:thread:987654
Routing rules (how an agent is chosen)
Routing picks
one agent
for each inbound message:
Exact peer match
bindings
with
peer.kind
peer.id
Parent peer match
(thread inheritance).
Guild + roles match
(Discord) via
guildId
roles
Guild match
(Discord) via
guildId
Team match
(Slack) via
teamId
Account match
accountId
on the channel).
Channel match
(any account on that channel,
accountId: &quot;*&quot;
Default agent
agents.list[].default
, else first list entry, fallback to
main
When a binding includes multiple match fields (
peer
guildId
teamId
roles
all provided fields must match
for that binding to apply.
The matched agent determines which workspace and session store are used.
Broadcast groups (run multiple agents)
Broadcast groups let you run
multiple agents
for the same peer
when OpenClaw would normally reply
(for example: in WhatsApp groups, after mention/activation gating).
Config:
Copy
broadcast
strategy
&quot;parallel&quot;
&quot;
[email&#160;protected]
&quot;
&quot;alfred&quot;
&quot;baerbel&quot;
&quot;+15555550123&quot;
&quot;support&quot;
&quot;logger&quot;
See:
Broadcast Groups
Config overview
agents.list
: named agent definitions (workspace, model, etc.).
bindings
: map inbound channels/accounts/peers to agents.
Example:
Copy
agents
list
&quot;support&quot;
name
&quot;Support&quot;
workspace
&quot;~/.openclaw/workspace-support&quot;
bindings
match
channel
&quot;slack&quot;
teamId
&quot;T123&quot;
agentId
&quot;support&quot;
match
channel
&quot;telegram&quot;
peer
kind
&quot;group&quot;
&quot;-100123&quot;
} }
agentId
&quot;support&quot;
Session storage
Session stores live under the state directory (default
~/.openclaw
~/.openclaw/agents/&lt;agentId&gt;/sessions/sessions.json
JSONL transcripts live alongside the store
You can override the store path via
session.store
and
{agentId}
templating.
WebChat behavior
WebChat attaches to the
selected agent
and defaults to the agent’s main
session. Because of this, WebChat lets you see cross‑channel context for that
agent in one place.
Reply context
Inbound replies include:
ReplyToId
ReplyToBody
, and
ReplyToSender
when available.
Quoted context is appended to
Body
as a
[Replying to ...]
block.
This is consistent across channels.
Broadcast Groups
Channel Location Parsing

---
## Channels > Discord

[Source: https://docs.openclaw.ai/channels/discord]

Discord - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Messaging platforms
Discord
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
Chat Channels
Messaging platforms
WhatsApp
Telegram
Discord
IRC
Slack
Feishu
Google Chat
Mattermost
Signal
iMessage
Microsoft Teams
LINE
Matrix
Zalo
Zalo Personal
Configuration
Pairing
Group Messages
Groups
Broadcast Groups
Channel Routing
Channel Location Parsing
Channel Troubleshooting
Discord (Bot API)
Quick setup
Runtime model
Interactive components
Access control and routing
Role-based agent routing
Developer Portal setup
Native commands and command auth
Feature details
Tools and action gates
Components v2 UI
Voice messages
Troubleshooting
Configuration reference pointers
Safety and operations
Related
Messaging platforms
Discord
Discord (Bot API)
Status: ready for DMs and guild channels via the official Discord gateway.
Pairing
Discord DMs default to pairing mode.
Slash commands
Native command behavior and command catalog.
Channel troubleshooting
Cross-channel diagnostics and repair flow.
Quick setup
Create a Discord bot and enable intents
Create an application in the Discord Developer Portal, add a bot, then enable:
Message Content Intent
Server Members Intent
(required for role allowlists and role-based routing; recommended for name-to-ID allowlist matching)
Configure token
Copy
channels
discord
enabled
true
token
&quot;YOUR_BOT_TOKEN&quot;
Env fallback for the default account:
Copy
DISCORD_BOT_TOKEN
...
Invite the bot and start gateway
Invite the bot to your server with message permissions.
Copy
openclaw
gateway
Approve first DM pairing
Copy
openclaw
pairing
list
discord
openclaw
pairing
approve
discord
&lt;
COD
&gt;
Pairing codes expire after 1 hour.
Token resolution is account-aware. Config token values win over env fallback.
DISCORD_BOT_TOKEN
is only used for the default account.
Runtime model
Gateway owns the Discord connection.
Reply routing is deterministic: Discord inbound replies back to Discord.
By default (
session.dmScope=main
), direct chats share the agent main session (
agent:main:main
Guild channels are isolated session keys (
agent:&lt;agentId&gt;:discord:channel:&lt;channelId&gt;
Group DMs are ignored by default (
channels.discord.dm.groupEnabled=false
Native slash commands run in isolated command sessions (
agent:&lt;agentId&gt;:discord:slash:&lt;userId&gt;
), while still carrying
CommandTargetSessionKey
to the routed conversation session.
Interactive components
OpenClaw supports Discord components v2 containers for agent messages. Use the message tool with a
components
payload. Interaction results are routed back to the agent as normal inbound messages and follow the existing Discord
replyToMode
settings.
Supported blocks:
text
section
separator
actions
media-gallery
file
Action rows allow up to 5 buttons or a single select menu
Select types:
string
user
role
mentionable
channel
File attachments:
file
blocks must point to an attachment reference (
attachment://&lt;filename&gt;
Provide the attachment via
media
path
filePath
(single file); use
media-gallery
for multiple files
Use
filename
to override the upload name when it should match the attachment reference
Modal forms:
Add
components.modal
with up to 5 fields
Field types:
text
checkbox
radio
select
role-select
user-select
OpenClaw adds a trigger button automatically
Example:
Copy
channel
&quot;discord&quot;
action
&quot;send&quot;
&quot;channel:123456789012345678&quot;
message
&quot;Optional fallback text&quot;
components
text
&quot;Choose a path&quot;
blocks
type
&quot;actions&quot;
buttons
label
&quot;Approve&quot;
style
&quot;success&quot;
label
&quot;Decline&quot;
style
&quot;danger&quot;
type
&quot;actions&quot;
select
type
&quot;string&quot;
placeholder
&quot;Pick an option&quot;
options
label
&quot;Option A&quot;
value
&quot;a&quot;
label
&quot;Option B&quot;
value
&quot;b&quot;
modal
title
&quot;Details&quot;
triggerLabel
&quot;Open form&quot;
fields
type
&quot;text&quot;
label
&quot;Requester&quot;
type
&quot;select&quot;
label
&quot;Priority&quot;
options
label
&quot;Low&quot;
value
&quot;low&quot;
label
&quot;High&quot;
value
&quot;high&quot;
Access control and routing
DM policy
Guild policy
Mentions and group DMs
channels.discord.dmPolicy
controls DM access (legacy:
channels.discord.dm.policy
pairing
(default)
allowlist
open
(requires
channels.discord.allowFrom
to include
&quot;*&quot;
; legacy:
channels.discord.dm.allowFrom
disabled
If DM policy is not open, unknown users are blocked (or prompted for pairing in
pairing
mode).
DM target format for delivery:
user:&lt;id&gt;
&lt;@id&gt;
mention
Bare numeric IDs are ambiguous and rejected unless an explicit user/channel target kind is provided.
Guild handling is controlled by
channels.discord.groupPolicy
open
allowlist
disabled
Secure baseline when
channels.discord
exists is
allowlist
allowlist
behavior:
guild must match
channels.discord.guilds
preferred, slug accepted)
optional sender allowlists:
users
(IDs or names) and
roles
(role IDs only); if either is configured, senders are allowed when they match
users
roles
if a guild has
channels
configured, non-listed channels are denied
if a guild has no
channels
block, all channels in that allowlisted guild are allowed
Example:
Copy
channels
discord
groupPolicy
&quot;allowlist&quot;
guilds
&quot;123456789012345678&quot;
requireMention
true
users
&quot;987654321098765432&quot;
roles
&quot;123456789012345678&quot;
channels
general
allow
true
help
allow
true
requireMention
true
If you only set
DISCORD_BOT_TOKEN
and do not create a
channels.discord
block, runtime fallback is
groupPolicy=&quot;open&quot;
(with a warning in logs).
Guild messages are mention-gated by default.
Mention detection includes:
explicit bot mention
configured mention patterns (
agents.list[].groupChat.mentionPatterns
, fallback
messages.groupChat.mentionPatterns
implicit reply-to-bot behavior in supported cases
requireMention
is configured per guild/channel (
channels.discord.guilds...
Group DMs:
default: ignored (
dm.groupEnabled=false
optional allowlist via
dm.groupChannels
(channel IDs or slugs)
Role-based agent routing
Use
bindings[].match.roles
to route Discord guild members to different agents by role ID. Role-based bindings accept role IDs only and are evaluated after peer or parent-peer bindings and before guild-only bindings. If a binding also sets other match fields (for example
peer
guildId
roles
), all configured fields must match.
Copy
bindings
agentId
&quot;opus&quot;
match
channel
&quot;discord&quot;
guildId
&quot;123456789012345678&quot;
roles
&quot;111111111111111111&quot;
agentId
&quot;sonnet&quot;
match
channel
&quot;discord&quot;
guildId
&quot;123456789012345678&quot;
Developer Portal setup
Create app and bot
Discord Developer Portal -&gt;
Applications
-&gt;
New Application
Bot
-&gt;
Add Bot
Copy bot token
Privileged intents
Bot -&gt; Privileged Gateway Intents
, enable:
Message Content Intent
Server Members Intent (recommended)
Presence intent is optional and only required if you want to receive presence updates. Setting bot presence (
setPresence
) does not require enabling presence updates for members.
OAuth scopes and baseline permissions
OAuth URL generator:
scopes:
bot
applications.commands
Typical baseline permissions:
View Channels
Send Messages
Read Message History
Embed Links
Attach Files
Add Reactions (optional)
Avoid
Administrator
unless explicitly needed.
Copy IDs
Enable Discord Developer Mode, then copy:
server ID
channel ID
user ID
Prefer numeric IDs in OpenClaw config for reliable audits and probes.
Native commands and command auth
commands.native
defaults to
&quot;auto&quot;
and is enabled for Discord.
Per-channel override:
channels.discord.commands.native
commands.native=false
explicitly clears previously registered Discord native commands.
Native command auth uses the same Discord allowlists/policies as normal message handling.
Commands may still be visible in Discord UI for users who are not authorized; execution still enforces OpenClaw auth and returns “not authorized”.
See
Slash commands
for command catalog and behavior.
Feature details
Reply tags and native replies
Discord supports reply tags in agent output:
[[reply_to_current]]
[[reply_to:&lt;id&gt;]]
Controlled by
channels.discord.replyToMode
off
(default)
first
all
Note:
off
disables implicit reply threading. Explicit
[[reply_to_*]]
tags are still honored.
Message IDs are surfaced in context/history so agents can target specific messages.
History, context, and thread behavior
Guild history context:
channels.discord.historyLimit
default
fallback:
messages.groupChat.historyLimit
disables
DM history controls:
channels.discord.dmHistoryLimit
channels.discord.dms[&quot;&lt;user_id&gt;&quot;].historyLimit
Thread behavior:
Discord threads are routed as channel sessions
parent thread metadata can be used for parent-session linkage
thread config inherits parent channel config unless a thread-specific entry exists
Channel topics are injected as
untrusted
context (not as system prompt).
Reaction notifications
Per-guild reaction notification mode:
off
own
(default)
all
allowlist
(uses
guilds.&lt;id&gt;.users
Reaction events are turned into system events and attached to the routed Discord session.
Ack reactions
ackReaction
sends an acknowledgement emoji while OpenClaw is processing an inbound message.
Resolution order:
channels.discord.accounts.&lt;accountId&gt;.ackReaction
channels.discord.ackReaction
messages.ackReaction
agent identity emoji fallback (
agents.list[].identity.emoji
, else ”👀”)
Notes:
Discord accepts unicode emoji or custom emoji names.
Use
&quot;&quot;
to disable the reaction for a channel or account.
Config writes
Channel-initiated config writes are enabled by default.
This affects
/config set|unset
flows (when command features are enabled).
Disable:
Copy
channels
discord
configWrites
false
Gateway proxy
Route Discord gateway WebSocket traffic through an HTTP(S) proxy with
channels.discord.proxy
Copy
channels
discord
proxy
&quot;http://proxy.example:8080&quot;
Per-account override:
Copy
channels
discord
accounts
primary
proxy
&quot;http://proxy.example:8080&quot;
PluralKit support
Enable PluralKit resolution to map proxied messages to system member identity:
Copy
channels
discord
pluralkit
enabled
true
token
&quot;pk_live_...&quot;
// optional; needed for private systems
Notes:
allowlists can use
pk:&lt;memberId&gt;
member display names are matched by name/slug
lookups use original message ID and are time-window constrained
if lookup fails, proxied messages are treated as bot messages and dropped unless
allowBots=true
Presence configuration
Presence updates are applied only when you set a status or activity field.
Status only example:
Copy
channels
discord
status
&quot;idle&quot;
Activity example (custom status is the default activity type):
Copy
channels
discord
activity
&quot;Focus time&quot;
activityType
Streaming example:
Copy
channels
discord
activity
&quot;Live coding&quot;
activityType
activityUrl
&quot;https://twitch.tv/openclaw&quot;
Activity type map:
0: Playing
1: Streaming (requires
activityUrl
2: Listening
3: Watching
4: Custom (uses the activity text as the status state; emoji is optional)
5: Competing
Exec approvals in Discord
Discord supports button-based exec approvals in DMs and can optionally post approval prompts in the originating channel.
Config path:
channels.discord.execApprovals.enabled
channels.discord.execApprovals.approvers
channels.discord.execApprovals.target
channel
both
, default:
agentFilter
sessionFilter
cleanupAfterResolve
When
target
channel
both
, the approval prompt is visible in the channel. Only configured approvers can use the buttons; other users receive an ephemeral denial. Approval prompts include the command text, so only enable channel delivery in trusted channels. If the channel ID cannot be derived from the session key, OpenClaw falls back to DM delivery.
If approvals fail with unknown approval IDs, verify approver list and feature enablement.
Related docs:
Exec approvals
Tools and action gates
Discord message actions include messaging, channel admin, moderation, presence, and metadata actions.
Core examples:
messaging:
sendMessage
readMessages
editMessage
deleteMessage
threadReply
reactions:
react
reactions
emojiList
moderation:
timeout
kick
ban
presence:
setPresence
Action gates live under
channels.discord.actions.*
Default gate behavior:
Action group
Default
reactions, messages, threads, pins, polls, search, memberInfo, roleInfo, channelInfo, channels, voiceStatus, events, stickers, emojiUploads, stickerUploads, permissions
enabled
roles
disabled
moderation
disabled
presence
disabled
Components v2 UI
OpenClaw uses Discord components v2 for exec approvals and cross-context markers. Discord message actions can also accept
components
for custom UI (advanced; requires Carbon component instances), while legacy
embeds
remain available but are not recommended.
channels.discord.ui.components.accentColor
sets the accent color used by Discord component containers (hex).
Set per account with
channels.discord.accounts.&lt;id&gt;.ui.components.accentColor
embeds
are ignored when components v2 are present.
Example:
Copy
channels
discord
components
accentColor
&quot;#5865F2&quot;
Voice messages
Discord voice messages show a waveform preview and require OGG/Opus audio plus metadata. OpenClaw generates the waveform automatically, but it needs
ffmpeg
and
ffprobe
available on the gateway host to inspect and convert audio files.
Requirements and constraints:
Provide a
local file path
(URLs are rejected).
Omit text content (Discord does not allow text + voice message in the same payload).
Any audio format is accepted; OpenClaw converts to OGG/Opus when needed.
Example:
Copy
message(action
&quot;send&quot;
channel=
&quot;discord&quot;
target=
&quot;channel:123&quot;
path=
&quot;/path/to/audio.mp3&quot;
asVoice=
true
Troubleshooting
Used disallowed intents or bot sees no guild messages
enable Message Content Intent
enable Server Members Intent when you depend on user/member resolution
restart gateway after changing intents
Guild messages blocked unexpectedly
verify
groupPolicy
verify guild allowlist under
channels.discord.guilds
if guild
channels
map exists, only listed channels are allowed
verify
requireMention
behavior and mention patterns
Useful checks:
Copy
openclaw
doctor
openclaw
channels
status
--probe
openclaw
logs
--follow
Require mention false but still blocked
Common causes:
groupPolicy=&quot;allowlist&quot;
without matching guild/channel allowlist
requireMention
configured in the wrong place (must be under
channels.discord.guilds
or channel entry)
sender blocked by guild/channel
users
allowlist
Permissions audit mismatches
channels status --probe
permission checks only work for numeric channel IDs.
If you use slug keys, runtime matching can still work, but probe cannot fully verify permissions.
DM and pairing issues
DM disabled:
channels.discord.dm.enabled=false
DM policy disabled:
channels.discord.dmPolicy=&quot;disabled&quot;
(legacy:
channels.discord.dm.policy
awaiting pairing approval in
pairing
mode
Bot to bot loops
By default bot-authored messages are ignored.
If you set
channels.discord.allowBots=true
, use strict mention and allowlist rules to avoid loop behavior.
Configuration reference pointers
Primary reference:
Configuration reference - Discord
High-signal Discord fields:
startup/auth:
enabled
token
accounts.*
allowBots
policy:
groupPolicy
dm.*
guilds.*
guilds.*.channels.*
command:
commands.native
commands.useAccessGroups
configWrites
reply/history:
replyToMode
historyLimit
dmHistoryLimit
dms.*.historyLimit
delivery:
textChunkLimit
chunkMode
maxLinesPerMessage
media/retry:
mediaMaxMb
retry
actions:
actions.*
presence:
activity
status
activityType
activityUrl
UI:
ui.components.accentColor
features:
pluralkit
execApprovals
intents
agentComponents
heartbeat
responsePrefix
Safety and operations
Treat bot tokens as secrets (
DISCORD_BOT_TOKEN
preferred in supervised environments).
Grant least-privilege Discord permissions.
If command deploy/state is stale, restart gateway and re-check with
openclaw channels status --probe
Related
Pairing
Channel routing
Troubleshooting
Slash commands
Telegram
IRC

---
## Channels > Feishu

[Source: https://docs.openclaw.ai/channels/feishu]

Feishu - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Messaging platforms
Feishu
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
Chat Channels
Messaging platforms
WhatsApp
Telegram
Discord
IRC
Slack
Feishu
Google Chat
Mattermost
Signal
iMessage
Microsoft Teams
LINE
Matrix
Zalo
Zalo Personal
Configuration
Pairing
Group Messages
Groups
Broadcast Groups
Channel Routing
Channel Location Parsing
Channel Troubleshooting
Feishu bot
Plugin required
Quickstart
Method 1: onboarding wizard (recommended)
Method 2: CLI setup
Step 1: Create a Feishu app
1. Open Feishu Open Platform
2. Create an app
3. Copy credentials
4. Configure permissions
5. Enable bot capability
6. Configure event subscription
7. Publish the app
Step 2: Configure OpenClaw
Configure with the wizard (recommended)
Configure via config file
Configure via environment variables
Lark (global) domain
Step 3: Start + test
1. Start the gateway
2. Send a test message
3. Approve pairing
Overview
Access control
Direct messages
Group chats
Group configuration examples
Allow all groups, require @mention (default)
Allow all groups, no @mention required
Allow specific users in groups only
Get group/user IDs
Group IDs (chat_id)
User IDs (open_id)
Common commands
Gateway management commands
Troubleshooting
Bot does not respond in group chats
Bot does not receive messages
App Secret leak
Message send failures
Advanced configuration
Multiple accounts
Message limits
Streaming
Multi-agent routing
Configuration reference
dmPolicy reference
Supported message types
Receive
Send
Messaging platforms
Feishu
Feishu bot
Feishu (Lark) is a team chat platform used by companies for messaging and collaboration. This plugin connects OpenClaw to a Feishu/Lark bot using the platform’s WebSocket event subscription so messages can be received without exposing a public webhook URL.
Plugin required
Install the Feishu plugin:
Copy
openclaw
plugins
install
@openclaw/feishu
Local checkout (when running from a git repo):
Copy
openclaw
plugins
install
./extensions/feishu
Quickstart
There are two ways to add the Feishu channel:
Method 1: onboarding wizard (recommended)
If you just installed OpenClaw, run the wizard:
Copy
openclaw
onboard
The wizard guides you through:
Creating a Feishu app and collecting credentials
Configuring app credentials in OpenClaw
Starting the gateway
After configuration
, check gateway status:
openclaw gateway status
openclaw logs --follow
Method 2: CLI setup
If you already completed initial install, add the channel via CLI:
Copy
openclaw
channels
add
Choose
Feishu
, then enter the App ID and App Secret.
After configuration
, manage the gateway:
openclaw gateway status
openclaw gateway restart
openclaw logs --follow
Step 1: Create a Feishu app
1. Open Feishu Open Platform
Visit
Feishu Open Platform
and sign in.
Lark (global) tenants should use
https://open.larksuite.com/app
and set
domain: &quot;lark&quot;
in the Feishu config.
2. Create an app
Click
Create enterprise app
Fill in the app name + description
Choose an app icon
3. Copy credentials
From
Credentials &amp; Basic Info
, copy:
App ID
(format:
cli_xxx
App Secret
Important:
keep the App Secret private.
4. Configure permissions
Permissions
, click
Batch import
and paste:
Copy
&quot;scopes&quot;
&quot;tenant&quot;
&quot;aily:file:read&quot;
&quot;aily:file:write&quot;
&quot;application:application.app_message_stats.overview:readonly&quot;
&quot;application:application:self_manage&quot;
&quot;application:bot.menu:write&quot;
&quot;contact:user.employee_id:readonly&quot;
&quot;corehr:file:download&quot;
&quot;event:ip_list&quot;
&quot;im:chat.access_event.bot_p2p_chat:read&quot;
&quot;im:chat.members:bot_access&quot;
&quot;im:message&quot;
&quot;im:message.group_at_msg:readonly&quot;
&quot;im:message.p2p_msg:readonly&quot;
&quot;im:message:readonly&quot;
&quot;im:message:send_as_bot&quot;
&quot;im:resource&quot;
&quot;user&quot;
&quot;aily:file:read&quot;
&quot;aily:file:write&quot;
&quot;im:chat.access_event.bot_p2p_chat:read&quot;
5. Enable bot capability
App Capability
&gt;
Bot
Enable bot capability
Set the bot name
6. Configure event subscription
Important:
before setting event subscription, make sure:
You already ran
openclaw channels add
for Feishu
The gateway is running (
openclaw gateway status
Event Subscription
Choose
Use long connection to receive events
(WebSocket)
Add the event:
im.message.receive_v1
⚠️ If the gateway is not running, the long-connection setup may fail to save.
7. Publish the app
Create a version in
Version Management &amp; Release
Submit for review and publish
Wait for admin approval (enterprise apps usually auto-approve)
Step 2: Configure OpenClaw
Configure with the wizard (recommended)
Copy
openclaw
channels
add
Choose
Feishu
and paste your App ID + App Secret.
Configure via config file
Edit
~/.openclaw/openclaw.json
Copy
channels
feishu
enabled
true
dmPolicy
&quot;pairing&quot;
accounts
main
appId
&quot;cli_xxx&quot;
appSecret
&quot;xxx&quot;
botName
&quot;My AI assistant&quot;
Configure via environment variables
Copy
export
FEISHU_APP_ID
&quot;cli_xxx&quot;
export
FEISHU_APP_SECRET
&quot;xxx&quot;
Lark (global) domain
If your tenant is on Lark (international), set the domain to
lark
(or a full domain string). You can set it at
channels.feishu.domain
or per account (
channels.feishu.accounts.&lt;id&gt;.domain
Copy
channels
feishu
domain
&quot;lark&quot;
accounts
main
appId
&quot;cli_xxx&quot;
appSecret
&quot;xxx&quot;
Step 3: Start + test
1. Start the gateway
Copy
openclaw
gateway
2. Send a test message
In Feishu, find your bot and send a message.
3. Approve pairing
By default, the bot replies with a pairing code. Approve it:
Copy
openclaw
pairing
approve
feishu
&lt;
COD
&gt;
After approval, you can chat normally.
Overview
Feishu bot channel
: Feishu bot managed by the gateway
Deterministic routing
: replies always return to Feishu
Session isolation
: DMs share a main session; groups are isolated
WebSocket connection
: long connection via Feishu SDK, no public URL needed
Access control
Direct messages
Default
dmPolicy: &quot;pairing&quot;
(unknown users get a pairing code)
Approve pairing
Copy
openclaw
pairing
list
feishu
openclaw
pairing
approve
feishu
&lt;
COD
&gt;
Allowlist mode
: set
channels.feishu.allowFrom
with allowed Open IDs
Group chats
1. Group policy
channels.feishu.groupPolicy
&quot;open&quot;
= allow everyone in groups (default)
&quot;allowlist&quot;
= only allow
groupAllowFrom
&quot;disabled&quot;
= disable group messages
2. Mention requirement
channels.feishu.groups.&lt;chat_id&gt;.requireMention
true
= require @mention (default)
false
= respond without mentions
Group configuration examples
Allow all groups, require @mention (default)
Copy
channels
feishu
groupPolicy
&quot;open&quot;
// Default requireMention: true
Allow all groups, no @mention required
Copy
channels
feishu
groups
oc_xxx
requireMention
false
Allow specific users in groups only
Copy
channels
feishu
groupPolicy
&quot;allowlist&quot;
groupAllowFrom
&quot;ou_xxx&quot;
&quot;ou_yyy&quot;
Get group/user IDs
Group IDs (chat_id)
Group IDs look like
oc_xxx
Method 1 (recommended)
Start the gateway and @mention the bot in the group
Run
openclaw logs --follow
and look for
chat_id
Method 2
Use the Feishu API debugger to list group chats.
User IDs (open_id)
User IDs look like
ou_xxx
Method 1 (recommended)
Start the gateway and DM the bot
Run
openclaw logs --follow
and look for
open_id
Method 2
Check pairing requests for user Open IDs:
Copy
openclaw
pairing
list
feishu
Common commands
Command
Description
/status
Show bot status
/reset
Reset the session
/model
Show/switch model
Note: Feishu does not support native command menus yet, so commands must be sent as text.
Gateway management commands
Command
Description
openclaw gateway status
Show gateway status
openclaw gateway install
Install/start gateway service
openclaw gateway stop
Stop gateway service
openclaw gateway restart
Restart gateway service
openclaw logs --follow
Tail gateway logs
Troubleshooting
Bot does not respond in group chats
Ensure the bot is added to the group
Ensure you @mention the bot (default behavior)
Check
groupPolicy
is not set to
&quot;disabled&quot;
Check logs:
openclaw logs --follow
Bot does not receive messages
Ensure the app is published and approved
Ensure event subscription includes
im.message.receive_v1
Ensure
long connection
is enabled
Ensure app permissions are complete
Ensure the gateway is running:
openclaw gateway status
Check logs:
openclaw logs --follow
App Secret leak
Reset the App Secret in Feishu Open Platform
Update the App Secret in your config
Restart the gateway
Message send failures
Ensure the app has
im:message:send_as_bot
permission
Ensure the app is published
Check logs for detailed errors
Advanced configuration
Multiple accounts
Copy
channels
feishu
accounts
main
appId
&quot;cli_xxx&quot;
appSecret
&quot;xxx&quot;
botName
&quot;Primary bot&quot;
backup
appId
&quot;cli_yyy&quot;
appSecret
&quot;yyy&quot;
botName
&quot;Backup bot&quot;
enabled
false
Message limits
textChunkLimit
: outbound text chunk size (default: 2000 chars)
mediaMaxMb
: media upload/download limit (default: 30MB)
Streaming
Feishu supports streaming replies via interactive cards. When enabled, the bot updates a card as it generates text.
Copy
channels
feishu
streaming
true
// enable streaming card output (default true)
blockStreaming
true
// enable block-level streaming (default true)
Set
streaming: false
to wait for the full reply before sending.
Multi-agent routing
Use
bindings
to route Feishu DMs or groups to different agents.
Copy
agents
list
&quot;main&quot;
&quot;clawd-fan&quot;
workspace
&quot;/home/user/clawd-fan&quot;
agentDir
&quot;/home/user/.openclaw/agents/clawd-fan/agent&quot;
&quot;clawd-xi&quot;
workspace
&quot;/home/user/clawd-xi&quot;
agentDir
&quot;/home/user/.openclaw/agents/clawd-xi/agent&quot;
bindings
agentId
&quot;main&quot;
match
channel
&quot;feishu&quot;
peer
kind
&quot;direct&quot;
&quot;ou_xxx&quot;
agentId
&quot;clawd-fan&quot;
match
channel
&quot;feishu&quot;
peer
kind
&quot;direct&quot;
&quot;ou_yyy&quot;
agentId
&quot;clawd-xi&quot;
match
channel
&quot;feishu&quot;
peer
kind
&quot;group&quot;
&quot;oc_zzz&quot;
Routing fields:
match.channel
&quot;feishu&quot;
match.peer.kind
&quot;direct&quot;
&quot;group&quot;
match.peer.id
: user Open ID (
ou_xxx
) or group ID (
oc_xxx
See
Get group/user IDs
for lookup tips.
Configuration reference
Full configuration:
Gateway configuration
Key options:
Setting
Description
Default
channels.feishu.enabled
Enable/disable channel
true
channels.feishu.domain
API domain (
feishu
lark
feishu
channels.feishu.accounts.&lt;id&gt;.appId
App ID
channels.feishu.accounts.&lt;id&gt;.appSecret
App Secret
channels.feishu.accounts.&lt;id&gt;.domain
Per-account API domain override
feishu
channels.feishu.dmPolicy
DM policy
pairing
channels.feishu.allowFrom
DM allowlist (open_id list)
channels.feishu.groupPolicy
Group policy
open
channels.feishu.groupAllowFrom
Group allowlist
channels.feishu.groups.&lt;chat_id&gt;.requireMention
Require @mention
true
channels.feishu.groups.&lt;chat_id&gt;.enabled
Enable group
true
channels.feishu.textChunkLimit
Message chunk size
2000
channels.feishu.mediaMaxMb
Media size limit
channels.feishu.streaming
Enable streaming card output
true
channels.feishu.blockStreaming
Enable block streaming
true
dmPolicy reference
Value
Behavior
&quot;pairing&quot;
Default.
Unknown users get a pairing code; must be approved
&quot;allowlist&quot;
Only users in
allowFrom
can chat
&quot;open&quot;
Allow all users (requires
&quot;*&quot;
in allowFrom)
&quot;disabled&quot;
Disable DMs
Supported message types
Receive
✅ Text
✅ Rich text (post)
✅ Images
✅ Files
✅ Audio
✅ Video
✅ Stickers
Send
✅ Text
✅ Images
✅ Files
✅ Audio
⚠️ Rich text (partial support)
Slack
Google Chat

---
## Channels > Googlechat

[Source: https://docs.openclaw.ai/channels/googlechat]

Google Chat - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Messaging platforms
Google Chat
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
Chat Channels
Messaging platforms
WhatsApp
Telegram
Discord
IRC
Slack
Feishu
Google Chat
Mattermost
Signal
iMessage
Microsoft Teams
LINE
Matrix
Zalo
Zalo Personal
Configuration
Pairing
Group Messages
Groups
Broadcast Groups
Channel Routing
Channel Location Parsing
Channel Troubleshooting
Google Chat (Chat API)
Quick setup (beginner)
Add to Google Chat
Public URL (Webhook-only)
Option A: Tailscale Funnel (Recommended)
Option B: Reverse Proxy (Caddy)
Option C: Cloudflare Tunnel
How it works
Targets
Config highlights
Troubleshooting
405 Method Not Allowed
Other issues
Messaging platforms
Google Chat
Google Chat (Chat API)
Status: ready for DMs + spaces via Google Chat API webhooks (HTTP only).
Quick setup (beginner)
Create a Google Cloud project and enable the
Google Chat API
Go to:
Google Chat API Credentials
Enable the API if it is not already enabled.
Create a
Service Account
Press
Create Credentials
&gt;
Service Account
Name it whatever you want (e.g.,
openclaw-chat
Leave permissions blank (press
Continue
Leave principals with access blank (press
Done
Create and download the
JSON Key
In the list of service accounts, click on the one you just created.
Go to the
Keys
tab.
Click
Add Key
&gt;
Create new key
Select
JSON
and press
Create
Store the downloaded JSON file on your gateway host (e.g.,
~/.openclaw/googlechat-service-account.json
Create a Google Chat app in the
Google Cloud Console Chat Configuration
Fill in the
Application info
App name
: (e.g.
OpenClaw
Avatar URL
: (e.g.
https://openclaw.ai/logo.png
Description
: (e.g.
Personal AI Assistant
Enable
Interactive features
Under
Functionality
, check
Join spaces and group conversations
Under
Connection settings
, select
HTTP endpoint URL
Under
Triggers
, select
Use a common HTTP endpoint URL for all triggers
and set it to your gateway’s public URL followed by
/googlechat
Tip: Run
openclaw status
to find your gateway’s public URL.
Under
Visibility
, check
Make this Chat app available to specific people and groups in &lt;Your Domain&gt;
Enter your email address (e.g.
[email&#160;protected]
) in the text box.
Click
Save
at the bottom.
Enable the app status
After saving,
refresh the page
Look for the
App status
section (usually near the top or bottom after saving).
Change the status to
Live - available to users
Click
Save
again.
Configure OpenClaw with the service account path + webhook audience:
Env:
GOOGLE_CHAT_SERVICE_ACCOUNT_FILE=/path/to/service-account.json
Or config:
channels.googlechat.serviceAccountFile: &quot;/path/to/service-account.json&quot;
Set the webhook audience type + value (matches your Chat app config).
Start the gateway. Google Chat will POST to your webhook path.
Add to Google Chat
Once the gateway is running and your email is added to the visibility list:
Go to
Google Chat
Click the
(plus) icon next to
Direct Messages
In the search bar (where you usually add people), type the
App name
you configured in the Google Cloud Console.
Note
: The bot will
not
appear in the “Marketplace” browse list because it is a private app. You must search for it by name.
Select your bot from the results.
Click
Add
Chat
to start a 1:1 conversation.
Send “Hello” to trigger the assistant!
Public URL (Webhook-only)
Google Chat webhooks require a public HTTPS endpoint. For security,
only expose the
/googlechat
path
to the internet. Keep the OpenClaw dashboard and other sensitive endpoints on your private network.
Option A: Tailscale Funnel (Recommended)
Use Tailscale Serve for the private dashboard and Funnel for the public webhook path. This keeps
private while exposing only
/googlechat
Check what address your gateway is bound to:
Copy
-tlnp
grep
18789
Note the IP address (e.g.,
127.0.0.1
0.0.0.0
, or your Tailscale IP like
100.x.x.x
Expose the dashboard to the tailnet only (port 8443):
Copy
# If bound to localhost (127.0.0.1 or 0.0.0.0):
tailscale
serve
--bg
--https
8443
http://127.0.0.1:18789
# If bound to Tailscale IP only (e.g., 100.106.161.80):
tailscale
serve
--bg
--https
8443
http://100.106.161.80:18789
Expose only the webhook path publicly:
Copy
# If bound to localhost (127.0.0.1 or 0.0.0.0):
tailscale
funnel
--bg
--set-path
/googlechat
http://127.0.0.1:18789/googlechat
# If bound to Tailscale IP only (e.g., 100.106.161.80):
tailscale
funnel
--bg
--set-path
/googlechat
http://100.106.161.80:18789/googlechat
Authorize the node for Funnel access:
If prompted, visit the authorization URL shown in the output to enable Funnel for this node in your tailnet policy.
Verify the configuration:
Copy
tailscale
serve
status
tailscale
funnel
status
Your public webhook URL will be:
https://&lt;node-name&gt;.&lt;tailnet&gt;.ts.net/googlechat
Your private dashboard stays tailnet-only:
https://&lt;node-name&gt;.&lt;tailnet&gt;.ts.net:8443/
Use the public URL (without
:8443
) in the Google Chat app config.
Note: This configuration persists across reboots. To remove it later, run
tailscale funnel reset
and
tailscale serve reset
Option B: Reverse Proxy (Caddy)
If you use a reverse proxy like Caddy, only proxy the specific path:
Copy
your-domain.com {
reverse_proxy /googlechat* localhost:18789
With this config, any request to
your-domain.com/
will be ignored or returned as 404, while
your-domain.com/googlechat
is safely routed to OpenClaw.
Option C: Cloudflare Tunnel
Configure your tunnel’s ingress rules to only route the webhook path:
Path
/googlechat
-&gt;
http://localhost:18789/googlechat
Default Rule
: HTTP 404 (Not Found)
How it works
Google Chat sends webhook POSTs to the gateway. Each request includes an
Authorization: Bearer &lt;token&gt;
header.
OpenClaw verifies the token against the configured
audienceType
audience
audienceType: &quot;app-url&quot;
→ audience is your HTTPS webhook URL.
audienceType: &quot;project-number&quot;
→ audience is the Cloud project number.
Messages are routed by space:
DMs use session key
agent:&lt;agentId&gt;:googlechat:dm:&lt;spaceId&gt;
Spaces use session key
agent:&lt;agentId&gt;:googlechat:group:&lt;spaceId&gt;
DM access is pairing by default. Unknown senders receive a pairing code; approve with:
openclaw pairing approve googlechat &lt;code&gt;
Group spaces require @-mention by default. Use
botUser
if mention detection needs the app’s user name.
Targets
Use these identifiers for delivery and allowlists:
Direct messages:
users/&lt;userId&gt;
(recommended) or raw email
[email&#160;protected]
(mutable principal).
Deprecated:
users/&lt;email&gt;
is treated as a user id, not an email allowlist.
Spaces:
spaces/&lt;spaceId&gt;
Config highlights
Copy
channels
googlechat
enabled
true
serviceAccountFile
&quot;/path/to/service-account.json&quot;
audienceType
&quot;app-url&quot;
audience
&quot;https://gateway.example.com/googlechat&quot;
webhookPath
&quot;/googlechat&quot;
botUser
&quot;users/1234567890&quot;
// optional; helps mention detection
policy
&quot;pairing&quot;
allowFrom
&quot;users/1234567890&quot;
&quot;
[email&#160;protected]
&quot;
groupPolicy
&quot;allowlist&quot;
groups
&quot;spaces/AAAA&quot;
allow
true
requireMention
true
users
&quot;users/1234567890&quot;
systemPrompt
&quot;Short answers only.&quot;
actions
reactions
true
typingIndicator
&quot;message&quot;
mediaMaxMb
Notes:
Service account credentials can also be passed inline with
serviceAccount
(JSON string).
Default webhook path is
/googlechat
webhookPath
isn’t set.
Reactions are available via the
reactions
tool and
channels action
when
actions.reactions
is enabled.
typingIndicator
supports
none
message
(default), and
reaction
(reaction requires user OAuth).
Attachments are downloaded through the Chat API and stored in the media pipeline (size capped by
mediaMaxMb
Troubleshooting
405 Method Not Allowed
If Google Cloud Logs Explorer shows errors like:
Copy
status code: 405, reason phrase: HTTP error response: HTTP/1.1 405 Method Not Allowed
This means the webhook handler isn’t registered. Common causes:
Channel not configured
: The
channels.googlechat
section is missing from your config. Verify with:
Copy
openclaw
config
get
channels.googlechat
If it returns “Config path not found”, add the configuration (see
Config highlights
Plugin not enabled
: Check plugin status:
Copy
openclaw
plugins
list
grep
googlechat
If it shows “disabled”, add
plugins.entries.googlechat.enabled: true
to your config.
Gateway not restarted
: After adding config, restart the gateway:
Copy
openclaw
gateway
restart
Verify the channel is running:
Copy
openclaw
channels
status
# Should show: Google Chat default: enabled, configured, ...
Other issues
Check
openclaw channels status --probe
for auth errors or missing audience config.
If no messages arrive, confirm the Chat app’s webhook URL + event subscriptions.
If mention gating blocks replies, set
botUser
to the app’s user resource name and verify
requireMention
Use
openclaw logs --follow
while sending a test message to see if requests reach the gateway.
Related docs:
Gateway configuration
Security
Reactions
Feishu
Mattermost

---
## Channels > Grammy

[Source: https://docs.openclaw.ai/channels/grammy]

grammY - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Technical reference
grammY
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
grammY Integration (Telegram Bot API)
Why grammY
What we shipped
Technical reference
grammY
grammY Integration (Telegram Bot API)
Why grammY
TS-first Bot API client with built-in long-poll + webhook helpers, middleware, error handling, rate limiter.
Cleaner media helpers than hand-rolling fetch + FormData; supports all Bot API methods.
Extensible: proxy support via custom fetch, session middleware (optional), type-safe context.
What we shipped
Single client path:
fetch-based implementation removed; grammY is now the sole Telegram client (send + gateway) with the grammY throttler enabled by default.
Gateway:
monitorTelegramProvider
builds a grammY
Bot
, wires mention/allowlist gating, media download via
getFile
download
, and delivers replies with
sendMessage/sendPhoto/sendVideo/sendAudio/sendDocument
. Supports long-poll or webhook via
webhookCallback
Proxy:
optional
channels.telegram.proxy
uses
undici.ProxyAgent
through grammY’s
client.baseFetch
Webhook support:
webhook-set.ts
wraps
setWebhook/deleteWebhook
webhook.ts
hosts the callback with health + graceful shutdown. Gateway enables webhook mode when
channels.telegram.webhookUrl
channels.telegram.webhookSecret
are set (otherwise it long-polls).
Sessions:
direct chats collapse into the agent main session (
agent:&lt;agentId&gt;:&lt;mainKey&gt;
); groups use
agent:&lt;agentId&gt;:telegram:group:&lt;chatId&gt;
; replies route back to the same channel.
Config knobs:
channels.telegram.botToken
channels.telegram.dmPolicy
channels.telegram.groups
(allowlist + mention defaults),
channels.telegram.allowFrom
channels.telegram.groupAllowFrom
channels.telegram.groupPolicy
channels.telegram.mediaMaxMb
channels.telegram.linkPreview
channels.telegram.proxy
channels.telegram.webhookSecret
channels.telegram.webhookUrl
channels.telegram.webhookHost
Live stream preview:
optional
channels.telegram.streamMode
sends a temporary message and updates it with
editMessageText
. This is separate from channel block streaming.
Tests:
grammy mocks cover DM + group mention gating and outbound send; more media/webhook fixtures still welcome.
Open questions
Optional grammY plugins (throttler) if we hit Bot API 429s.
Add more structured media tests (stickers, voice notes).
Make webhook listen port configurable (currently fixed to 8787 unless wired through the gateway).
Token Use and Costs
TypeBox

---
## Channels > Group Messages

[Source: https://docs.openclaw.ai/channels/group-messages]

Group Messages - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Configuration
Group Messages
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
Chat Channels
Messaging platforms
WhatsApp
Telegram
Discord
IRC
Slack
Feishu
Google Chat
Mattermost
Signal
iMessage
Microsoft Teams
LINE
Matrix
Zalo
Zalo Personal
Configuration
Pairing
Group Messages
Groups
Broadcast Groups
Channel Routing
Channel Location Parsing
Channel Troubleshooting
Group messages (WhatsApp web channel)
What’s implemented (2025-12-03)
Config example (WhatsApp)
Activation command (owner-only)
How to use
Testing / verification
Known considerations
Configuration
Group Messages
Group messages (WhatsApp web channel)
Goal: let Clawd sit in WhatsApp groups, wake up only when pinged, and keep that thread separate from the personal DM session.
Note:
agents.list[].groupChat.mentionPatterns
is now used by Telegram/Discord/Slack/iMessage as well; this doc focuses on WhatsApp-specific behavior. For multi-agent setups, set
agents.list[].groupChat.mentionPatterns
per agent (or use
messages.groupChat.mentionPatterns
as a global fallback).
What’s implemented (2025-12-03)
Activation modes:
mention
(default) or
always
mention
requires a ping (real WhatsApp @-mentions via
mentionedJids
, regex patterns, or the bot’s E.164 anywhere in the text).
always
wakes the agent on every message but it should reply only when it can add meaningful value; otherwise it returns the silent token
NO_REPLY
. Defaults can be set in config (
channels.whatsapp.groups
) and overridden per group via
/activation
. When
channels.whatsapp.groups
is set, it also acts as a group allowlist (include
&quot;*&quot;
to allow all).
Group policy:
channels.whatsapp.groupPolicy
controls whether group messages are accepted (
open|disabled|allowlist
allowlist
uses
channels.whatsapp.groupAllowFrom
(fallback: explicit
channels.whatsapp.allowFrom
). Default is
allowlist
(blocked until you add senders).
Per-group sessions: session keys look like
agent:&lt;agentId&gt;:whatsapp:group:&lt;jid&gt;
so commands such as
/verbose on
/think high
(sent as standalone messages) are scoped to that group; personal DM state is untouched. Heartbeats are skipped for group threads.
Context injection:
pending-only
group messages (default 50) that
did not
trigger a run are prefixed under
[Chat messages since your last reply - for context]
, with the triggering line under
[Current message - respond to this]
. Messages already in the session are not re-injected.
Sender surfacing: every group batch now ends with
[from: Sender Name (+E164)]
so Pi knows who is speaking.
Ephemeral/view-once: we unwrap those before extracting text/mentions, so pings inside them still trigger.
Group system prompt: on the first turn of a group session (and whenever
/activation
changes the mode) we inject a short blurb into the system prompt like
You are replying inside the WhatsApp group &quot;&lt;subject&gt;&quot;. Group members: Alice (+44...), Bob (+43...), … Activation: trigger-only … Address the specific sender noted in the message context.
If metadata isn’t available we still tell the agent it’s a group chat.
Config example (WhatsApp)
Add a
groupChat
block to
~/.openclaw/openclaw.json
so display-name pings work even when WhatsApp strips the visual
in the text body:
Copy
channels
whatsapp
groups
&quot;*&quot;
requireMention
true
agents
list
&quot;main&quot;
groupChat
historyLimit
mentionPatterns
&quot;@?openclaw&quot;
&quot;\\+?15555550123&quot;
Notes:
The regexes are case-insensitive; they cover a display-name ping like
@openclaw
and the raw number with or without
/spaces.
WhatsApp still sends canonical mentions via
mentionedJids
when someone taps the contact, so the number fallback is rarely needed but is a useful safety net.
Activation command (owner-only)
Use the group chat command:
/activation mention
/activation always
Only the owner number (from
channels.whatsapp.allowFrom
, or the bot’s own E.164 when unset) can change this. Send
/status
as a standalone message in the group to see the current activation mode.
How to use
Add your WhatsApp account (the one running OpenClaw) to the group.
Say
@openclaw …
(or include the number). Only allowlisted senders can trigger it unless you set
groupPolicy: &quot;open&quot;
The agent prompt will include recent group context plus the trailing
[from: …]
marker so it can address the right person.
Session-level directives (
/verbose on
/think high
/new
/reset
/compact
) apply only to that group’s session; send them as standalone messages so they register. Your personal DM session remains independent.
Testing / verification
Manual smoke:
Send an
@openclaw
ping in the group and confirm a reply that references the sender name.
Send a second ping and verify the history block is included then cleared on the next turn.
Check gateway logs (run with
--verbose
) to see
inbound web message
entries showing
from: &lt;groupJid&gt;
and the
[from: …]
suffix.
Known considerations
Heartbeats are intentionally skipped for groups to avoid noisy broadcasts.
Echo suppression uses the combined batch string; if you send identical text twice without mentions, only the first will get a response.
Session store entries will appear as
agent:&lt;agentId&gt;:whatsapp:group:&lt;jid&gt;
in the session store (
~/.openclaw/agents/&lt;agentId&gt;/sessions/sessions.json
by default); a missing entry just means the group hasn’t triggered a run yet.
Typing indicators in groups follow
agents.defaults.typingMode
(default:
message
when unmentioned).
Pairing
Groups

---
## Channels > Groups

[Source: https://docs.openclaw.ai/channels/groups]

Groups - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Configuration
Groups
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
Chat Channels
Messaging platforms
WhatsApp
Telegram
Discord
IRC
Slack
Feishu
Google Chat
Mattermost
Signal
iMessage
Microsoft Teams
LINE
Matrix
Zalo
Zalo Personal
Configuration
Pairing
Group Messages
Groups
Broadcast Groups
Channel Routing
Channel Location Parsing
Channel Troubleshooting
Groups
Beginner intro (2 minutes)
Session keys
Pattern: personal DMs + public groups (single agent)
Display labels
Group policy
Mention gating (default)
Group/channel tool restrictions (optional)
Group allowlists
Activation (owner-only)
Context fields
iMessage specifics
WhatsApp specifics
Configuration
Groups
Groups
OpenClaw treats group chats consistently across surfaces: WhatsApp, Telegram, Discord, Slack, Signal, iMessage, Microsoft Teams.
Beginner intro (2 minutes)
OpenClaw “lives” on your own messaging accounts. There is no separate WhatsApp bot user.
you
are in a group, OpenClaw can see that group and respond there.
Default behavior:
Groups are restricted (
groupPolicy: &quot;allowlist&quot;
Replies require a mention unless you explicitly disable mention gating.
Translation: allowlisted senders can trigger OpenClaw by mentioning it.
TL;DR
DM access
is controlled by
*.allowFrom
Group access
is controlled by
*.groupPolicy
+ allowlists (
*.groups
*.groupAllowFrom
Reply triggering
is controlled by mention gating (
requireMention
/activation
Quick flow (what happens to a group message):
Copy
groupPolicy? disabled -&gt; drop
groupPolicy? allowlist -&gt; group allowed? no -&gt; drop
requireMention? yes -&gt; mentioned? no -&gt; store for context only
otherwise -&gt; reply
If you want…
Goal
What to set
Allow all groups but only reply on @mentions
groups: { &quot;*&quot;: { requireMention: true } }
Disable all group replies
groupPolicy: &quot;disabled&quot;
Only specific groups
groups: { &quot;&lt;group-id&gt;&quot;: { ... } }
(no
&quot;*&quot;
key)
Only you can trigger in groups
groupPolicy: &quot;allowlist&quot;
groupAllowFrom: [&quot;+1555...&quot;]
Session keys
Group sessions use
agent:&lt;agentId&gt;:&lt;channel&gt;:group:&lt;id&gt;
session keys (rooms/channels use
agent:&lt;agentId&gt;:&lt;channel&gt;:channel:&lt;id&gt;
Telegram forum topics add
:topic:&lt;threadId&gt;
to the group id so each topic has its own session.
Direct chats use the main session (or per-sender if configured).
Heartbeats are skipped for group sessions.
Pattern: personal DMs + public groups (single agent)
Yes — this works well if your “personal” traffic is
DMs
and your “public” traffic is
groups
Why: in single-agent mode, DMs typically land in the
main
session key (
agent:main:main
), while groups always use
non-main
session keys (
agent:main:&lt;channel&gt;:group:&lt;id&gt;
). If you enable sandboxing with
mode: &quot;non-main&quot;
, those group sessions run in Docker while your main DM session stays on-host.
This gives you one agent “brain” (shared workspace + memory), but two execution postures:
DMs
: full tools (host)
Groups
: sandbox + restricted tools (Docker)
If you need truly separate workspaces/personas (“personal” and “public” must never mix), use a second agent + bindings. See
Multi-Agent Routing
Example (DMs on host, groups sandboxed + messaging-only tools):
Copy
agents
defaults
sandbox
mode
&quot;non-main&quot;
// groups/channels are non-main -&gt; sandboxed
scope
&quot;session&quot;
// strongest isolation (one container per group/channel)
workspaceAccess
&quot;none&quot;
tools
sandbox
tools
// If allow is non-empty, everything else is blocked (deny still wins).
allow
&quot;group:messaging&quot;
&quot;group:sessions&quot;
deny
&quot;group:runtime&quot;
&quot;group:fs&quot;
&quot;group:ui&quot;
&quot;nodes&quot;
&quot;cron&quot;
&quot;gateway&quot;
Want “groups can only see folder X” instead of “no host access”? Keep
workspaceAccess: &quot;none&quot;
and mount only allowlisted paths into the sandbox:
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
docker
binds
// hostPath:containerPath:mode
&quot;/home/user/FriendsShared:/data:ro&quot;
Related:
Configuration keys and defaults:
Gateway configuration
Debugging why a tool is blocked:
Sandbox vs Tool Policy vs Elevated
Bind mounts details:
Sandboxing
Display labels
UI labels use
displayName
when available, formatted as
&lt;channel&gt;:&lt;token&gt;
#room
is reserved for rooms/channels; group chats use
g-&lt;slug&gt;
(lowercase, spaces -&gt;
, keep
#@+._-
Group policy
Control how group/room messages are handled per channel:
Copy
channels
whatsapp
groupPolicy
&quot;disabled&quot;
// &quot;open&quot; | &quot;disabled&quot; | &quot;allowlist&quot;
groupAllowFrom
&quot;+15551234567&quot;
telegram
groupPolicy
&quot;disabled&quot;
groupAllowFrom
&quot;123456789&quot;
// numeric Telegram user id (wizard can resolve @username)
signal
groupPolicy
&quot;disabled&quot;
groupAllowFrom
&quot;+15551234567&quot;
imessage
groupPolicy
&quot;disabled&quot;
groupAllowFrom
&quot;chat_id:123&quot;
msteams
groupPolicy
&quot;disabled&quot;
groupAllowFrom
&quot;
[email&#160;protected]
&quot;
discord
groupPolicy
&quot;allowlist&quot;
guilds
GUILD_ID
channels
help
allow
true
} } }
slack
groupPolicy
&quot;allowlist&quot;
channels
&quot;#general&quot;
allow
true
} }
matrix
groupPolicy
&quot;allowlist&quot;
groupAllowFrom
&quot;@owner:example.org&quot;
groups
&quot;!roomId:example.org&quot;
allow
true
&quot;#alias:example.org&quot;
allow
true
Policy
Behavior
&quot;open&quot;
Groups bypass allowlists; mention-gating still applies.
&quot;disabled&quot;
Block all group messages entirely.
&quot;allowlist&quot;
Only allow groups/rooms that match the configured allowlist.
Notes:
groupPolicy
is separate from mention-gating (which requires @mentions).
WhatsApp/Telegram/Signal/iMessage/Microsoft Teams: use
groupAllowFrom
(fallback: explicit
allowFrom
Discord: allowlist uses
channels.discord.guilds.&lt;id&gt;.channels
Slack: allowlist uses
channels.slack.channels
Matrix: allowlist uses
channels.matrix.groups
(room IDs, aliases, or names). Use
channels.matrix.groupAllowFrom
to restrict senders; per-room
users
allowlists are also supported.
Group DMs are controlled separately (
channels.discord.dm.*
channels.slack.dm.*
Telegram allowlist can match user IDs (
&quot;123456789&quot;
&quot;telegram:123456789&quot;
&quot;tg:123456789&quot;
) or usernames (
&quot;@alice&quot;
&quot;alice&quot;
); prefixes are case-insensitive.
Default is
groupPolicy: &quot;allowlist&quot;
; if your group allowlist is empty, group messages are blocked.
Quick mental model (evaluation order for group messages):
groupPolicy
(open/disabled/allowlist)
group allowlists (
*.groups
*.groupAllowFrom
, channel-specific allowlist)
mention gating (
requireMention
/activation
Mention gating (default)
Group messages require a mention unless overridden per group. Defaults live per subsystem under
*.groups.&quot;*&quot;
Replying to a bot message counts as an implicit mention (when the channel supports reply metadata). This applies to Telegram, WhatsApp, Slack, Discord, and Microsoft Teams.
Copy
channels
whatsapp
groups
&quot;*&quot;
requireMention
true
&quot;
[email&#160;protected]
&quot;
requireMention
false
telegram
groups
&quot;*&quot;
requireMention
true
&quot;123456789&quot;
requireMention
false
imessage
groups
&quot;*&quot;
requireMention
true
&quot;123&quot;
requireMention
false
agents
list
&quot;main&quot;
groupChat
mentionPatterns
&quot;@openclaw&quot;
&quot;openclaw&quot;
&quot;\\+15555550123&quot;
historyLimit
Notes:
mentionPatterns
are case-insensitive regexes.
Surfaces that provide explicit mentions still pass; patterns are a fallback.
Per-agent override:
agents.list[].groupChat.mentionPatterns
(useful when multiple agents share a group).
Mention gating is only enforced when mention detection is possible (native mentions or
mentionPatterns
are configured).
Discord defaults live in
channels.discord.guilds.&quot;*&quot;
(overridable per guild/channel).
Group history context is wrapped uniformly across channels and is
pending-only
(messages skipped due to mention gating); use
messages.groupChat.historyLimit
for the global default and
channels.&lt;channel&gt;.historyLimit
(or
channels.&lt;channel&gt;.accounts.*.historyLimit
) for overrides. Set
to disable.
Group/channel tool restrictions (optional)
Some channel configs support restricting which tools are available
inside a specific group/room/channel
tools
: allow/deny tools for the whole group.
toolsBySender
: per-sender overrides within the group (keys are sender IDs/usernames/emails/phone numbers depending on the channel). Use
&quot;*&quot;
as a wildcard.
Resolution order (most specific wins):
group/channel
toolsBySender
match
group/channel
tools
default (
&quot;*&quot;
toolsBySender
match
default (
&quot;*&quot;
tools
Example (Telegram):
Copy
channels
telegram
groups
&quot;*&quot;
tools
deny
&quot;exec&quot;
] } }
&quot;-1001234567890&quot;
tools
deny
&quot;exec&quot;
&quot;read&quot;
&quot;write&quot;
] }
toolsBySender
&quot;123456789&quot;
alsoAllow
&quot;exec&quot;
] }
Notes:
Group/channel tool restrictions are applied in addition to global/agent tool policy (deny still wins).
Some channels use different nesting for rooms/channels (e.g., Discord
guilds.*.channels.*
, Slack
channels.*
, MS Teams
teams.*.channels.*
Group allowlists
When
channels.whatsapp.groups
channels.telegram.groups
, or
channels.imessage.groups
is configured, the keys act as a group allowlist. Use
&quot;*&quot;
to allow all groups while still setting default mention behavior.
Common intents (copy/paste):
Disable all group replies
Copy
channels
whatsapp
groupPolicy
&quot;disabled&quot;
} }
Allow only specific groups (WhatsApp)
Copy
channels
whatsapp
groups
&quot;
[email&#160;protected]
&quot;
requireMention
true
&quot;
[email&#160;protected]
&quot;
requireMention
false
Allow all groups but require mention (explicit)
Copy
channels
whatsapp
groups
&quot;*&quot;
requireMention
true
} }
Only the owner can trigger in groups (WhatsApp)
Copy
channels
whatsapp
groupPolicy
&quot;allowlist&quot;
groupAllowFrom
&quot;+15551234567&quot;
groups
&quot;*&quot;
requireMention
true
} }
Activation (owner-only)
Group owners can toggle per-group activation:
/activation mention
/activation always
Owner is determined by
channels.whatsapp.allowFrom
(or the bot’s self E.164 when unset). Send the command as a standalone message. Other surfaces currently ignore
/activation
Context fields
Group inbound payloads set:
ChatType=group
GroupSubject
(if known)
GroupMembers
(if known)
WasMentioned
(mention gating result)
Telegram forum topics also include
MessageThreadId
and
IsForum
The agent system prompt includes a group intro on the first turn of a new group session. It reminds the model to respond like a human, avoid Markdown tables, and avoid typing literal
sequences.
iMessage specifics
Prefer
chat_id:&lt;id&gt;
when routing or allowlisting.
List chats:
imsg chats --limit 20
Group replies always go back to the same
chat_id
WhatsApp specifics
See
Group messages
for WhatsApp-only behavior (history injection, mention handling details).
Group Messages
Broadcast Groups

---
## Channels > Imessage

[Source: https://docs.openclaw.ai/channels/imessage]

iMessage - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Messaging platforms
iMessage
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
Chat Channels
Messaging platforms
WhatsApp
Telegram
Discord
IRC
Slack
Feishu
Google Chat
Mattermost
Signal
iMessage
Microsoft Teams
LINE
Matrix
Zalo
Zalo Personal
Configuration
Pairing
Group Messages
Groups
Broadcast Groups
Channel Routing
Channel Location Parsing
Channel Troubleshooting
iMessage (legacy: imsg)
Quick setup
Requirements and permissions (macOS)
Access control and routing
Deployment patterns
Media, chunking, and delivery targets
Config writes
Troubleshooting
Configuration reference pointers
Messaging platforms
iMessage
iMessage (legacy: imsg)
For new iMessage deployments, use
BlueBubbles
The
imsg
integration is legacy and may be removed in a future release.
Status: legacy external CLI integration. Gateway spawns
imsg rpc
and communicates over JSON-RPC on stdio (no separate daemon/port).
BlueBubbles (recommended)
Preferred iMessage path for new setups.
Pairing
iMessage DMs default to pairing mode.
Configuration reference
Full iMessage field reference.
Quick setup
Local Mac (fast path)
Remote Mac over SSH
Install and verify imsg
Copy
brew
install
steipete/tap/imsg
imsg
rpc
--help
Configure OpenClaw
Copy
channels
imessage
enabled
true
cliPath
&quot;/usr/local/bin/imsg&quot;
dbPath
&quot;/Users/&lt;you&gt;/Library/Messages/chat.db&quot;
Start gateway
Copy
openclaw
gateway
Approve first DM pairing (default dmPolicy)
Copy
openclaw
pairing
list
imessage
openclaw
pairing
approve
imessage
&lt;
COD
&gt;
Pairing requests expire after 1 hour.
OpenClaw only requires a stdio-compatible
cliPath
, so you can point
cliPath
at a wrapper script that SSHes to a remote Mac and runs
imsg
Copy
#!/usr/bin/env bash
exec
ssh
gateway-host
imsg
&quot;$@&quot;
Recommended config when attachments are enabled:
Copy
channels
imessage
enabled
true
cliPath
&quot;~/.openclaw/scripts/imsg-ssh&quot;
remoteHost
&quot;user@gateway-host&quot;
// used for SCP attachment fetches
includeAttachments
true
remoteHost
is not set, OpenClaw attempts to auto-detect it by parsing the SSH wrapper script.
Requirements and permissions (macOS)
Messages must be signed in on the Mac running
imsg
Full Disk Access is required for the process context running OpenClaw/
imsg
(Messages DB access).
Automation permission is required to send messages through Messages.app.
Permissions are granted per process context. If gateway runs headless (LaunchAgent/SSH), run a one-time interactive command in that same context to trigger prompts:
Copy
imsg
chats
--limit
# or
imsg
send
&lt;
handl
&gt;
&quot;test&quot;
Access control and routing
DM policy
Group policy + mentions
Sessions and deterministic replies
channels.imessage.dmPolicy
controls direct messages:
pairing
(default)
allowlist
open
(requires
allowFrom
to include
&quot;*&quot;
disabled
Allowlist field:
channels.imessage.allowFrom
Allowlist entries can be handles or chat targets (
chat_id:*
chat_guid:*
chat_identifier:*
channels.imessage.groupPolicy
controls group handling:
allowlist
(default when configured)
open
disabled
Group sender allowlist:
channels.imessage.groupAllowFrom
Runtime fallback: if
groupAllowFrom
is unset, iMessage group sender checks fall back to
allowFrom
when available.
Mention gating for groups:
iMessage has no native mention metadata
mention detection uses regex patterns (
agents.list[].groupChat.mentionPatterns
, fallback
messages.groupChat.mentionPatterns
with no configured patterns, mention gating cannot be enforced
Control commands from authorized senders can bypass mention gating in groups.
DMs use direct routing; groups use group routing.
With default
session.dmScope=main
, iMessage DMs collapse into the agent main session.
Group sessions are isolated (
agent:&lt;agentId&gt;:imessage:group:&lt;chat_id&gt;
Replies route back to iMessage using originating channel/target metadata.
Group-ish thread behavior:
Some multi-participant iMessage threads can arrive with
is_group=false
If that
chat_id
is explicitly configured under
channels.imessage.groups
, OpenClaw treats it as group traffic (group gating + group session isolation).
Deployment patterns
Dedicated bot macOS user (separate iMessage identity)
Use a dedicated Apple ID and macOS user so bot traffic is isolated from your personal Messages profile.
Typical flow:
Create/sign in a dedicated macOS user.
Sign into Messages with the bot Apple ID in that user.
Install
imsg
in that user.
Create SSH wrapper so OpenClaw can run
imsg
in that user context.
Point
channels.imessage.accounts.&lt;id&gt;.cliPath
and
.dbPath
to that user profile.
First run may require GUI approvals (Automation + Full Disk Access) in that bot user session.
Remote Mac over Tailscale (example)
Common topology:
gateway runs on Linux/VM
iMessage +
imsg
runs on a Mac in your tailnet
cliPath
wrapper uses SSH to run
imsg
remoteHost
enables SCP attachment fetches
Example:
Copy
channels
imessage
enabled
true
cliPath
&quot;~/.openclaw/scripts/imsg-ssh&quot;
remoteHost
&quot;
[email&#160;protected]
&quot;
includeAttachments
true
dbPath
&quot;/Users/bot/Library/Messages/chat.db&quot;
Copy
#!/usr/bin/env bash
exec
ssh
[email&#160;protected]
imsg
&quot;$@&quot;
Use SSH keys so both SSH and SCP are non-interactive.
Multi-account pattern
iMessage supports per-account config under
channels.imessage.accounts
Each account can override fields such as
cliPath
dbPath
allowFrom
groupPolicy
mediaMaxMb
, and history settings.
Media, chunking, and delivery targets
Attachments and media
inbound attachment ingestion is optional:
channels.imessage.includeAttachments
remote attachment paths can be fetched via SCP when
remoteHost
is set
outbound media size uses
channels.imessage.mediaMaxMb
(default 16 MB)
Outbound chunking
text chunk limit:
channels.imessage.textChunkLimit
(default 4000)
chunk mode:
channels.imessage.chunkMode
length
(default)
newline
(paragraph-first splitting)
Addressing formats
Preferred explicit targets:
chat_id:123
(recommended for stable routing)
chat_guid:...
chat_identifier:...
Handle targets are also supported:
imessage:+1555...
sms:+1555...
[email&#160;protected]
Copy
imsg
chats
--limit
Config writes
iMessage allows channel-initiated config writes by default (for
/config set|unset
when
commands.config: true
Disable:
Copy
channels
imessage
configWrites
false
Troubleshooting
imsg not found or RPC unsupported
Validate the binary and RPC support:
Copy
imsg
rpc
--help
openclaw
channels
status
--probe
If probe reports RPC unsupported, update
imsg
DMs are ignored
Check:
channels.imessage.dmPolicy
channels.imessage.allowFrom
pairing approvals (
openclaw pairing list imessage
Group messages are ignored
Check:
channels.imessage.groupPolicy
channels.imessage.groupAllowFrom
channels.imessage.groups
allowlist behavior
mention pattern configuration (
agents.list[].groupChat.mentionPatterns
Remote attachments fail
Check:
channels.imessage.remoteHost
SSH/SCP key auth from the gateway host
remote path readability on the Mac running Messages
macOS permission prompts were missed
Re-run in an interactive GUI terminal in the same user/session context and approve prompts:
Copy
imsg
chats
--limit
imsg
send
&lt;
handl
&gt;
&quot;test&quot;
Confirm Full Disk Access + Automation are granted for the process context that runs OpenClaw/
imsg
Configuration reference pointers
Configuration reference - iMessage
Gateway configuration
Pairing
BlueBubbles
Signal
Microsoft Teams

---
## Channels > Irc

[Source: https://docs.openclaw.ai/channels/irc]

IRC - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Messaging platforms
IRC
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
Chat Channels
Messaging platforms
WhatsApp
Telegram
Discord
IRC
Slack
Feishu
Google Chat
Mattermost
Signal
iMessage
Microsoft Teams
LINE
Matrix
Zalo
Zalo Personal
Configuration
Pairing
Group Messages
Groups
Broadcast Groups
Channel Routing
Channel Location Parsing
Channel Troubleshooting
Quick start
Security defaults
Access control
Common gotcha: allowFrom is for DMs, not channels
Reply triggering (mentions)
Security note (recommended for public channels)
Same tools for everyone in the channel
Different tools per sender (owner gets more power)
NickServ
Environment variables
Troubleshooting
Messaging platforms
IRC
Connect OpenClaw to IRC channels and direct messages.
Use IRC when you want OpenClaw in classic channels (
#room
) and direct messages.
IRC ships as an extension plugin, but it is configured in the main config under
channels.irc
Quick start
Enable IRC config in
~/.openclaw/openclaw.json
Set at least:
Copy
&quot;channels&quot;
&quot;irc&quot;
&quot;enabled&quot;
true
&quot;host&quot;
&quot;irc.libera.chat&quot;
&quot;port&quot;
6697
&quot;tls&quot;
true
&quot;nick&quot;
&quot;openclaw-bot&quot;
&quot;channels&quot;
&quot;#openclaw&quot;
Start/restart gateway:
Copy
openclaw
gateway
run
Security defaults
channels.irc.dmPolicy
defaults to
&quot;pairing&quot;
channels.irc.groupPolicy
defaults to
&quot;allowlist&quot;
With
groupPolicy=&quot;allowlist&quot;
, set
channels.irc.groups
to define allowed channels.
Use TLS (
channels.irc.tls=true
) unless you intentionally accept plaintext transport.
Access control
There are two separate “gates” for IRC channels:
Channel access
groupPolicy
groups
): whether the bot accepts messages from a channel at all.
Sender access
groupAllowFrom
/ per-channel
groups[&quot;#channel&quot;].allowFrom
): who is allowed to trigger the bot inside that channel.
Config keys:
DM allowlist (DM sender access):
channels.irc.allowFrom
Group sender allowlist (channel sender access):
channels.irc.groupAllowFrom
Per-channel controls (channel + sender + mention rules):
channels.irc.groups[&quot;#channel&quot;]
channels.irc.groupPolicy=&quot;open&quot;
allows unconfigured channels (
still mention-gated by default
Allowlist entries can use nick or
nick!user@host
forms.
Common gotcha:
allowFrom
is for DMs, not channels
If you see logs like:
irc: drop group sender alice!ident@host (policy=allowlist)
…it means the sender wasn’t allowed for
group/channel
messages. Fix it by either:
setting
channels.irc.groupAllowFrom
(global for all channels), or
setting per-channel sender allowlists:
channels.irc.groups[&quot;#channel&quot;].allowFrom
Example (allow anyone in
#tuirc-dev
to talk to the bot):
Copy
channels
irc
groupPolicy
&quot;allowlist&quot;
groups
&quot;#tuirc-dev&quot;
allowFrom
&quot;*&quot;
] }
Reply triggering (mentions)
Even if a channel is allowed (via
groupPolicy
groups
) and the sender is allowed, OpenClaw defaults to
mention-gating
in group contexts.
That means you may see logs like
drop channel … (missing-mention)
unless the message includes a mention pattern that matches the bot.
To make the bot reply in an IRC channel
without needing a mention
, disable mention gating for that channel:
Copy
channels
irc
groupPolicy
&quot;allowlist&quot;
groups
&quot;#tuirc-dev&quot;
requireMention
false
allowFrom
&quot;*&quot;
Or to allow
all
IRC channels (no per-channel allowlist) and still reply without mentions:
Copy
channels
irc
groupPolicy
&quot;open&quot;
groups
&quot;*&quot;
requireMention
false
allowFrom
&quot;*&quot;
] }
Security note (recommended for public channels)
If you allow
allowFrom: [&quot;*&quot;]
in a public channel, anyone can prompt the bot.
To reduce risk, restrict tools for that channel.
Same tools for everyone in the channel
Copy
channels
irc
groups
&quot;#tuirc-dev&quot;
allowFrom
&quot;*&quot;
tools
deny
&quot;group:runtime&quot;
&quot;group:fs&quot;
&quot;gateway&quot;
&quot;nodes&quot;
&quot;cron&quot;
&quot;browser&quot;
Different tools per sender (owner gets more power)
Use
toolsBySender
to apply a stricter policy to
&quot;*&quot;
and a looser one to your nick:
Copy
channels
irc
groups
&quot;#tuirc-dev&quot;
allowFrom
&quot;*&quot;
toolsBySender
&quot;*&quot;
deny
&quot;group:runtime&quot;
&quot;group:fs&quot;
&quot;gateway&quot;
&quot;nodes&quot;
&quot;cron&quot;
&quot;browser&quot;
eigen
deny
&quot;gateway&quot;
&quot;nodes&quot;
&quot;cron&quot;
Notes:
toolsBySender
keys can be a nick (e.g.
&quot;eigen&quot;
) or a full hostmask (
&quot;
[email&#160;protected]
&quot;
) for stronger identity matching.
The first matching sender policy wins;
&quot;*&quot;
is the wildcard fallback.
For more on group access vs mention-gating (and how they interact), see:
/channels/groups
NickServ
To identify with NickServ after connect:
Copy
&quot;channels&quot;
&quot;irc&quot;
&quot;nickserv&quot;
&quot;enabled&quot;
true
&quot;service&quot;
&quot;NickServ&quot;
&quot;password&quot;
&quot;your-nickserv-password&quot;
Optional one-time registration on connect:
Copy
&quot;channels&quot;
&quot;irc&quot;
&quot;nickserv&quot;
&quot;register&quot;
true
&quot;registerEmail&quot;
&quot;
[email&#160;protected]
&quot;
Disable
register
after the nick is registered to avoid repeated REGISTER attempts.
Environment variables
Default account supports:
IRC_HOST
IRC_PORT
IRC_TLS
IRC_NICK
IRC_USERNAME
IRC_REALNAME
IRC_PASSWORD
IRC_CHANNELS
(comma-separated)
IRC_NICKSERV_PASSWORD
IRC_NICKSERV_REGISTER_EMAIL
Troubleshooting
If the bot connects but never replies in channels, verify
channels.irc.groups
and
whether mention-gating is dropping messages (
missing-mention
). If you want it to reply without pings, set
requireMention:false
for the channel.
If login fails, verify nick availability and server password.
If TLS fails on a custom network, verify host/port and certificate setup.
Discord
Slack

---
## Channels > Line

[Source: https://docs.openclaw.ai/channels/line]

LINE - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Messaging platforms
LINE
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
Chat Channels
Messaging platforms
WhatsApp
Telegram
Discord
IRC
Slack
Feishu
Google Chat
Mattermost
Signal
iMessage
Microsoft Teams
LINE
Matrix
Zalo
Zalo Personal
Configuration
Pairing
Group Messages
Groups
Broadcast Groups
Channel Routing
Channel Location Parsing
Channel Troubleshooting
LINE (plugin)
Plugin required
Setup
Configure
Access control
Message behavior
Channel data (rich messages)
Troubleshooting
Messaging platforms
LINE
LINE (plugin)
LINE connects to OpenClaw via the LINE Messaging API. The plugin runs as a webhook
receiver on the gateway and uses your channel access token + channel secret for
authentication.
Status: supported via plugin. Direct messages, group chats, media, locations, Flex
messages, template messages, and quick replies are supported. Reactions and threads
are not supported.
Plugin required
Install the LINE plugin:
Copy
openclaw
plugins
install
@openclaw/line
Local checkout (when running from a git repo):
Copy
openclaw
plugins
install
./extensions/line
Setup
Create a LINE Developers account and open the Console:
https://developers.line.biz/console/
Create (or pick) a Provider and add a
Messaging API
channel.
Copy the
Channel access token
and
Channel secret
from the channel settings.
Enable
Use webhook
in the Messaging API settings.
Set the webhook URL to your gateway endpoint (HTTPS required):
Copy
https://gateway-host/line/webhook
The gateway responds to LINE’s webhook verification (GET) and inbound events (POST).
If you need a custom path, set
channels.line.webhookPath
channels.line.accounts.&lt;id&gt;.webhookPath
and update the URL accordingly.
Configure
Minimal config:
Copy
channels
line
enabled
true
channelAccessToken
&quot;LINE_CHANNEL_ACCESS_TOKEN&quot;
channelSecret
&quot;LINE_CHANNEL_SECRET&quot;
dmPolicy
&quot;pairing&quot;
Env vars (default account only):
LINE_CHANNEL_ACCESS_TOKEN
LINE_CHANNEL_SECRET
Token/secret files:
Copy
channels
line
tokenFile
&quot;/path/to/line-token.txt&quot;
secretFile
&quot;/path/to/line-secret.txt&quot;
Multiple accounts:
Copy
channels
line
accounts
marketing
channelAccessToken
&quot;...&quot;
channelSecret
&quot;...&quot;
webhookPath
&quot;/line/marketing&quot;
Access control
Direct messages default to pairing. Unknown senders get a pairing code and their
messages are ignored until approved.
Copy
openclaw
pairing
list
line
openclaw
pairing
approve
line
&lt;
COD
&gt;
Allowlists and policies:
channels.line.dmPolicy
pairing | allowlist | open | disabled
channels.line.allowFrom
: allowlisted LINE user IDs for DMs
channels.line.groupPolicy
allowlist | open | disabled
channels.line.groupAllowFrom
: allowlisted LINE user IDs for groups
Per-group overrides:
channels.line.groups.&lt;groupId&gt;.allowFrom
LINE IDs are case-sensitive. Valid IDs look like:
User:
+ 32 hex chars
Group:
+ 32 hex chars
Room:
+ 32 hex chars
Message behavior
Text is chunked at 5000 characters.
Markdown formatting is stripped; code blocks and tables are converted into Flex
cards when possible.
Streaming responses are buffered; LINE receives full chunks with a loading
animation while the agent works.
Media downloads are capped by
channels.line.mediaMaxMb
(default 10).
Channel data (rich messages)
Use
channelData.line
to send quick replies, locations, Flex cards, or template
messages.
Copy
text
&quot;Here you go&quot;
channelData
line
quickReplies
&quot;Status&quot;
&quot;Help&quot;
location
title
&quot;Office&quot;
address
&quot;123 Main St&quot;
latitude
35.681236
longitude
139.767125
flexMessage
altText
&quot;Status card&quot;
contents
/* Flex payload */
templateMessage
type
&quot;confirm&quot;
text
&quot;Proceed?&quot;
confirmLabel
&quot;Yes&quot;
confirmData
&quot;yes&quot;
cancelLabel
&quot;No&quot;
cancelData
&quot;no&quot;
The LINE plugin also ships a
/card
command for Flex message presets:
Copy
/card info &quot;Welcome&quot; &quot;Thanks for joining!&quot;
Troubleshooting
Webhook verification fails:
ensure the webhook URL is HTTPS and the
channelSecret
matches the LINE console.
No inbound events:
confirm the webhook path matches
channels.line.webhookPath
and that the gateway is reachable from LINE.
Media download errors:
raise
channels.line.mediaMaxMb
if media exceeds the
default limit.
Microsoft Teams
Matrix

---
## Channels > Location

[Source: https://docs.openclaw.ai/channels/location]

Channel Location Parsing - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Configuration
Channel Location Parsing
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
Chat Channels
Messaging platforms
WhatsApp
Telegram
Discord
IRC
Slack
Feishu
Google Chat
Mattermost
Signal
iMessage
Microsoft Teams
LINE
Matrix
Zalo
Zalo Personal
Configuration
Pairing
Group Messages
Groups
Broadcast Groups
Channel Routing
Channel Location Parsing
Channel Troubleshooting
Channel location parsing
Text formatting
Context fields
Channel notes
Configuration
Channel Location Parsing
Channel location parsing
OpenClaw normalizes shared locations from chat channels into:
human-readable text appended to the inbound body, and
structured fields in the auto-reply context payload.
Currently supported:
Telegram
(location pins + venues + live locations)
WhatsApp
(locationMessage + liveLocationMessage)
Matrix
m.location
with
geo_uri
Text formatting
Locations are rendered as friendly lines without brackets:
Pin:
📍 48.858844, 2.294351 ±12m
Named place:
📍 Eiffel Tower — Champ de Mars, Paris (48.858844, 2.294351 ±12m)
Live share:
🛰 Live location: 48.858844, 2.294351 ±12m
If the channel includes a caption/comment, it is appended on the next line:
Copy
📍 48.858844, 2.294351 ±12m
Meet here
Context fields
When a location is present, these fields are added to
ctx
LocationLat
(number)
LocationLon
(number)
LocationAccuracy
(number, meters; optional)
LocationName
(string; optional)
LocationAddress
(string; optional)
LocationSource
pin | place | live
LocationIsLive
(boolean)
Channel notes
Telegram
: venues map to
LocationName/LocationAddress
; live locations use
live_period
WhatsApp
locationMessage.comment
and
liveLocationMessage.caption
are appended as the caption line.
Matrix
geo_uri
is parsed as a pin location; altitude is ignored and
LocationIsLive
is always false.
Channel Routing
Channel Troubleshooting

---
## Channels > Matrix

[Source: https://docs.openclaw.ai/channels/matrix]

Matrix - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Messaging platforms
Matrix
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
Chat Channels
Messaging platforms
WhatsApp
Telegram
Discord
IRC
Slack
Feishu
Google Chat
Mattermost
Signal
iMessage
Microsoft Teams
LINE
Matrix
Zalo
Zalo Personal
Configuration
Pairing
Group Messages
Groups
Broadcast Groups
Channel Routing
Channel Location Parsing
Channel Troubleshooting
Matrix (plugin)
Plugin required
Setup
Encryption (E2EE)
Multi-account
Routing model
Access control (DMs)
Rooms (groups)
Threads
Capabilities
Troubleshooting
Configuration reference (Matrix)
Messaging platforms
Matrix
Matrix (plugin)
Matrix is an open, decentralized messaging protocol. OpenClaw connects as a Matrix
user
on any homeserver, so you need a Matrix account for the bot. Once it is logged in, you can DM
the bot directly or invite it to rooms (Matrix “groups”). Beeper is a valid client option too,
but it requires E2EE to be enabled.
Status: supported via plugin (@vector-im/matrix-bot-sdk). Direct messages, rooms, threads, media, reactions,
polls (send + poll-start as text), location, and E2EE (with crypto support).
Plugin required
Matrix ships as a plugin and is not bundled with the core install.
Install via CLI (npm registry):
Copy
openclaw
plugins
install
@openclaw/matrix
Local checkout (when running from a git repo):
Copy
openclaw
plugins
install
./extensions/matrix
If you choose Matrix during configure/onboarding and a git checkout is detected,
OpenClaw will offer the local install path automatically.
Details:
Plugins
Setup
Install the Matrix plugin:
From npm:
openclaw plugins install @openclaw/matrix
From a local checkout:
openclaw plugins install ./extensions/matrix
Create a Matrix account on a homeserver:
Browse hosting options at
https://matrix.org/ecosystem/hosting/
Or host it yourself.
Get an access token for the bot account:
Use the Matrix login API with
curl
at your home server:
Copy
curl
--request
POST
--url
https://matrix.example.org/_matrix/client/v3/login
--header
&#x27;Content-Type: application/json&#x27;
--data
&#x27;{
&quot;type&quot;: &quot;m.login.password&quot;,
&quot;identifier&quot;: {
&quot;type&quot;: &quot;m.id.user&quot;,
&quot;user&quot;: &quot;your-user-name&quot;
&quot;password&quot;: &quot;your-password&quot;
}&#x27;
Replace
matrix.example.org
with your homeserver URL.
Or set
channels.matrix.userId
channels.matrix.password
: OpenClaw calls the same
login endpoint, stores the access token in
~/.openclaw/credentials/matrix/credentials.json
and reuses it on next start.
Configure credentials:
Env:
MATRIX_HOMESERVER
MATRIX_ACCESS_TOKEN
(or
MATRIX_USER_ID
MATRIX_PASSWORD
Or config:
channels.matrix.*
If both are set, config takes precedence.
With access token: user ID is fetched automatically via
/whoami
When set,
channels.matrix.userId
should be the full Matrix ID (example:
@bot:example.org
Restart the gateway (or finish onboarding).
Start a DM with the bot or invite it to a room from any Matrix client
(Element, Beeper, etc.; see
https://matrix.org/ecosystem/clients/
). Beeper requires E2EE,
so set
channels.matrix.encryption: true
and verify the device.
Minimal config (access token, user ID auto-fetched):
Copy
channels
matrix
enabled
true
homeserver
&quot;https://matrix.example.org&quot;
accessToken
&quot;syt_***&quot;
policy
&quot;pairing&quot;
E2EE config (end to end encryption enabled):
Copy
channels
matrix
enabled
true
homeserver
&quot;https://matrix.example.org&quot;
accessToken
&quot;syt_***&quot;
encryption
true
policy
&quot;pairing&quot;
Encryption (E2EE)
End-to-end encryption is
supported
via the Rust crypto SDK.
Enable with
channels.matrix.encryption: true
If the crypto module loads, encrypted rooms are decrypted automatically.
Outbound media is encrypted when sending to encrypted rooms.
On first connection, OpenClaw requests device verification from your other sessions.
Verify the device in another Matrix client (Element, etc.) to enable key sharing.
If the crypto module cannot be loaded, E2EE is disabled and encrypted rooms will not decrypt;
OpenClaw logs a warning.
If you see missing crypto module errors (for example,
@matrix-org/matrix-sdk-crypto-nodejs-*
allow build scripts for
@matrix-org/matrix-sdk-crypto-nodejs
and run
pnpm rebuild @matrix-org/matrix-sdk-crypto-nodejs
or fetch the binary with
node node_modules/@matrix-org/matrix-sdk-crypto-nodejs/download-lib.js
Crypto state is stored per account + access token in
~/.openclaw/matrix/accounts/&lt;account&gt;/&lt;homeserver&gt;__&lt;user&gt;/&lt;token-hash&gt;/crypto/
(SQLite database). Sync state lives alongside it in
bot-storage.json
If the access token (device) changes, a new store is created and the bot must be
re-verified for encrypted rooms.
Device verification:
When E2EE is enabled, the bot will request verification from your other sessions on startup.
Open Element (or another client) and approve the verification request to establish trust.
Once verified, the bot can decrypt messages in encrypted rooms.
Multi-account
Multi-account support: use
channels.matrix.accounts
with per-account credentials and optional
name
. See
gateway/configuration
for the shared pattern.
Each account runs as a separate Matrix user on any homeserver. Per-account config
inherits from the top-level
channels.matrix
settings and can override any option
(DM policy, groups, encryption, etc.).
Copy
channels
matrix
enabled
true
policy
&quot;pairing&quot;
accounts
assistant
name
&quot;Main assistant&quot;
homeserver
&quot;https://matrix.example.org&quot;
accessToken
&quot;syt_assistant_***&quot;
encryption
true
alerts
name
&quot;Alerts bot&quot;
homeserver
&quot;https://matrix.example.org&quot;
accessToken
&quot;syt_alerts_***&quot;
policy
&quot;allowlist&quot;
allowFrom
&quot;@admin:example.org&quot;
] }
Notes:
Account startup is serialized to avoid race conditions with concurrent module imports.
Env variables (
MATRIX_HOMESERVER
MATRIX_ACCESS_TOKEN
, etc.) only apply to the
default
account.
Base channel settings (DM policy, group policy, mention gating, etc.) apply to all accounts unless overridden per account.
Use
bindings[].match.accountId
to route each account to a different agent.
Crypto state is stored per account + access token (separate key stores per account).
Routing model
Replies always go back to Matrix.
DMs share the agent’s main session; rooms map to group sessions.
Access control (DMs)
Default:
channels.matrix.dm.policy = &quot;pairing&quot;
. Unknown senders get a pairing code.
Approve via:
openclaw pairing list matrix
openclaw pairing approve matrix &lt;CODE&gt;
Public DMs:
channels.matrix.dm.policy=&quot;open&quot;
plus
channels.matrix.dm.allowFrom=[&quot;*&quot;]
channels.matrix.dm.allowFrom
accepts full Matrix user IDs (example:
@user:server
). The wizard resolves display names to user IDs when directory search finds a single exact match.
Do not use display names or bare localparts (example:
&quot;Alice&quot;
&quot;alice&quot;
). They are ambiguous and are ignored for allowlist matching. Use full
@user:server
IDs.
Rooms (groups)
Default:
channels.matrix.groupPolicy = &quot;allowlist&quot;
(mention-gated). Use
channels.defaults.groupPolicy
to override the default when unset.
Allowlist rooms with
channels.matrix.groups
(room IDs or aliases; names are resolved to IDs when directory search finds a single exact match):
Copy
channels
matrix
groupPolicy
&quot;allowlist&quot;
groups
&quot;!roomId:example.org&quot;
allow
true
&quot;#alias:example.org&quot;
allow
true
groupAllowFrom
&quot;@owner:example.org&quot;
requireMention: false
enables auto-reply in that room.
groups.&quot;*&quot;
can set defaults for mention gating across rooms.
groupAllowFrom
restricts which senders can trigger the bot in rooms (full Matrix user IDs).
Per-room
users
allowlists can further restrict senders inside a specific room (use full Matrix user IDs).
The configure wizard prompts for room allowlists (room IDs, aliases, or names) and resolves names only on an exact, unique match.
On startup, OpenClaw resolves room/user names in allowlists to IDs and logs the mapping; unresolved entries are ignored for allowlist matching.
Invites are auto-joined by default; control with
channels.matrix.autoJoin
and
channels.matrix.autoJoinAllowlist
To allow
no rooms
, set
channels.matrix.groupPolicy: &quot;disabled&quot;
(or keep an empty allowlist).
Legacy key:
channels.matrix.rooms
(same shape as
groups
Threads
Reply threading is supported.
channels.matrix.threadReplies
controls whether replies stay in threads:
off
inbound
(default),
always
channels.matrix.replyToMode
controls reply-to metadata when not replying in a thread:
off
(default),
first
all
Capabilities
Feature
Status
Direct messages
✅ Supported
Rooms
✅ Supported
Threads
✅ Supported
Media
✅ Supported
E2EE
✅ Supported (crypto module required)
Reactions
✅ Supported (send/read via tools)
Polls
✅ Send supported; inbound poll starts are converted to text (responses/ends ignored)
Location
✅ Supported (geo URI; altitude ignored)
Native commands
✅ Supported
Troubleshooting
Run this ladder first:
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
Then confirm DM pairing state if needed:
Copy
openclaw
pairing
list
matrix
Common failures:
Logged in but room messages ignored: room blocked by
groupPolicy
or room allowlist.
DMs ignored: sender pending approval when
channels.matrix.dm.policy=&quot;pairing&quot;
Encrypted rooms fail: crypto support or encryption settings mismatch.
For triage flow:
/channels/troubleshooting
Configuration reference (Matrix)
Full configuration:
Configuration
Provider options:
channels.matrix.enabled
: enable/disable channel startup.
channels.matrix.homeserver
: homeserver URL.
channels.matrix.userId
: Matrix user ID (optional with access token).
channels.matrix.accessToken
: access token.
channels.matrix.password
: password for login (token stored).
channels.matrix.deviceName
: device display name.
channels.matrix.encryption
: enable E2EE (default: false).
channels.matrix.initialSyncLimit
: initial sync limit.
channels.matrix.threadReplies
off | inbound | always
(default: inbound).
channels.matrix.textChunkLimit
: outbound text chunk size (chars).
channels.matrix.chunkMode
length
(default) or
newline
to split on blank lines (paragraph boundaries) before length chunking.
channels.matrix.dm.policy
pairing | allowlist | open | disabled
(default: pairing).
channels.matrix.dm.allowFrom
: DM allowlist (full Matrix user IDs).
open
requires
&quot;*&quot;
. The wizard resolves names to IDs when possible.
channels.matrix.groupPolicy
allowlist | open | disabled
(default: allowlist).
channels.matrix.groupAllowFrom
: allowlisted senders for group messages (full Matrix user IDs).
channels.matrix.allowlistOnly
: force allowlist rules for DMs + rooms.
channels.matrix.groups
: group allowlist + per-room settings map.
channels.matrix.rooms
: legacy group allowlist/config.
channels.matrix.replyToMode
: reply-to mode for threads/tags.
channels.matrix.mediaMaxMb
: inbound/outbound media cap (MB).
channels.matrix.autoJoin
: invite handling (
always | allowlist | off
, default: always).
channels.matrix.autoJoinAllowlist
: allowed room IDs/aliases for auto-join.
channels.matrix.accounts
: multi-account configuration keyed by account ID (each account inherits top-level settings).
channels.matrix.actions
: per-action tool gating (reactions/messages/pins/memberInfo/channelInfo).
LINE
Zalo

---
## Channels > Mattermost

[Source: https://docs.openclaw.ai/channels/mattermost]

Mattermost - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Messaging platforms
Mattermost
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
Chat Channels
Messaging platforms
WhatsApp
Telegram
Discord
IRC
Slack
Feishu
Google Chat
Mattermost
Signal
iMessage
Microsoft Teams
LINE
Matrix
Zalo
Zalo Personal
Configuration
Pairing
Group Messages
Groups
Broadcast Groups
Channel Routing
Channel Location Parsing
Channel Troubleshooting
Mattermost (plugin)
Plugin required
Quick setup
Environment variables (default account)
Chat modes
Access control (DMs)
Channels (groups)
Targets for outbound delivery
Multi-account
Troubleshooting
Messaging platforms
Mattermost
Mattermost (plugin)
Status: supported via plugin (bot token + WebSocket events). Channels, groups, and DMs are supported.
Mattermost is a self-hostable team messaging platform; see the official site at
mattermost.com
for product details and downloads.
Plugin required
Mattermost ships as a plugin and is not bundled with the core install.
Install via CLI (npm registry):
Copy
openclaw
plugins
install
@openclaw/mattermost
Local checkout (when running from a git repo):
Copy
openclaw
plugins
install
./extensions/mattermost
If you choose Mattermost during configure/onboarding and a git checkout is detected,
OpenClaw will offer the local install path automatically.
Details:
Plugins
Quick setup
Install the Mattermost plugin.
Create a Mattermost bot account and copy the
bot token
Copy the Mattermost
base URL
(e.g.,
https://chat.example.com
Configure OpenClaw and start the gateway.
Minimal config:
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
Environment variables (default account)
Set these on the gateway host if you prefer env vars:
MATTERMOST_BOT_TOKEN=...
MATTERMOST_URL=https://chat.example.com
Env vars apply only to the
default
account (
default
). Other accounts must use config values.
Chat modes
Mattermost responds to DMs automatically. Channel behavior is controlled by
chatmode
oncall
(default): respond only when @mentioned in channels.
onmessage
: respond to every channel message.
onchar
: respond when a message starts with a trigger prefix.
Config example:
Copy
channels
mattermost
chatmode
&quot;onchar&quot;
oncharPrefixes
&quot;&gt;&quot;
&quot;!&quot;
Notes:
onchar
still responds to explicit @mentions.
channels.mattermost.requireMention
is honored for legacy configs but
chatmode
is preferred.
Access control (DMs)
Default:
channels.mattermost.dmPolicy = &quot;pairing&quot;
(unknown senders get a pairing code).
Approve via:
openclaw pairing list mattermost
openclaw pairing approve mattermost &lt;CODE&gt;
Public DMs:
channels.mattermost.dmPolicy=&quot;open&quot;
plus
channels.mattermost.allowFrom=[&quot;*&quot;]
Channels (groups)
Default:
channels.mattermost.groupPolicy = &quot;allowlist&quot;
(mention-gated).
Allowlist senders with
channels.mattermost.groupAllowFrom
(user IDs or
@username
Open channels:
channels.mattermost.groupPolicy=&quot;open&quot;
(mention-gated).
Targets for outbound delivery
Use these target formats with
openclaw message send
or cron/webhooks:
channel:&lt;id&gt;
for a channel
user:&lt;id&gt;
for a DM
@username
for a DM (resolved via the Mattermost API)
Bare IDs are treated as channels.
Multi-account
Mattermost supports multiple accounts under
channels.mattermost.accounts
Copy
channels
mattermost
accounts
default
name
&quot;Primary&quot;
botToken
&quot;mm-token&quot;
baseUrl
&quot;https://chat.example.com&quot;
alerts
name
&quot;Alerts&quot;
botToken
&quot;mm-token-2&quot;
baseUrl
&quot;https://alerts.example.com&quot;
Troubleshooting
No replies in channels: ensure the bot is in the channel and mention it (oncall), use a trigger prefix (onchar), or set
chatmode: &quot;onmessage&quot;
Auth errors: check the bot token, base URL, and whether the account is enabled.
Multi-account issues: env vars only apply to the
default
account.
Google Chat
Signal

---
## Channels > Msteams

[Source: https://docs.openclaw.ai/channels/msteams]

Microsoft Teams - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Messaging platforms
Microsoft Teams
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
Chat Channels
Messaging platforms
WhatsApp
Telegram
Discord
IRC
Slack
Feishu
Google Chat
Mattermost
Signal
iMessage
Microsoft Teams
LINE
Matrix
Zalo
Zalo Personal
Configuration
Pairing
Group Messages
Groups
Broadcast Groups
Channel Routing
Channel Location Parsing
Channel Troubleshooting
Microsoft Teams (plugin)
Plugin required
Quick setup (beginner)
Goals
Config writes
Access control (DMs + groups)
How it works
Azure Bot Setup (Prerequisites)
Step 1: Create Azure Bot
Step 2: Get Credentials
Step 3: Configure Messaging Endpoint
Step 4: Enable Teams Channel
Local Development (Tunneling)
Teams Developer Portal (Alternative)
Testing the Bot
Setup (minimal text-only)
History context
Current Teams RSC Permissions (Manifest)
Example Teams Manifest (redacted)
Manifest caveats (must-have fields)
Updating an existing app
Capabilities: RSC only vs Graph
With Teams RSC only (app installed, no Graph API permissions)
With Teams RSC + Microsoft Graph Application permissions
RSC vs Graph API
Graph-enabled media + history (required for channels)
Known Limitations
Webhook timeouts
Formatting
Configuration
Routing &amp; Sessions
Reply Style: Threads vs Posts
Attachments &amp; Images
Sending files in group chats
Why group chats need SharePoint
Setup
Sharing behavior
Fallback behavior
Files stored location
Polls (Adaptive Cards)
Adaptive Cards (arbitrary)
Target formats
Proactive messaging
Team and Channel IDs (Common Gotcha)
Private Channels
Troubleshooting
Common issues
Manifest upload errors
RSC permissions not working
References
Messaging platforms
Microsoft Teams
Microsoft Teams (plugin)
“Abandon all hope, ye who enter here.”
Updated: 2026-01-21
Status: text + DM attachments are supported; channel/group file sending requires
sharePointSiteId
+ Graph permissions (see
Sending files in group chats
). Polls are sent via Adaptive Cards.
Plugin required
Microsoft Teams ships as a plugin and is not bundled with the core install.
Breaking change (2026.1.15):
MS Teams moved out of core. If you use it, you must install the plugin.
Explainable: keeps core installs lighter and lets MS Teams dependencies update independently.
Install via CLI (npm registry):
Copy
openclaw
plugins
install
@openclaw/msteams
Local checkout (when running from a git repo):
Copy
openclaw
plugins
install
./extensions/msteams
If you choose Teams during configure/onboarding and a git checkout is detected,
OpenClaw will offer the local install path automatically.
Details:
Plugins
Quick setup (beginner)
Install the Microsoft Teams plugin.
Create an
Azure Bot
(App ID + client secret + tenant ID).
Configure OpenClaw with those credentials.
Expose
/api/messages
(port 3978 by default) via a public URL or tunnel.
Install the Teams app package and start the gateway.
Minimal config:
Copy
channels
msteams
enabled
true
appId
&quot;&lt;APP_ID&gt;&quot;
appPassword
&quot;&lt;APP_PASSWORD&gt;&quot;
tenantId
&quot;&lt;TENANT_ID&gt;&quot;
webhook
port
3978
path
&quot;/api/messages&quot;
Note: group chats are blocked by default (
channels.msteams.groupPolicy: &quot;allowlist&quot;
). To allow group replies, set
channels.msteams.groupAllowFrom
(or use
groupPolicy: &quot;open&quot;
to allow any member, mention-gated).
Goals
Talk to OpenClaw via Teams DMs, group chats, or channels.
Keep routing deterministic: replies always go back to the channel they arrived on.
Default to safe channel behavior (mentions required unless configured otherwise).
Config writes
By default, Microsoft Teams is allowed to write config updates triggered by
/config set|unset
(requires
commands.config: true
Disable with:
Copy
channels
msteams
configWrites
false
} }
Access control (DMs + groups)
DM access
Default:
channels.msteams.dmPolicy = &quot;pairing&quot;
. Unknown senders are ignored until approved.
channels.msteams.allowFrom
accepts AAD object IDs, UPNs, or display names. The wizard resolves names to IDs via Microsoft Graph when credentials allow.
Group access
Default:
channels.msteams.groupPolicy = &quot;allowlist&quot;
(blocked unless you add
groupAllowFrom
). Use
channels.defaults.groupPolicy
to override the default when unset.
channels.msteams.groupAllowFrom
controls which senders can trigger in group chats/channels (falls back to
channels.msteams.allowFrom
Set
groupPolicy: &quot;open&quot;
to allow any member (still mention‑gated by default).
To allow
no channels
, set
channels.msteams.groupPolicy: &quot;disabled&quot;
Example:
Copy
channels
msteams
groupPolicy
&quot;allowlist&quot;
groupAllowFrom
&quot;
[email&#160;protected]
&quot;
Teams + channel allowlist
Scope group/channel replies by listing teams and channels under
channels.msteams.teams
Keys can be team IDs or names; channel keys can be conversation IDs or names.
When
groupPolicy=&quot;allowlist&quot;
and a teams allowlist is present, only listed teams/channels are accepted (mention‑gated).
The configure wizard accepts
Team/Channel
entries and stores them for you.
On startup, OpenClaw resolves team/channel and user allowlist names to IDs (when Graph permissions allow)
and logs the mapping; unresolved entries are kept as typed.
Example:
Copy
channels
msteams
groupPolicy
&quot;allowlist&quot;
teams
&quot;My Team&quot;
channels
General
requireMention
true
How it works
Install the Microsoft Teams plugin.
Create an
Azure Bot
(App ID + secret + tenant ID).
Build a
Teams app package
that references the bot and includes the RSC permissions below.
Upload/install the Teams app into a team (or personal scope for DMs).
Configure
msteams
~/.openclaw/openclaw.json
(or env vars) and start the gateway.
The gateway listens for Bot Framework webhook traffic on
/api/messages
by default.
Azure Bot Setup (Prerequisites)
Before configuring OpenClaw, you need to create an Azure Bot resource.
Step 1: Create Azure Bot
Go to
Create Azure Bot
Fill in the
Basics
tab:
Field
Value
Bot handle
Your bot name, e.g.,
openclaw-msteams
(must be unique)
Subscription
Select your Azure subscription
Resource group
Create new or use existing
Pricing tier
Free
for dev/testing
Type of App
Single Tenant
(recommended - see note below)
Creation type
Create new Microsoft App ID
Deprecation notice:
Creation of new multi-tenant bots was deprecated after 2025-07-31. Use
Single Tenant
for new bots.
Click
Review + create
Create
(wait ~1-2 minutes)
Step 2: Get Credentials
Go to your Azure Bot resource →
Configuration
Copy
Microsoft App ID
→ this is your
appId
Click
Manage Password
→ go to the App Registration
Under
Certificates &amp; secrets
New client secret
→ copy the
Value
→ this is your
appPassword
Go to
Overview
→ copy
Directory (tenant) ID
→ this is your
tenantId
Step 3: Configure Messaging Endpoint
In Azure Bot →
Configuration
Set
Messaging endpoint
to your webhook URL:
Production:
https://your-domain.com/api/messages
Local dev: Use a tunnel (see
Local Development
below)
Step 4: Enable Teams Channel
In Azure Bot →
Channels
Click
Microsoft Teams
→ Configure → Save
Accept the Terms of Service
Local Development (Tunneling)
Teams can’t reach
localhost
. Use a tunnel for local development:
Option A: ngrok
Copy
ngrok
http
3978
# Copy the https URL, e.g., https://abc123.ngrok.io
# Set messaging endpoint to: https://abc123.ngrok.io/api/messages
Option B: Tailscale Funnel
Copy
tailscale
funnel
3978
# Use your Tailscale funnel URL as the messaging endpoint
Teams Developer Portal (Alternative)
Instead of manually creating a manifest ZIP, you can use the
Teams Developer Portal
Click
+ New app
Fill in basic info (name, description, developer info)
Go to
App features
Bot
Select
Enter a bot ID manually
and paste your Azure Bot App ID
Check scopes:
Personal
Team
Group Chat
Click
Distribute
Download app package
In Teams:
Apps
Manage your apps
Upload a custom app
→ select the ZIP
This is often easier than hand-editing JSON manifests.
Testing the Bot
Option A: Azure Web Chat (verify webhook first)
In Azure Portal → your Azure Bot resource →
Test in Web Chat
Send a message - you should see a response
This confirms your webhook endpoint works before Teams setup
Option B: Teams (after app installation)
Install the Teams app (sideload or org catalog)
Find the bot in Teams and send a DM
Check gateway logs for incoming activity
Setup (minimal text-only)
Install the Microsoft Teams plugin
From npm:
openclaw plugins install @openclaw/msteams
From a local checkout:
openclaw plugins install ./extensions/msteams
Bot registration
Create an Azure Bot (see above) and note:
App ID
Client secret (App password)
Tenant ID (single-tenant)
Teams app manifest
Include a
bot
entry with
botId = &lt;App ID&gt;
Scopes:
personal
team
groupChat
supportsFiles: true
(required for personal scope file handling).
Add RSC permissions (below).
Create icons:
outline.png
(32x32) and
color.png
(192x192).
Zip all three files together:
manifest.json
outline.png
color.png
Configure OpenClaw
Copy
&quot;msteams&quot;
&quot;enabled&quot;
true
&quot;appId&quot;
&quot;&lt;APP_ID&gt;&quot;
&quot;appPassword&quot;
&quot;&lt;APP_PASSWORD&gt;&quot;
&quot;tenantId&quot;
&quot;&lt;TENANT_ID&gt;&quot;
&quot;webhook&quot;
&quot;port&quot;
3978
&quot;path&quot;
&quot;/api/messages&quot;
You can also use environment variables instead of config keys:
MSTEAMS_APP_ID
MSTEAMS_APP_PASSWORD
MSTEAMS_TENANT_ID
Bot endpoint
Set the Azure Bot Messaging Endpoint to:
https://&lt;host&gt;:3978/api/messages
(or your chosen path/port).
Run the gateway
The Teams channel starts automatically when the plugin is installed and
msteams
config exists with credentials.
History context
channels.msteams.historyLimit
controls how many recent channel/group messages are wrapped into the prompt.
Falls back to
messages.groupChat.historyLimit
. Set
to disable (default 50).
DM history can be limited with
channels.msteams.dmHistoryLimit
(user turns). Per-user overrides:
channels.msteams.dms[&quot;&lt;user_id&gt;&quot;].historyLimit
Current Teams RSC Permissions (Manifest)
These are the
existing resourceSpecific permissions
in our Teams app manifest. They only apply inside the team/chat where the app is installed.
For channels (team scope):
ChannelMessage.Read.Group
(Application) - receive all channel messages without @mention
ChannelMessage.Send.Group
(Application)
Member.Read.Group
(Application)
Owner.Read.Group
(Application)
ChannelSettings.Read.Group
(Application)
TeamMember.Read.Group
(Application)
TeamSettings.Read.Group
(Application)
For group chats:
ChatMessage.Read.Chat
(Application) - receive all group chat messages without @mention
Example Teams Manifest (redacted)
Minimal, valid example with the required fields. Replace IDs and URLs.
Copy
&quot;$schema&quot;
&quot;https://developer.microsoft.com/en-us/json-schemas/teams/v1.23/MicrosoftTeams.schema.json&quot;
&quot;manifestVersion&quot;
&quot;1.23&quot;
&quot;version&quot;
&quot;1.0.0&quot;
&quot;id&quot;
&quot;00000000-0000-0000-0000-000000000000&quot;
&quot;name&quot;
&quot;short&quot;
&quot;OpenClaw&quot;
&quot;developer&quot;
&quot;name&quot;
&quot;Your Org&quot;
&quot;websiteUrl&quot;
&quot;https://example.com&quot;
&quot;privacyUrl&quot;
&quot;https://example.com/privacy&quot;
&quot;termsOfUseUrl&quot;
&quot;https://example.com/terms&quot;
&quot;description&quot;
&quot;short&quot;
&quot;OpenClaw in Teams&quot;
&quot;full&quot;
&quot;OpenClaw in Teams&quot;
&quot;icons&quot;
&quot;outline&quot;
&quot;outline.png&quot;
&quot;color&quot;
&quot;color.png&quot;
&quot;accentColor&quot;
&quot;#5B6DEF&quot;
&quot;bots&quot;
&quot;botId&quot;
&quot;11111111-1111-1111-1111-111111111111&quot;
&quot;scopes&quot;
&quot;personal&quot;
&quot;team&quot;
&quot;groupChat&quot;
&quot;isNotificationOnly&quot;
false
&quot;supportsCalling&quot;
false
&quot;supportsVideo&quot;
false
&quot;supportsFiles&quot;
true
&quot;webApplicationInfo&quot;
&quot;id&quot;
&quot;11111111-1111-1111-1111-111111111111&quot;
&quot;authorization&quot;
&quot;permissions&quot;
&quot;resourceSpecific&quot;
&quot;name&quot;
&quot;ChannelMessage.Read.Group&quot;
&quot;type&quot;
&quot;Application&quot;
&quot;name&quot;
&quot;ChannelMessage.Send.Group&quot;
&quot;type&quot;
&quot;Application&quot;
&quot;name&quot;
&quot;Member.Read.Group&quot;
&quot;type&quot;
&quot;Application&quot;
&quot;name&quot;
&quot;Owner.Read.Group&quot;
&quot;type&quot;
&quot;Application&quot;
&quot;name&quot;
&quot;ChannelSettings.Read.Group&quot;
&quot;type&quot;
&quot;Application&quot;
&quot;name&quot;
&quot;TeamMember.Read.Group&quot;
&quot;type&quot;
&quot;Application&quot;
&quot;name&quot;
&quot;TeamSettings.Read.Group&quot;
&quot;type&quot;
&quot;Application&quot;
&quot;name&quot;
&quot;ChatMessage.Read.Chat&quot;
&quot;type&quot;
&quot;Application&quot;
Manifest caveats (must-have fields)
bots[].botId
must
match the Azure Bot App ID.
webApplicationInfo.id
must
match the Azure Bot App ID.
bots[].scopes
must include the surfaces you plan to use (
personal
team
groupChat
bots[].supportsFiles: true
is required for file handling in personal scope.
authorization.permissions.resourceSpecific
must include channel read/send if you want channel traffic.
Updating an existing app
To update an already-installed Teams app (e.g., to add RSC permissions):
Update your
manifest.json
with the new settings
Increment the
version
field
(e.g.,
1.0.0
1.1.0
Re-zip
the manifest with icons (
manifest.json
outline.png
color.png
Upload the new zip:
Option A (Teams Admin Center):
Teams Admin Center → Teams apps → Manage apps → find your app → Upload new version
Option B (Sideload):
In Teams → Apps → Manage your apps → Upload a custom app
For team channels:
Reinstall the app in each team for new permissions to take effect
Fully quit and relaunch Teams
(not just close the window) to clear cached app metadata
Capabilities: RSC only vs Graph
With
Teams RSC only
(app installed, no Graph API permissions)
Works:
Read channel message
text
content.
Send channel message
text
content.
Receive
personal (DM)
file attachments.
Does NOT work:
Channel/group
image or file contents
(payload only includes HTML stub).
Downloading attachments stored in SharePoint/OneDrive.
Reading message history (beyond the live webhook event).
With
Teams RSC + Microsoft Graph Application permissions
Adds:
Downloading hosted contents (images pasted into messages).
Downloading file attachments stored in SharePoint/OneDrive.
Reading channel/chat message history via Graph.
RSC vs Graph API
Capability
RSC Permissions
Graph API
Real-time messages
Yes (via webhook)
No (polling only)
Historical messages
Yes (can query history)
Setup complexity
App manifest only
Requires admin consent + token flow
Works offline
No (must be running)
Yes (query anytime)
Bottom line:
RSC is for real-time listening; Graph API is for historical access. For catching up on missed messages while offline, you need Graph API with
ChannelMessage.Read.All
(requires admin consent).
Graph-enabled media + history (required for channels)
If you need images/files in
channels
or want to fetch
message history
, you must enable Microsoft Graph permissions and grant admin consent.
In Entra ID (Azure AD)
App Registration
, add Microsoft Graph
Application permissions
ChannelMessage.Read.All
(channel attachments + history)
Chat.Read.All
ChatMessage.Read.All
(group chats)
Grant admin consent
for the tenant.
Bump the Teams app
manifest version
, re-upload, and
reinstall the app in Teams
Fully quit and relaunch Teams
to clear cached app metadata.
Additional permission for user mentions:
User @mentions work out of the box for users in the conversation. However, if you want to dynamically search and mention users who are
not in the current conversation
, add
User.Read.All
(Application) permission and grant admin consent.
Known Limitations
Webhook timeouts
Teams delivers messages via HTTP webhook. If processing takes too long (e.g., slow LLM responses), you may see:
Gateway timeouts
Teams retrying the message (causing duplicates)
Dropped replies
OpenClaw handles this by returning quickly and sending replies proactively, but very slow responses may still cause issues.
Formatting
Teams markdown is more limited than Slack or Discord:
Basic formatting works:
bold
italic
code
, links
Complex markdown (tables, nested lists) may not render correctly
Adaptive Cards are supported for polls and arbitrary card sends (see below)
Configuration
Key settings (see
/gateway/configuration
for shared channel patterns):
channels.msteams.enabled
: enable/disable the channel.
channels.msteams.appId
channels.msteams.appPassword
channels.msteams.tenantId
: bot credentials.
channels.msteams.webhook.port
(default
3978
channels.msteams.webhook.path
(default
/api/messages
channels.msteams.dmPolicy
pairing | allowlist | open | disabled
(default: pairing)
channels.msteams.allowFrom
: allowlist for DMs (AAD object IDs, UPNs, or display names). The wizard resolves names to IDs during setup when Graph access is available.
channels.msteams.textChunkLimit
: outbound text chunk size.
channels.msteams.chunkMode
length
(default) or
newline
to split on blank lines (paragraph boundaries) before length chunking.
channels.msteams.mediaAllowHosts
: allowlist for inbound attachment hosts (defaults to Microsoft/Teams domains).
channels.msteams.mediaAuthAllowHosts
: allowlist for attaching Authorization headers on media retries (defaults to Graph + Bot Framework hosts).
channels.msteams.requireMention
: require @mention in channels/groups (default true).
channels.msteams.replyStyle
thread | top-level
(see
Reply Style
channels.msteams.teams.&lt;teamId&gt;.replyStyle
: per-team override.
channels.msteams.teams.&lt;teamId&gt;.requireMention
: per-team override.
channels.msteams.teams.&lt;teamId&gt;.tools
: default per-team tool policy overrides (
allow
deny
alsoAllow
) used when a channel override is missing.
channels.msteams.teams.&lt;teamId&gt;.toolsBySender
: default per-team per-sender tool policy overrides (
&quot;*&quot;
wildcard supported).
channels.msteams.teams.&lt;teamId&gt;.channels.&lt;conversationId&gt;.replyStyle
: per-channel override.
channels.msteams.teams.&lt;teamId&gt;.channels.&lt;conversationId&gt;.requireMention
: per-channel override.
channels.msteams.teams.&lt;teamId&gt;.channels.&lt;conversationId&gt;.tools
: per-channel tool policy overrides (
allow
deny
alsoAllow
channels.msteams.teams.&lt;teamId&gt;.channels.&lt;conversationId&gt;.toolsBySender
: per-channel per-sender tool policy overrides (
&quot;*&quot;
wildcard supported).
channels.msteams.sharePointSiteId
: SharePoint site ID for file uploads in group chats/channels (see
Sending files in group chats
Routing &amp; Sessions
Session keys follow the standard agent format (see
/concepts/session
Direct messages share the main session (
agent:&lt;agentId&gt;:&lt;mainKey&gt;
Channel/group messages use conversation id:
agent:&lt;agentId&gt;:msteams:channel:&lt;conversationId&gt;
agent:&lt;agentId&gt;:msteams:group:&lt;conversationId&gt;
Reply Style: Threads vs Posts
Teams recently introduced two channel UI styles over the same underlying data model:
Style
Description
Recommended
replyStyle
Posts
(classic)
Messages appear as cards with threaded replies underneath
thread
(default)
Threads
(Slack-like)
Messages flow linearly, more like Slack
top-level
The problem:
The Teams API does not expose which UI style a channel uses. If you use the wrong
replyStyle
thread
in a Threads-style channel → replies appear nested awkwardly
top-level
in a Posts-style channel → replies appear as separate top-level posts instead of in-thread
Solution:
Configure
replyStyle
per-channel based on how the channel is set up:
Copy
&quot;msteams&quot;
&quot;replyStyle&quot;
&quot;thread&quot;
&quot;teams&quot;
&quot;19:
[email&#160;protected]
&quot;
&quot;channels&quot;
&quot;19:
[email&#160;protected]
&quot;
&quot;replyStyle&quot;
&quot;top-level&quot;
Attachments &amp; Images
Current limitations:
DMs:
Images and file attachments work via Teams bot file APIs.
Channels/groups:
Attachments live in M365 storage (SharePoint/OneDrive). The webhook payload only includes an HTML stub, not the actual file bytes.
Graph API permissions are required
to download channel attachments.
Without Graph permissions, channel messages with images will be received as text-only (the image content is not accessible to the bot).
By default, OpenClaw only downloads media from Microsoft/Teams hostnames. Override with
channels.msteams.mediaAllowHosts
(use
[&quot;*&quot;]
to allow any host).
Authorization headers are only attached for hosts in
channels.msteams.mediaAuthAllowHosts
(defaults to Graph + Bot Framework hosts). Keep this list strict (avoid multi-tenant suffixes).
Sending files in group chats
Bots can send files in DMs using the FileConsentCard flow (built-in). However,
sending files in group chats/channels
requires additional setup:
Context
How files are sent
Setup needed
DMs
FileConsentCard → user accepts → bot uploads
Works out of the box
Group chats/channels
Upload to SharePoint → share link
Requires
sharePointSiteId
+ Graph permissions
Images (any context)
Base64-encoded inline
Works out of the box
Why group chats need SharePoint
Bots don’t have a personal OneDrive drive (the
/me/drive
Graph API endpoint doesn’t work for application identities). To send files in group chats/channels, the bot uploads to a
SharePoint site
and creates a sharing link.
Setup
Add Graph API permissions
in Entra ID (Azure AD) → App Registration:
Sites.ReadWrite.All
(Application) - upload files to SharePoint
Chat.Read.All
(Application) - optional, enables per-user sharing links
Grant admin consent
for the tenant.
Get your SharePoint site ID:
Copy
# Via Graph Explorer or curl with a valid token:
curl
&quot;Authorization: Bearer $TOKEN&quot;
&quot;https://graph.microsoft.com/v1.0/sites/{hostname}:/{site-path}&quot;
# Example: for a site at &quot;contoso.sharepoint.com/sites/BotFiles&quot;
curl
&quot;Authorization: Bearer $TOKEN&quot;
&quot;https://graph.microsoft.com/v1.0/sites/contoso.sharepoint.com:/sites/BotFiles&quot;
# Response includes: &quot;id&quot;: &quot;contoso.sharepoint.com,guid1,guid2&quot;
Configure OpenClaw:
Copy
channels
msteams
// ... other config ...
sharePointSiteId
&quot;contoso.sharepoint.com,guid1,guid2&quot;
Sharing behavior
Permission
Sharing behavior
Sites.ReadWrite.All
only
Organization-wide sharing link (anyone in org can access)
Sites.ReadWrite.All
Chat.Read.All
Per-user sharing link (only chat members can access)
Per-user sharing is more secure as only the chat participants can access the file. If
Chat.Read.All
permission is missing, the bot falls back to organization-wide sharing.
Fallback behavior
Scenario
Result
Group chat + file +
sharePointSiteId
configured
Upload to SharePoint, send sharing link
Group chat + file + no
sharePointSiteId
Attempt OneDrive upload (may fail), send text only
Personal chat + file
FileConsentCard flow (works without SharePoint)
Any context + image
Base64-encoded inline (works without SharePoint)
Files stored location
Uploaded files are stored in a
/OpenClawShared/
folder in the configured SharePoint site’s default document library.
Polls (Adaptive Cards)
OpenClaw sends Teams polls as Adaptive Cards (there is no native Teams poll API).
CLI:
openclaw message poll --channel msteams --target conversation:&lt;id&gt; ...
Votes are recorded by the gateway in
~/.openclaw/msteams-polls.json
The gateway must stay online to record votes.
Polls do not auto-post result summaries yet (inspect the store file if needed).
Adaptive Cards (arbitrary)
Send any Adaptive Card JSON to Teams users or conversations using the
message
tool or CLI.
The
card
parameter accepts an Adaptive Card JSON object. When
card
is provided, the message text is optional.
Agent tool:
Copy
&quot;action&quot;
&quot;send&quot;
&quot;channel&quot;
&quot;msteams&quot;
&quot;target&quot;
&quot;user:&lt;id&gt;&quot;
&quot;card&quot;
&quot;type&quot;
&quot;AdaptiveCard&quot;
&quot;version&quot;
&quot;1.5&quot;
&quot;body&quot;
&quot;type&quot;
&quot;TextBlock&quot;
&quot;text&quot;
&quot;Hello!&quot;
CLI:
Copy
openclaw
message
send
--channel
msteams
--target
&quot;conversation:19:
[email&#160;protected]
&quot;
--card
&#x27;{&quot;type&quot;:&quot;AdaptiveCard&quot;,&quot;version&quot;:&quot;1.5&quot;,&quot;body&quot;:[{&quot;type&quot;:&quot;TextBlock&quot;,&quot;text&quot;:&quot;Hello!&quot;}]}&#x27;
See
Adaptive Cards documentation
for card schema and examples. For target format details, see
Target formats
below.
Target formats
MSTeams targets use prefixes to distinguish between users and conversations:
Target type
Format
Example
User (by ID)
user:&lt;aad-object-id&gt;
user:40a1a0ed-4ff2-4164-a219-55518990c197
User (by name)
user:&lt;display-name&gt;
user:John Smith
(requires Graph API)
Group/channel
conversation:&lt;conversation-id&gt;
conversation:19:
[email&#160;protected]
Group/channel (raw)
&lt;conversation-id&gt;
19:
[email&#160;protected]
(if contains
@thread
CLI examples:
Copy
# Send to a user by ID
openclaw
message
send
--channel
msteams
--target
&quot;user:40a1a0ed-...&quot;
--message
&quot;Hello&quot;
# Send to a user by display name (triggers Graph API lookup)
openclaw
message
send
--channel
msteams
--target
&quot;user:John Smith&quot;
--message
&quot;Hello&quot;
# Send to a group chat or channel
openclaw
message
send
--channel
msteams
--target
&quot;conversation:19:
[email&#160;protected]
&quot;
--message
&quot;Hello&quot;
# Send an Adaptive Card to a conversation
openclaw
message
send
--channel
msteams
--target
&quot;conversation:19:
[email&#160;protected]
&quot;
--card
&#x27;{&quot;type&quot;:&quot;AdaptiveCard&quot;,&quot;version&quot;:&quot;1.5&quot;,&quot;body&quot;:[{&quot;type&quot;:&quot;TextBlock&quot;,&quot;text&quot;:&quot;Hello&quot;}]}&#x27;
Agent tool examples:
Copy
&quot;action&quot;
&quot;send&quot;
&quot;channel&quot;
&quot;msteams&quot;
&quot;target&quot;
&quot;user:John Smith&quot;
&quot;message&quot;
&quot;Hello!&quot;
Copy
&quot;action&quot;
&quot;send&quot;
&quot;channel&quot;
&quot;msteams&quot;
&quot;target&quot;
&quot;conversation:19:
[email&#160;protected]
&quot;
&quot;card&quot;
&quot;type&quot;
&quot;AdaptiveCard&quot;
&quot;version&quot;
&quot;1.5&quot;
&quot;body&quot;
&quot;type&quot;
&quot;TextBlock&quot;
&quot;text&quot;
&quot;Hello&quot;
Note: Without the
user:
prefix, names default to group/team resolution. Always use
user:
when targeting people by display name.
Proactive messaging
Proactive messages are only possible
after
a user has interacted, because we store conversation references at that point.
See
/gateway/configuration
for
dmPolicy
and allowlist gating.
Team and Channel IDs (Common Gotcha)
The
groupId
query parameter in Teams URLs is
NOT
the team ID used for configuration. Extract IDs from the URL path instead:
Team URL:
Copy
https://teams.microsoft.com/l/team/19%3ABk4j...%40thread.tacv2/conversations?groupId=...
└────────────────────────────┘
Team ID (URL-decode this)
Channel URL:
Copy
https://teams.microsoft.com/l/channel/19%3A15bc...%40thread.tacv2/ChannelName?groupId=...
└─────────────────────────┘
Channel ID (URL-decode this)
For config:
Team ID = path segment after
/team/
(URL-decoded, e.g.,
19:
[email&#160;protected]
Channel ID = path segment after
/channel/
(URL-decoded)
Ignore
the
groupId
query parameter
Private Channels
Bots have limited support in private channels:
Feature
Standard Channels
Private Channels
Bot installation
Yes
Limited
Real-time messages (webhook)
Yes
May not work
RSC permissions
Yes
May behave differently
@mentions
Yes
If bot is accessible
Graph API history
Yes
Yes (with permissions)
Workarounds if private channels don’t work:
Use standard channels for bot interactions
Use DMs - users can always message the bot directly
Use Graph API for historical access (requires
ChannelMessage.Read.All
Troubleshooting
Common issues
Images not showing in channels:
Graph permissions or admin consent missing. Reinstall the Teams app and fully quit/reopen Teams.
No responses in channel:
mentions are required by default; set
channels.msteams.requireMention=false
or configure per team/channel.
Version mismatch (Teams still shows old manifest):
remove + re-add the app and fully quit Teams to refresh.
401 Unauthorized from webhook:
Expected when testing manually without Azure JWT - means endpoint is reachable but auth failed. Use Azure Web Chat to test properly.
Manifest upload errors
“Icon file cannot be empty”:
The manifest references icon files that are 0 bytes. Create valid PNG icons (32x32 for
outline.png
, 192x192 for
color.png
“webApplicationInfo.Id already in use”:
The app is still installed in another team/chat. Find and uninstall it first, or wait 5-10 minutes for propagation.
“Something went wrong” on upload:
Upload via
https://admin.teams.microsoft.com
instead, open browser DevTools (F12) → Network tab, and check the response body for the actual error.
Sideload failing:
Try “Upload an app to your org’s app catalog” instead of “Upload a custom app” - this often bypasses sideload restrictions.
RSC permissions not working
Verify
webApplicationInfo.id
matches your bot’s App ID exactly
Re-upload the app and reinstall in the team/chat
Check if your org admin has blocked RSC permissions
Confirm you’re using the right scope:
ChannelMessage.Read.Group
for teams,
ChatMessage.Read.Chat
for group chats
References
Create Azure Bot
- Azure Bot setup guide
Teams Developer Portal
- create/manage Teams apps
Teams app manifest schema
Receive channel messages with RSC
RSC permissions reference
Teams bot file handling
(channel/group requires Graph)
Proactive messaging
iMessage
LINE

---
## Channels > Pairing

[Source: https://docs.openclaw.ai/channels/pairing]

Pairing - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Configuration
Pairing
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
Chat Channels
Messaging platforms
WhatsApp
Telegram
Discord
IRC
Slack
Feishu
Google Chat
Mattermost
Signal
iMessage
Microsoft Teams
LINE
Matrix
Zalo
Zalo Personal
Configuration
Pairing
Group Messages
Groups
Broadcast Groups
Channel Routing
Channel Location Parsing
Channel Troubleshooting
Pairing
1) DM pairing (inbound chat access)
Approve a sender
Where the state lives
2) Node device pairing (iOS/Android/macOS/headless nodes)
Pair via Telegram (recommended for iOS)
Approve a node device
Node pairing state storage
Notes
Related docs
Configuration
Pairing
Pairing
“Pairing” is OpenClaw’s explicit
owner approval
step.
It is used in two places:
DM pairing
(who is allowed to talk to the bot)
Node pairing
(which devices/nodes are allowed to join the gateway network)
Security context:
Security
1) DM pairing (inbound chat access)
When a channel is configured with DM policy
pairing
, unknown senders get a short code and their message is
not processed
until you approve.
Default DM policies are documented in:
Security
Pairing codes:
8 characters, uppercase, no ambiguous chars (
0O1I
Expire after 1 hour
. The bot only sends the pairing message when a new request is created (roughly once per hour per sender).
Pending DM pairing requests are capped at
3 per channel
by default; additional requests are ignored until one expires or is approved.
Approve a sender
Copy
openclaw
pairing
list
telegram
openclaw
pairing
approve
telegram
&lt;
COD
&gt;
Supported channels:
telegram
whatsapp
signal
imessage
discord
slack
feishu
Where the state lives
Stored under
~/.openclaw/credentials/
Pending requests:
&lt;channel&gt;-pairing.json
Approved allowlist store:
&lt;channel&gt;-allowFrom.json
Treat these as sensitive (they gate access to your assistant).
2) Node device pairing (iOS/Android/macOS/headless nodes)
Nodes connect to the Gateway as
devices
with
role: node
. The Gateway
creates a device pairing request that must be approved.
Pair via Telegram (recommended for iOS)
If you use the
device-pair
plugin, you can do first-time device pairing entirely from Telegram:
In Telegram, message your bot:
/pair
The bot replies with two messages: an instruction message and a separate
setup code
message (easy to copy/paste in Telegram).
On your phone, open the OpenClaw iOS app → Settings → Gateway.
Paste the setup code and connect.
Back in Telegram:
/pair approve
The setup code is a base64-encoded JSON payload that contains:
url
: the Gateway WebSocket URL (
ws://...
wss://...
token
: a short-lived pairing token
Treat the setup code like a password while it is valid.
Approve a node device
Copy
openclaw
devices
list
openclaw
devices
approve
&lt;
requestI
&gt;
openclaw
devices
reject
&lt;
requestI
&gt;
Node pairing state storage
Stored under
~/.openclaw/devices/
pending.json
(short-lived; pending requests expire)
paired.json
(paired devices + tokens)
Notes
The legacy
node.pair.*
API (CLI:
openclaw nodes pending/approve
) is a
separate gateway-owned pairing store. WS nodes still require device pairing.
Related docs
Security model + prompt injection:
Security
Updating safely (run doctor):
Updating
Channel configs:
Telegram:
Telegram
WhatsApp:
WhatsApp
Signal:
Signal
BlueBubbles (iMessage):
BlueBubbles
iMessage (legacy):
iMessage
Discord:
Discord
Slack:
Slack
Zalo Personal
Group Messages

---
## Channels > Signal

[Source: https://docs.openclaw.ai/channels/signal]

Signal - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Messaging platforms
Signal
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
Chat Channels
Messaging platforms
WhatsApp
Telegram
Discord
IRC
Slack
Feishu
Google Chat
Mattermost
Signal
iMessage
Microsoft Teams
LINE
Matrix
Zalo
Zalo Personal
Configuration
Pairing
Group Messages
Groups
Broadcast Groups
Channel Routing
Channel Location Parsing
Channel Troubleshooting
Signal (signal-cli)
Prerequisites
Quick setup (beginner)
What it is
Config writes
The number model (important)
Setup path A: link existing Signal account (QR)
Setup path B: register dedicated bot number (SMS, Linux)
External daemon mode (httpUrl)
Access control (DMs + groups)
How it works (behavior)
Media + limits
Typing + read receipts
Reactions (message tool)
Delivery targets (CLI/cron)
Troubleshooting
Security notes
Configuration reference (Signal)
Messaging platforms
Signal
Signal (signal-cli)
Status: external CLI integration. Gateway talks to
signal-cli
over HTTP JSON-RPC + SSE.
Prerequisites
OpenClaw installed on your server (Linux flow below tested on Ubuntu 24).
signal-cli
available on the host where the gateway runs.
A phone number that can receive one verification SMS (for SMS registration path).
Browser access for Signal captcha (
signalcaptchas.org
) during registration.
Quick setup (beginner)
Use a
separate Signal number
for the bot (recommended).
Install
signal-cli
(Java required if you use the JVM build).
Choose one setup path:
Path A (QR link):
signal-cli link -n &quot;OpenClaw&quot;
and scan with Signal.
Path B (SMS register):
register a dedicated number with captcha + SMS verification.
Configure OpenClaw and restart the gateway.
Send a first DM and approve pairing (
openclaw pairing approve signal &lt;CODE&gt;
Minimal config:
Copy
channels
signal
enabled
true
account
&quot;+15551234567&quot;
cliPath
&quot;signal-cli&quot;
dmPolicy
&quot;pairing&quot;
allowFrom
&quot;+15557654321&quot;
Field reference:
Field
Description
account
Bot phone number in E.164 format (
+15551234567
cliPath
Path to
signal-cli
signal-cli
if on
PATH
dmPolicy
DM access policy (
pairing
recommended)
allowFrom
Phone numbers or
uuid:&lt;id&gt;
values allowed to DM
What it is
Signal channel via
signal-cli
(not embedded libsignal).
Deterministic routing: replies always go back to Signal.
DMs share the agent’s main session; groups are isolated (
agent:&lt;agentId&gt;:signal:group:&lt;groupId&gt;
Config writes
By default, Signal is allowed to write config updates triggered by
/config set|unset
(requires
commands.config: true
Disable with:
Copy
channels
signal
configWrites
false
} }
The number model (important)
The gateway connects to a
Signal device
(the
signal-cli
account).
If you run the bot on
your personal Signal account
, it will ignore your own messages (loop protection).
For “I text the bot and it replies,” use a
separate bot number
Setup path A: link existing Signal account (QR)
Install
signal-cli
(JVM or native build).
Link a bot account:
signal-cli link -n &quot;OpenClaw&quot;
then scan the QR in Signal.
Configure Signal and start the gateway.
Example:
Copy
channels
signal
enabled
true
account
&quot;+15551234567&quot;
cliPath
&quot;signal-cli&quot;
dmPolicy
&quot;pairing&quot;
allowFrom
&quot;+15557654321&quot;
Multi-account support: use
channels.signal.accounts
with per-account config and optional
name
. See
gateway/configuration
for the shared pattern.
Setup path B: register dedicated bot number (SMS, Linux)
Use this when you want a dedicated bot number instead of linking an existing Signal app account.
Get a number that can receive SMS (or voice verification for landlines).
Use a dedicated bot number to avoid account/session conflicts.
Install
signal-cli
on the gateway host:
Copy
VERSION
curl
-Ls
/dev/null
%{url_effective}
https://github.com/AsamK/signal-cli/releases/latest
sed
&#x27;s/^.*\/v//&#x27;
curl
&quot;https://github.com/AsamK/signal-cli/releases/download/v${VERSION}/signal-cli-${VERSION}-Linux-native.tar.gz&quot;
sudo
tar
&quot;signal-cli-${VERSION}-Linux-native.tar.gz&quot;
/opt
sudo
-sf
/opt/signal-cli
/usr/local/bin/
signal-cli
--version
If you use the JVM build (
signal-cli-${VERSION}.tar.gz
), install JRE 25+ first.
Keep
signal-cli
updated; upstream notes that old releases can break as Signal server APIs change.
Register and verify the number:
Copy
signal-cli
&lt;
BOT_PHONE_NUMBE
&gt;
register
If captcha is required:
Open
https://signalcaptchas.org/registration/generate.html
Complete captcha, copy the
signalcaptcha://...
link target from “Open Signal”.
Run from the same external IP as the browser session when possible.
Run registration again immediately (captcha tokens expire quickly):
Copy
signal-cli
&lt;
BOT_PHONE_NUMBE
&gt;
register
--captcha
&#x27;&lt;SIGNALCAPTCHA_URL&gt;&#x27;
signal-cli
&lt;
BOT_PHONE_NUMBE
&gt;
verify
&lt;
VERIFICATION_COD
&gt;
Configure OpenClaw, restart gateway, verify channel:
Copy
# If you run the gateway as a user systemd service:
systemctl
--user
restart
openclaw-gateway
# Then verify:
openclaw
doctor
openclaw
channels
status
--probe
Pair your DM sender:
Send any message to the bot number.
Approve code on the server:
openclaw pairing approve signal &lt;PAIRING_CODE&gt;
Save the bot number as a contact on your phone to avoid “Unknown contact”.
Important: registering a phone number account with
signal-cli
can de-authenticate the main Signal app session for that number. Prefer a dedicated bot number, or use QR link mode if you need to keep your existing phone app setup.
Upstream references:
signal-cli
README:
https://github.com/AsamK/signal-cli
Captcha flow:
https://github.com/AsamK/signal-cli/wiki/Registration-with-captcha
Linking flow:
https://github.com/AsamK/signal-cli/wiki/Linking-other-devices-(Provisioning)
External daemon mode (httpUrl)
If you want to manage
signal-cli
yourself (slow JVM cold starts, container init, or shared CPUs), run the daemon separately and point OpenClaw at it:
Copy
channels
signal
httpUrl
&quot;http://127.0.0.1:8080&quot;
autoStart
false
This skips auto-spawn and the startup wait inside OpenClaw. For slow starts when auto-spawning, set
channels.signal.startupTimeoutMs
Access control (DMs + groups)
DMs:
Default:
channels.signal.dmPolicy = &quot;pairing&quot;
Unknown senders receive a pairing code; messages are ignored until approved (codes expire after 1 hour).
Approve via:
openclaw pairing list signal
openclaw pairing approve signal &lt;CODE&gt;
Pairing is the default token exchange for Signal DMs. Details:
Pairing
UUID-only senders (from
sourceUuid
) are stored as
uuid:&lt;id&gt;
channels.signal.allowFrom
Groups:
channels.signal.groupPolicy = open | allowlist | disabled
channels.signal.groupAllowFrom
controls who can trigger in groups when
allowlist
is set.
How it works (behavior)
signal-cli
runs as a daemon; the gateway reads events via SSE.
Inbound messages are normalized into the shared channel envelope.
Replies always route back to the same number or group.
Media + limits
Outbound text is chunked to
channels.signal.textChunkLimit
(default 4000).
Optional newline chunking: set
channels.signal.chunkMode=&quot;newline&quot;
to split on blank lines (paragraph boundaries) before length chunking.
Attachments supported (base64 fetched from
signal-cli
Default media cap:
channels.signal.mediaMaxMb
(default 8).
Use
channels.signal.ignoreAttachments
to skip downloading media.
Group history context uses
channels.signal.historyLimit
(or
channels.signal.accounts.*.historyLimit
), falling back to
messages.groupChat.historyLimit
. Set
to disable (default 50).
Typing + read receipts
Typing indicators
: OpenClaw sends typing signals via
signal-cli sendTyping
and refreshes them while a reply is running.
Read receipts
: when
channels.signal.sendReadReceipts
is true, OpenClaw forwards read receipts for allowed DMs.
Signal-cli does not expose read receipts for groups.
Reactions (message tool)
Use
message action=react
with
channel=signal
Targets: sender E.164 or UUID (use
uuid:&lt;id&gt;
from pairing output; bare UUID works too).
messageId
is the Signal timestamp for the message you’re reacting to.
Group reactions require
targetAuthor
targetAuthorUuid
Examples:
Copy
message action=react channel=signal target=uuid:123e4567-e89b-12d3-a456-426614174000 messageId=1737630212345 emoji=🔥
message action=react channel=signal target=+15551234567 messageId=1737630212345 emoji=🔥 remove=true
message action=react channel=signal target=signal:group:&lt;groupId&gt; targetAuthor=uuid:&lt;sender-uuid&gt; messageId=1737630212345 emoji=✅
Config:
channels.signal.actions.reactions
: enable/disable reaction actions (default true).
channels.signal.reactionLevel
off | ack | minimal | extensive
off
ack
disables agent reactions (message tool
react
will error).
minimal
extensive
enables agent reactions and sets the guidance level.
Per-account overrides:
channels.signal.accounts.&lt;id&gt;.actions.reactions
channels.signal.accounts.&lt;id&gt;.reactionLevel
Delivery targets (CLI/cron)
DMs:
signal:+15551234567
(or plain E.164).
UUID DMs:
uuid:&lt;id&gt;
(or bare UUID).
Groups:
signal:group:&lt;groupId&gt;
Usernames:
username:&lt;name&gt;
(if supported by your Signal account).
Troubleshooting
Run this ladder first:
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
Then confirm DM pairing state if needed:
Copy
openclaw
pairing
list
signal
Common failures:
Daemon reachable but no replies: verify account/daemon settings (
httpUrl
account
) and receive mode.
DMs ignored: sender is pending pairing approval.
Group messages ignored: group sender/mention gating blocks delivery.
Config validation errors after edits: run
openclaw doctor --fix
Signal missing from diagnostics: confirm
channels.signal.enabled: true
Extra checks:
Copy
openclaw
pairing
list
signal
pgrep
-af
signal-cli
grep
&quot;signal&quot;
&quot;/tmp/openclaw/openclaw-$(
date
+%Y-%m-%d
).log&quot;
tail
-20
For triage flow:
/channels/troubleshooting
Security notes
signal-cli
stores account keys locally (typically
~/.local/share/signal-cli/data/
Back up Signal account state before server migration or rebuild.
Keep
channels.signal.dmPolicy: &quot;pairing&quot;
unless you explicitly want broader DM access.
SMS verification is only needed for registration or recovery flows, but losing control of the number/account can complicate re-registration.
Configuration reference (Signal)
Full configuration:
Configuration
Provider options:
channels.signal.enabled
: enable/disable channel startup.
channels.signal.account
: E.164 for the bot account.
channels.signal.cliPath
: path to
signal-cli
channels.signal.httpUrl
: full daemon URL (overrides host/port).
channels.signal.httpHost
channels.signal.httpPort
: daemon bind (default 127.0.0.1:8080).
channels.signal.autoStart
: auto-spawn daemon (default true if
httpUrl
unset).
channels.signal.startupTimeoutMs
: startup wait timeout in ms (cap 120000).
channels.signal.receiveMode
on-start | manual
channels.signal.ignoreAttachments
: skip attachment downloads.
channels.signal.ignoreStories
: ignore stories from the daemon.
channels.signal.sendReadReceipts
: forward read receipts.
channels.signal.dmPolicy
pairing | allowlist | open | disabled
(default: pairing).
channels.signal.allowFrom
: DM allowlist (E.164 or
uuid:&lt;id&gt;
open
requires
&quot;*&quot;
. Signal has no usernames; use phone/UUID ids.
channels.signal.groupPolicy
open | allowlist | disabled
(default: allowlist).
channels.signal.groupAllowFrom
: group sender allowlist.
channels.signal.historyLimit
: max group messages to include as context (0 disables).
channels.signal.dmHistoryLimit
: DM history limit in user turns. Per-user overrides:
channels.signal.dms[&quot;&lt;phone_or_uuid&gt;&quot;].historyLimit
channels.signal.textChunkLimit
: outbound chunk size (chars).
channels.signal.chunkMode
length
(default) or
newline
to split on blank lines (paragraph boundaries) before length chunking.
channels.signal.mediaMaxMb
: inbound/outbound media cap (MB).
Related global options:
agents.list[].groupChat.mentionPatterns
(Signal does not support native mentions).
messages.groupChat.mentionPatterns
(global fallback).
messages.responsePrefix
Mattermost
iMessage

---
## Channels > Slack

[Source: https://docs.openclaw.ai/channels/slack]

Slack - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Messaging platforms
Slack
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
Chat Channels
Messaging platforms
WhatsApp
Telegram
Discord
IRC
Slack
Feishu
Google Chat
Mattermost
Signal
iMessage
Microsoft Teams
LINE
Matrix
Zalo
Zalo Personal
Configuration
Pairing
Group Messages
Groups
Broadcast Groups
Channel Routing
Channel Location Parsing
Channel Troubleshooting
Slack
Quick setup
Token model
Access control and routing
Commands and slash behavior
Threading, sessions, and reply tags
Media, chunking, and delivery
Actions and gates
Events and operational behavior
Ack reactions
Manifest and scope checklist
Troubleshooting
Configuration reference pointers
Related
Messaging platforms
Slack
Slack
Status: production-ready for DMs + channels via Slack app integrations. Default mode is Socket Mode; HTTP Events API mode is also supported.
Pairing
Slack DMs default to pairing mode.
Slash commands
Native command behavior and command catalog.
Channel troubleshooting
Cross-channel diagnostics and repair playbooks.
Quick setup
Socket Mode (default)
HTTP Events API mode
Create Slack app and tokens
In Slack app settings:
enable
Socket Mode
create
App Token
xapp-...
) with
connections:write
install app and copy
Bot Token
xoxb-...
Configure OpenClaw
Copy
channels
slack
enabled
true
mode
&quot;socket&quot;
appToken
&quot;xapp-...&quot;
botToken
&quot;xoxb-...&quot;
Env fallback (default account only):
Copy
SLACK_APP_TOKEN
xapp-...
SLACK_BOT_TOKEN
xoxb-...
Subscribe app events
Subscribe bot events for:
app_mention
message.channels
message.groups
message.im
message.mpim
reaction_added
reaction_removed
member_joined_channel
member_left_channel
channel_rename
pin_added
pin_removed
Also enable App Home
Messages Tab
for DMs.
Start gateway
Copy
openclaw
gateway
Configure Slack app for HTTP
set mode to HTTP (
channels.slack.mode=&quot;http&quot;
copy Slack
Signing Secret
set Event Subscriptions + Interactivity + Slash command Request URL to the same webhook path (default
/slack/events
Configure OpenClaw HTTP mode
Copy
channels
slack
enabled
true
mode
&quot;http&quot;
botToken
&quot;xoxb-...&quot;
signingSecret
&quot;your-signing-secret&quot;
webhookPath
&quot;/slack/events&quot;
Use unique webhook paths for multi-account HTTP
Per-account HTTP mode is supported.
Give each account a distinct
webhookPath
so registrations do not collide.
Token model
botToken
appToken
are required for Socket Mode.
HTTP mode requires
botToken
signingSecret
Config tokens override env fallback.
SLACK_BOT_TOKEN
SLACK_APP_TOKEN
env fallback applies only to the default account.
userToken
xoxp-...
) is config-only (no env fallback) and defaults to read-only behavior (
userTokenReadOnly: true
Optional: add
chat:write.customize
if you want outgoing messages to use the active agent identity (custom
username
and icon).
icon_emoji
uses
:emoji_name:
syntax.
For actions/directory reads, user token can be preferred when configured. For writes, bot token remains preferred; user-token writes are only allowed when
userTokenReadOnly: false
and bot token is unavailable.
Access control and routing
DM policy
Channel policy
Mentions and channel users
channels.slack.dmPolicy
controls DM access (legacy:
channels.slack.dm.policy
pairing
(default)
allowlist
open
(requires
channels.slack.allowFrom
to include
&quot;*&quot;
; legacy:
channels.slack.dm.allowFrom
disabled
DM flags:
dm.enabled
(default true)
channels.slack.allowFrom
(preferred)
dm.allowFrom
(legacy)
dm.groupEnabled
(group DMs default false)
dm.groupChannels
(optional MPIM allowlist)
Pairing in DMs uses
openclaw pairing approve slack &lt;code&gt;
channels.slack.groupPolicy
controls channel handling:
open
allowlist
disabled
Channel allowlist lives under
channels.slack.channels
Runtime note: if
channels.slack
is completely missing (env-only setup) and
channels.defaults.groupPolicy
is unset, runtime falls back to
groupPolicy=&quot;open&quot;
and logs a warning.
Name/ID resolution:
channel allowlist entries and DM allowlist entries are resolved at startup when token access allows
unresolved entries are kept as configured
Channel messages are mention-gated by default.
Mention sources:
explicit app mention (
&lt;@botId&gt;
mention regex patterns (
agents.list[].groupChat.mentionPatterns
, fallback
messages.groupChat.mentionPatterns
implicit reply-to-bot thread behavior
Per-channel controls (
channels.slack.channels.&lt;id|name&gt;
requireMention
users
(allowlist)
allowBots
skills
systemPrompt
tools
toolsBySender
Commands and slash behavior
Native command auto-mode is
off
for Slack (
commands.native: &quot;auto&quot;
does not enable Slack native commands).
Enable native Slack command handlers with
channels.slack.commands.native: true
(or global
commands.native: true
When native commands are enabled, register matching slash commands in Slack (
/&lt;command&gt;
names).
If native commands are not enabled, you can run a single configured slash command via
channels.slack.slashCommand
Default slash command settings:
enabled: false
name: &quot;openclaw&quot;
sessionPrefix: &quot;slack:slash&quot;
ephemeral: true
Slash sessions use isolated keys:
agent:&lt;agentId&gt;:slack:slash:&lt;userId&gt;
and still route command execution against the target conversation session (
CommandTargetSessionKey
Threading, sessions, and reply tags
DMs route as
direct
; channels as
channel
; MPIMs as
group
With default
session.dmScope=main
, Slack DMs collapse to agent main session.
Channel sessions:
agent:&lt;agentId&gt;:slack:channel:&lt;channelId&gt;
Thread replies can create thread session suffixes (
:thread:&lt;threadTs&gt;
) when applicable.
channels.slack.thread.historyScope
default is
thread
thread.inheritParent
default is
false
channels.slack.thread.initialHistoryLimit
controls how many existing thread messages are fetched when a new thread session starts (default
; set
to disable).
Reply threading controls:
channels.slack.replyToMode
off|first|all
(default
off
channels.slack.replyToModeByChatType
: per
direct|group|channel
legacy fallback for direct chats:
channels.slack.dm.replyToMode
Manual reply tags are supported:
[[reply_to_current]]
[[reply_to:&lt;id&gt;]]
Note:
replyToMode=&quot;off&quot;
disables implicit reply threading. Explicit
[[reply_to_*]]
tags are still honored.
Media, chunking, and delivery
Inbound attachments
Slack file attachments are downloaded from Slack-hosted private URLs (token-authenticated request flow) and written to the media store when fetch succeeds and size limits permit.
Runtime inbound size cap defaults to
20MB
unless overridden by
channels.slack.mediaMaxMb
Outbound text and files
text chunks use
channels.slack.textChunkLimit
(default 4000)
channels.slack.chunkMode=&quot;newline&quot;
enables paragraph-first splitting
file sends use Slack upload APIs and can include thread replies (
thread_ts
outbound media cap follows
channels.slack.mediaMaxMb
when configured; otherwise channel sends use MIME-kind defaults from media pipeline
Delivery targets
Preferred explicit targets:
user:&lt;id&gt;
for DMs
channel:&lt;id&gt;
for channels
Slack DMs are opened via Slack conversation APIs when sending to user targets.
Actions and gates
Slack actions are controlled by
channels.slack.actions.*
Available action groups in current Slack tooling:
Group
Default
messages
enabled
reactions
enabled
pins
enabled
memberInfo
enabled
emojiList
enabled
Events and operational behavior
Message edits/deletes/thread broadcasts are mapped into system events.
Reaction add/remove events are mapped into system events.
Member join/leave, channel created/renamed, and pin add/remove events are mapped into system events.
channel_id_changed
can migrate channel config keys when
configWrites
is enabled.
Channel topic/purpose metadata is treated as untrusted context and can be injected into routing context.
Ack reactions
ackReaction
sends an acknowledgement emoji while OpenClaw is processing an inbound message.
Resolution order:
channels.slack.accounts.&lt;accountId&gt;.ackReaction
channels.slack.ackReaction
messages.ackReaction
agent identity emoji fallback (
agents.list[].identity.emoji
, else ”👀”)
Notes:
Slack expects shortcodes (for example
&quot;eyes&quot;
Use
&quot;&quot;
to disable the reaction for a channel or account.
Manifest and scope checklist
Slack app manifest example
Copy
&quot;display_information&quot;
&quot;name&quot;
&quot;OpenClaw&quot;
&quot;description&quot;
&quot;Slack connector for OpenClaw&quot;
&quot;features&quot;
&quot;bot_user&quot;
&quot;display_name&quot;
&quot;OpenClaw&quot;
&quot;always_online&quot;
false
&quot;app_home&quot;
&quot;messages_tab_enabled&quot;
true
&quot;messages_tab_read_only_enabled&quot;
false
&quot;slash_commands&quot;
&quot;command&quot;
&quot;/openclaw&quot;
&quot;description&quot;
&quot;Send a message to OpenClaw&quot;
&quot;should_escape&quot;
false
&quot;oauth_config&quot;
&quot;scopes&quot;
&quot;bot&quot;
&quot;chat:write&quot;
&quot;channels:history&quot;
&quot;channels:read&quot;
&quot;groups:history&quot;
&quot;im:history&quot;
&quot;mpim:history&quot;
&quot;users:read&quot;
&quot;app_mentions:read&quot;
&quot;reactions:read&quot;
&quot;reactions:write&quot;
&quot;pins:read&quot;
&quot;pins:write&quot;
&quot;emoji:read&quot;
&quot;commands&quot;
&quot;files:read&quot;
&quot;files:write&quot;
&quot;settings&quot;
&quot;socket_mode_enabled&quot;
true
&quot;event_subscriptions&quot;
&quot;bot_events&quot;
&quot;app_mention&quot;
&quot;message.channels&quot;
&quot;message.groups&quot;
&quot;message.im&quot;
&quot;message.mpim&quot;
&quot;reaction_added&quot;
&quot;reaction_removed&quot;
&quot;member_joined_channel&quot;
&quot;member_left_channel&quot;
&quot;channel_rename&quot;
&quot;pin_added&quot;
&quot;pin_removed&quot;
Optional user-token scopes (read operations)
If you configure
channels.slack.userToken
, typical read scopes are:
channels:history
groups:history
im:history
mpim:history
channels:read
groups:read
im:read
mpim:read
users:read
reactions:read
pins:read
emoji:read
search:read
(if you depend on Slack search reads)
Troubleshooting
No replies in channels
Check, in order:
groupPolicy
channel allowlist (
channels.slack.channels
requireMention
per-channel
users
allowlist
Useful commands:
Copy
openclaw
channels
status
--probe
openclaw
logs
--follow
openclaw
doctor
DM messages ignored
Check:
channels.slack.dm.enabled
channels.slack.dmPolicy
(or legacy
channels.slack.dm.policy
pairing approvals / allowlist entries
Copy
openclaw
pairing
list
slack
Socket mode not connecting
Validate bot + app tokens and Socket Mode enablement in Slack app settings.
HTTP mode not receiving events
Validate:
signing secret
webhook path
Slack Request URLs (Events + Interactivity + Slash Commands)
unique
webhookPath
per HTTP account
Native/slash commands not firing
Verify whether you intended:
native command mode (
channels.slack.commands.native: true
) with matching slash commands registered in Slack
or single slash command mode (
channels.slack.slashCommand.enabled: true
Also check
commands.useAccessGroups
and channel/user allowlists.
Configuration reference pointers
Primary reference:
Configuration reference - Slack
High-signal Slack fields:
mode/auth:
mode
botToken
appToken
signingSecret
webhookPath
accounts.*
DM access:
dm.enabled
dmPolicy
allowFrom
(legacy:
dm.policy
dm.allowFrom
dm.groupEnabled
dm.groupChannels
channel access:
groupPolicy
channels.*
channels.*.users
channels.*.requireMention
threading/history:
replyToMode
replyToModeByChatType
thread.*
historyLimit
dmHistoryLimit
dms.*.historyLimit
delivery:
textChunkLimit
chunkMode
mediaMaxMb
ops/features:
configWrites
commands.native
slashCommand.*
actions.*
userToken
userTokenReadOnly
Related
Pairing
Channel routing
Troubleshooting
Configuration
Slash commands
IRC
Feishu

---
## Channels > Telegram

[Source: https://docs.openclaw.ai/channels/telegram]

Telegram - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Messaging platforms
Telegram
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
Chat Channels
Messaging platforms
WhatsApp
Telegram
Discord
IRC
Slack
Feishu
Google Chat
Mattermost
Signal
iMessage
Microsoft Teams
LINE
Matrix
Zalo
Zalo Personal
Configuration
Pairing
Group Messages
Groups
Broadcast Groups
Channel Routing
Channel Location Parsing
Channel Troubleshooting
Telegram (Bot API)
Quick setup
Telegram side settings
Access control and activation
Runtime behavior
Feature reference
Troubleshooting
Telegram config reference pointers
Related
Messaging platforms
Telegram
Telegram (Bot API)
Status: production-ready for bot DMs + groups via grammY. Long polling is the default mode; webhook mode is optional.
Pairing
Default DM policy for Telegram is pairing.
Channel troubleshooting
Cross-channel diagnostics and repair playbooks.
Gateway configuration
Full channel config patterns and examples.
Quick setup
Create the bot token in BotFather
Open Telegram and chat with
@BotFather
(confirm the handle is exactly
@BotFather
Run
/newbot
, follow prompts, and save the token.
Configure token and DM policy
Copy
channels
telegram
enabled
true
botToken
&quot;123:abc&quot;
dmPolicy
&quot;pairing&quot;
groups
&quot;*&quot;
requireMention
true
} }
Env fallback:
TELEGRAM_BOT_TOKEN=...
(default account only).
Start gateway and approve first DM
Copy
openclaw
gateway
openclaw
pairing
list
telegram
openclaw
pairing
approve
telegram
&lt;
COD
&gt;
Pairing codes expire after 1 hour.
Add the bot to a group
Add the bot to your group, then set
channels.telegram.groups
and
groupPolicy
to match your access model.
Token resolution order is account-aware. In practice, config values win over env fallback, and
TELEGRAM_BOT_TOKEN
only applies to the default account.
Telegram side settings
Privacy mode and group visibility
Telegram bots default to
Privacy Mode
, which limits what group messages they receive.
If the bot must see all group messages, either:
disable privacy mode via
/setprivacy
, or
make the bot a group admin.
When toggling privacy mode, remove + re-add the bot in each group so Telegram applies the change.
Group permissions
Admin status is controlled in Telegram group settings.
Admin bots receive all group messages, which is useful for always-on group behavior.
Helpful BotFather toggles
/setjoingroups
to allow/deny group adds
/setprivacy
for group visibility behavior
Access control and activation
DM policy
Group policy and allowlists
Mention behavior
channels.telegram.dmPolicy
controls direct message access:
pairing
(default)
allowlist
open
(requires
allowFrom
to include
&quot;*&quot;
disabled
channels.telegram.allowFrom
accepts numeric Telegram user IDs.
telegram:
tg:
prefixes are accepted and normalized.
The onboarding wizard accepts
@username
input and resolves it to numeric IDs.
If you upgraded and your config contains
@username
allowlist entries, run
openclaw doctor --fix
to resolve them (best-effort; requires a Telegram bot token).
Finding your Telegram user ID
Safer (no third-party bot):
DM your bot.
Run
openclaw logs --follow
Read
from.id
Official Bot API method:
Copy
curl
&quot;https://api.telegram.org/bot&lt;bot_token&gt;/getUpdates&quot;
Third-party method (less private):
@userinfobot
@getidsbot
There are two independent controls:
Which groups are allowed
channels.telegram.groups
groups
config: all groups allowed
groups
configured: acts as allowlist (explicit IDs or
&quot;*&quot;
Which senders are allowed in groups
channels.telegram.groupPolicy
open
allowlist
(default)
disabled
groupAllowFrom
is used for group sender filtering. If not set, Telegram falls back to
allowFrom
groupAllowFrom
entries must be numeric Telegram user IDs.
Example: allow any member in one specific group:
Copy
channels
telegram
groups
&quot;-1001234567890&quot;
groupPolicy
&quot;open&quot;
requireMention
false
Group replies require mention by default.
Mention can come from:
native
@botusername
mention, or
mention patterns in:
agents.list[].groupChat.mentionPatterns
messages.groupChat.mentionPatterns
Session-level command toggles:
/activation always
/activation mention
These update session state only. Use config for persistence.
Persistent config example:
Copy
channels
telegram
groups
&quot;*&quot;
requireMention
false
Getting the group chat ID:
forward a group message to
@userinfobot
@getidsbot
or read
chat.id
from
openclaw logs --follow
or inspect Bot API
getUpdates
Runtime behavior
Telegram is owned by the gateway process.
Routing is deterministic: Telegram inbound replies back to Telegram (the model does not pick channels).
Inbound messages normalize into the shared channel envelope with reply metadata and media placeholders.
Group sessions are isolated by group ID. Forum topics append
:topic:&lt;threadId&gt;
to keep topics isolated.
DM messages can carry
message_thread_id
; OpenClaw routes them with thread-aware session keys and preserves thread ID for replies.
Long polling uses grammY runner with per-chat/per-thread sequencing. Overall runner sink concurrency uses
agents.defaults.maxConcurrent
Telegram Bot API has no read-receipt support (
sendReadReceipts
does not apply).
Feature reference
Live stream preview (message edits)
OpenClaw can stream partial replies by sending a temporary Telegram message and editing it as text arrives.
Requirement:
channels.telegram.streamMode
is not
&quot;off&quot;
(default:
&quot;partial&quot;
Modes:
off
: no live preview
partial
: frequent preview updates from partial text
block
: chunked preview updates using
channels.telegram.draftChunk
draftChunk
defaults for
streamMode: &quot;block&quot;
minChars: 200
maxChars: 800
breakPreference: &quot;paragraph&quot;
maxChars
is clamped by
channels.telegram.textChunkLimit
This works in direct chats and groups/topics.
For text-only replies, OpenClaw keeps the same preview message and performs a final edit in place (no second message).
For complex replies (for example media payloads), OpenClaw falls back to normal final delivery and then cleans up the preview message.
streamMode
is separate from block streaming. When block streaming is explicitly enabled for Telegram, OpenClaw skips the preview stream to avoid double-streaming.
Telegram-only reasoning stream:
/reasoning stream
sends reasoning to the live preview while generating
final answer is sent without reasoning text
Formatting and HTML fallback
Outbound text uses Telegram
parse_mode: &quot;HTML&quot;
Markdown-ish text is rendered to Telegram-safe HTML.
Raw model HTML is escaped to reduce Telegram parse failures.
If Telegram rejects parsed HTML, OpenClaw retries as plain text.
Link previews are enabled by default and can be disabled with
channels.telegram.linkPreview: false
Native commands and custom commands
Telegram command menu registration is handled at startup with
setMyCommands
Native command defaults:
commands.native: &quot;auto&quot;
enables native commands for Telegram
Add custom command menu entries:
Copy
channels
telegram
customCommands
command
&quot;backup&quot;
description
&quot;Git backup&quot;
command
&quot;generate&quot;
description
&quot;Create an image&quot;
Rules:
names are normalized (strip leading
, lowercase)
valid pattern:
a-z
0-9
, length
1..32
custom commands cannot override native commands
conflicts/duplicates are skipped and logged
Notes:
custom commands are menu entries only; they do not auto-implement behavior
plugin/skill commands can still work when typed even if not shown in Telegram menu
If native commands are disabled, built-ins are removed. Custom/plugin commands may still register if configured.
Common setup failure:
setMyCommands failed
usually means outbound DNS/HTTPS to
api.telegram.org
is blocked.
Device pairing commands (
device-pair
plugin)
When the
device-pair
plugin is installed:
/pair
generates setup code
paste code in iOS app
/pair approve
approves latest pending request
More details:
Pairing
Inline buttons
Configure inline keyboard scope:
Copy
channels
telegram
capabilities
inlineButtons
&quot;allowlist&quot;
Per-account override:
Copy
channels
telegram
accounts
main
capabilities
inlineButtons
&quot;allowlist&quot;
Scopes:
off
group
all
allowlist
(default)
Legacy
capabilities: [&quot;inlineButtons&quot;]
maps to
inlineButtons: &quot;all&quot;
Message action example:
Copy
action
&quot;send&quot;
channel
&quot;telegram&quot;
&quot;123456789&quot;
message
&quot;Choose an option:&quot;
buttons
text
&quot;Yes&quot;
callback_data
&quot;yes&quot;
text
&quot;No&quot;
callback_data
&quot;no&quot;
text
&quot;Cancel&quot;
callback_data
&quot;cancel&quot;
Callback clicks are passed to the agent as text:
callback_data: &lt;value&gt;
Telegram message actions for agents and automation
Telegram tool actions include:
sendMessage
content
, optional
mediaUrl
replyToMessageId
messageThreadId
react
chatId
messageId
emoji
deleteMessage
chatId
messageId
editMessage
chatId
messageId
content
Channel message actions expose ergonomic aliases (
send
react
delete
edit
sticker
sticker-search
Gating controls:
channels.telegram.actions.sendMessage
channels.telegram.actions.editMessage
channels.telegram.actions.deleteMessage
channels.telegram.actions.reactions
channels.telegram.actions.sticker
(default: disabled)
Reaction removal semantics:
/tools/reactions
Reply threading tags
Telegram supports explicit reply threading tags in generated output:
[[reply_to_current]]
replies to the triggering message
[[reply_to:&lt;id&gt;]]
replies to a specific Telegram message ID
channels.telegram.replyToMode
controls handling:
off
(default)
first
all
Note:
off
disables implicit reply threading. Explicit
[[reply_to_*]]
tags are still honored.
Forum topics and thread behavior
Forum supergroups:
topic session keys append
:topic:&lt;threadId&gt;
replies and typing target the topic thread
topic config path:
channels.telegram.groups.&lt;chatId&gt;.topics.&lt;threadId&gt;
General topic (
threadId=1
) special-case:
message sends omit
message_thread_id
(Telegram rejects
sendMessage(...thread_id=1)
typing actions still include
message_thread_id
Topic inheritance: topic entries inherit group settings unless overridden (
requireMention
allowFrom
skills
systemPrompt
enabled
groupPolicy
Template context includes:
MessageThreadId
IsForum
DM thread behavior:
private chats with
message_thread_id
keep DM routing but use thread-aware session keys/reply targets.
Audio, video, and stickers
Audio messages
Telegram distinguishes voice notes vs audio files.
default: audio file behavior
tag
[[audio_as_voice]]
in agent reply to force voice-note send
Message action example:
Copy
action
&quot;send&quot;
channel
&quot;telegram&quot;
&quot;123456789&quot;
media
&quot;https://example.com/voice.ogg&quot;
asVoice
true
Video messages
Telegram distinguishes video files vs video notes.
Message action example:
Copy
action
&quot;send&quot;
channel
&quot;telegram&quot;
&quot;123456789&quot;
media
&quot;https://example.com/video.mp4&quot;
asVideoNote
true
Video notes do not support captions; provided message text is sent separately.
Stickers
Inbound sticker handling:
static WEBP: downloaded and processed (placeholder
&lt;media:sticker&gt;
animated TGS: skipped
video WEBM: skipped
Sticker context fields:
Sticker.emoji
Sticker.setName
Sticker.fileId
Sticker.fileUniqueId
Sticker.cachedDescription
Sticker cache file:
~/.openclaw/telegram/sticker-cache.json
Stickers are described once (when possible) and cached to reduce repeated vision calls.
Enable sticker actions:
Copy
channels
telegram
actions
sticker
true
Send sticker action:
Copy
action
&quot;sticker&quot;
channel
&quot;telegram&quot;
&quot;123456789&quot;
fileId
&quot;CAACAgIAAxkBAAI...&quot;
Search cached stickers:
Copy
action
&quot;sticker-search&quot;
channel
&quot;telegram&quot;
query
&quot;cat waving&quot;
limit
Reaction notifications
Telegram reactions arrive as
message_reaction
updates (separate from message payloads).
When enabled, OpenClaw enqueues system events like:
Telegram reaction added: 👍 by Alice (@alice) on msg 42
Config:
channels.telegram.reactionNotifications
off | own | all
(default:
own
channels.telegram.reactionLevel
off | ack | minimal | extensive
(default:
minimal
Notes:
own
means user reactions to bot-sent messages only (best-effort via sent-message cache).
Telegram does not provide thread IDs in reaction updates.
non-forum groups route to group chat session
forum groups route to the group general-topic session (
:topic:1
), not the exact originating topic
allowed_updates
for polling/webhook include
message_reaction
automatically.
Ack reactions
ackReaction
sends an acknowledgement emoji while OpenClaw is processing an inbound message.
Resolution order:
channels.telegram.accounts.&lt;accountId&gt;.ackReaction
channels.telegram.ackReaction
messages.ackReaction
agent identity emoji fallback (
agents.list[].identity.emoji
, else ”👀”)
Notes:
Telegram expects unicode emoji (for example ”👀”).
Use
&quot;&quot;
to disable the reaction for a channel or account.
Config writes from Telegram events and commands
Channel config writes are enabled by default (
configWrites !== false
Telegram-triggered writes include:
group migration events (
migrate_to_chat_id
) to update
channels.telegram.groups
/config set
and
/config unset
(requires command enablement)
Disable:
Copy
channels
telegram
configWrites
false
Long polling vs webhook
Default: long polling.
Webhook mode:
set
channels.telegram.webhookUrl
set
channels.telegram.webhookSecret
(required when webhook URL is set)
optional
channels.telegram.webhookPath
(default
/telegram-webhook
optional
channels.telegram.webhookHost
(default
127.0.0.1
Default local listener for webhook mode binds to
127.0.0.1:8787
If your public endpoint differs, place a reverse proxy in front and point
webhookUrl
at the public URL.
Set
webhookHost
(for example
0.0.0.0
) when you intentionally need external ingress.
Limits, retry, and CLI targets
channels.telegram.textChunkLimit
default is 4000.
channels.telegram.chunkMode=&quot;newline&quot;
prefers paragraph boundaries (blank lines) before length splitting.
channels.telegram.mediaMaxMb
(default 5) caps inbound Telegram media download/processing size.
channels.telegram.timeoutSeconds
overrides Telegram API client timeout (if unset, grammY default applies).
group context history uses
channels.telegram.historyLimit
messages.groupChat.historyLimit
(default 50);
disables.
DM history controls:
channels.telegram.dmHistoryLimit
channels.telegram.dms[&quot;&lt;user_id&gt;&quot;].historyLimit
outbound Telegram API retries are configurable via
channels.telegram.retry
CLI send target can be numeric chat ID or username:
Copy
openclaw
message
send
--channel
telegram
--target
123456789
--message
&quot;hi&quot;
openclaw
message
send
--channel
telegram
--target
@name
--message
&quot;hi&quot;
Troubleshooting
Bot does not respond to non mention group messages
requireMention=false
, Telegram privacy mode must allow full visibility.
BotFather:
/setprivacy
-&gt; Disable
then remove + re-add bot to group
openclaw channels status
warns when config expects unmentioned group messages.
openclaw channels status --probe
can check explicit numeric group IDs; wildcard
&quot;*&quot;
cannot be membership-probed.
quick session test:
/activation always
Bot not seeing group messages at all
when
channels.telegram.groups
exists, group must be listed (or include
&quot;*&quot;
verify bot membership in group
review logs:
openclaw logs --follow
for skip reasons
Commands work partially or not at all
authorize your sender identity (pairing and/or numeric
allowFrom
command authorization still applies even when group policy is
open
setMyCommands failed
usually indicates DNS/HTTPS reachability issues to
api.telegram.org
Polling or network instability
Node 22+ + custom fetch/proxy can trigger immediate abort behavior if AbortSignal types mismatch.
Some hosts resolve
api.telegram.org
to IPv6 first; broken IPv6 egress can cause intermittent Telegram API failures.
Validate DNS answers:
Copy
dig
+short
api.telegram.org
dig
+short
api.telegram.org
AAAA
More help:
Channel troubleshooting
Telegram config reference pointers
Primary reference:
channels.telegram.enabled
: enable/disable channel startup.
channels.telegram.botToken
: bot token (BotFather).
channels.telegram.tokenFile
: read token from file path.
channels.telegram.dmPolicy
pairing | allowlist | open | disabled
(default: pairing).
channels.telegram.allowFrom
: DM allowlist (numeric Telegram user IDs).
open
requires
&quot;*&quot;
openclaw doctor --fix
can resolve legacy
@username
entries to IDs.
channels.telegram.groupPolicy
open | allowlist | disabled
(default: allowlist).
channels.telegram.groupAllowFrom
: group sender allowlist (numeric Telegram user IDs).
openclaw doctor --fix
can resolve legacy
@username
entries to IDs.
channels.telegram.groups
: per-group defaults + allowlist (use
&quot;*&quot;
for global defaults).
channels.telegram.groups.&lt;id&gt;.groupPolicy
: per-group override for groupPolicy (
open | allowlist | disabled
channels.telegram.groups.&lt;id&gt;.requireMention
: mention gating default.
channels.telegram.groups.&lt;id&gt;.skills
: skill filter (omit = all skills, empty = none).
channels.telegram.groups.&lt;id&gt;.allowFrom
: per-group sender allowlist override.
channels.telegram.groups.&lt;id&gt;.systemPrompt
: extra system prompt for the group.
channels.telegram.groups.&lt;id&gt;.enabled
: disable the group when
false
channels.telegram.groups.&lt;id&gt;.topics.&lt;threadId&gt;.*
: per-topic overrides (same fields as group).
channels.telegram.groups.&lt;id&gt;.topics.&lt;threadId&gt;.groupPolicy
: per-topic override for groupPolicy (
open | allowlist | disabled
channels.telegram.groups.&lt;id&gt;.topics.&lt;threadId&gt;.requireMention
: per-topic mention gating override.
channels.telegram.capabilities.inlineButtons
off | dm | group | all | allowlist
(default: allowlist).
channels.telegram.accounts.&lt;account&gt;.capabilities.inlineButtons
: per-account override.
channels.telegram.replyToMode
off | first | all
(default:
off
channels.telegram.textChunkLimit
: outbound chunk size (chars).
channels.telegram.chunkMode
length
(default) or
newline
to split on blank lines (paragraph boundaries) before length chunking.
channels.telegram.linkPreview
: toggle link previews for outbound messages (default: true).
channels.telegram.streamMode
off | partial | block
(live stream preview).
channels.telegram.mediaMaxMb
: inbound/outbound media cap (MB).
channels.telegram.retry
: retry policy for outbound Telegram API calls (attempts, minDelayMs, maxDelayMs, jitter).
channels.telegram.network.autoSelectFamily
: override Node autoSelectFamily (true=enable, false=disable). Defaults to disabled on Node 22 to avoid Happy Eyeballs timeouts.
channels.telegram.proxy
: proxy URL for Bot API calls (SOCKS/HTTP).
channels.telegram.webhookUrl
: enable webhook mode (requires
channels.telegram.webhookSecret
channels.telegram.webhookSecret
: webhook secret (required when webhookUrl is set).
channels.telegram.webhookPath
: local webhook path (default
/telegram-webhook
channels.telegram.webhookHost
: local webhook bind host (default
127.0.0.1
channels.telegram.actions.reactions
: gate Telegram tool reactions.
channels.telegram.actions.sendMessage
: gate Telegram tool message sends.
channels.telegram.actions.deleteMessage
: gate Telegram tool message deletes.
channels.telegram.actions.sticker
: gate Telegram sticker actions — send and search (default: false).
channels.telegram.reactionNotifications
off | own | all
— control which reactions trigger system events (default:
own
when not set).
channels.telegram.reactionLevel
off | ack | minimal | extensive
— control agent’s reaction capability (default:
minimal
when not set).
Configuration reference - Telegram
Telegram-specific high-signal fields:
startup/auth:
enabled
botToken
tokenFile
accounts.*
access control:
dmPolicy
allowFrom
groupPolicy
groupAllowFrom
groups
groups.*.topics.*
command/menu:
commands.native
customCommands
threading/replies:
replyToMode
streaming:
streamMode
(preview),
draftChunk
blockStreaming
formatting/delivery:
textChunkLimit
chunkMode
linkPreview
responsePrefix
media/network:
mediaMaxMb
timeoutSeconds
retry
network.autoSelectFamily
proxy
webhook:
webhookUrl
webhookSecret
webhookPath
webhookHost
actions/capabilities:
capabilities.inlineButtons
actions.sendMessage|editMessage|deleteMessage|reactions|sticker
reactions:
reactionNotifications
reactionLevel
writes/history:
configWrites
historyLimit
dmHistoryLimit
dms.*.historyLimit
Related
Pairing
Channel routing
Troubleshooting
WhatsApp
Discord

---
## Channels > Troubleshooting

[Source: https://docs.openclaw.ai/channels/troubleshooting]

Channel Troubleshooting - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Configuration
Channel Troubleshooting
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
Chat Channels
Messaging platforms
WhatsApp
Telegram
Discord
IRC
Slack
Feishu
Google Chat
Mattermost
Signal
iMessage
Microsoft Teams
LINE
Matrix
Zalo
Zalo Personal
Configuration
Pairing
Group Messages
Groups
Broadcast Groups
Channel Routing
Channel Location Parsing
Channel Troubleshooting
Channel troubleshooting
Command ladder
WhatsApp
WhatsApp failure signatures
Telegram
Telegram failure signatures
Discord
Discord failure signatures
Slack
Slack failure signatures
iMessage and BlueBubbles
iMessage and BlueBubbles failure signatures
Signal
Signal failure signatures
Matrix
Matrix failure signatures
Configuration
Channel Troubleshooting
Channel troubleshooting
Use this page when a channel connects but behavior is wrong.
Command ladder
Run these in order first:
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
Healthy baseline:
Runtime: running
RPC probe: ok
Channel probe shows connected/ready
WhatsApp
WhatsApp failure signatures
Symptom
Fastest check
Fix
Connected but no DM replies
openclaw pairing list whatsapp
Approve sender or switch DM policy/allowlist.
Group messages ignored
Check
requireMention
+ mention patterns in config
Mention the bot or relax mention policy for that group.
Random disconnect/relogin loops
openclaw channels status --probe
+ logs
Re-login and verify credentials directory is healthy.
Full troubleshooting:
/channels/whatsapp#troubleshooting-quick
Telegram
Telegram failure signatures
Symptom
Fastest check
Fix
/start
but no usable reply flow
openclaw pairing list telegram
Approve pairing or change DM policy.
Bot online but group stays silent
Verify mention requirement and bot privacy mode
Disable privacy mode for group visibility or mention bot.
Send failures with network errors
Inspect logs for Telegram API call failures
Fix DNS/IPv6/proxy routing to
api.telegram.org
Upgraded and allowlist blocks you
openclaw security audit
and config allowlists
Run
openclaw doctor --fix
or replace
@username
with numeric sender IDs.
Full troubleshooting:
/channels/telegram#troubleshooting
Discord
Discord failure signatures
Symptom
Fastest check
Fix
Bot online but no guild replies
openclaw channels status --probe
Allow guild/channel and verify message content intent.
Group messages ignored
Check logs for mention gating drops
Mention bot or set guild/channel
requireMention: false
DM replies missing
openclaw pairing list discord
Approve DM pairing or adjust DM policy.
Full troubleshooting:
/channels/discord#troubleshooting
Slack
Slack failure signatures
Symptom
Fastest check
Fix
Socket mode connected but no responses
openclaw channels status --probe
Verify app token + bot token and required scopes.
DMs blocked
openclaw pairing list slack
Approve pairing or relax DM policy.
Channel message ignored
Check
groupPolicy
and channel allowlist
Allow the channel or switch policy to
open
Full troubleshooting:
/channels/slack#troubleshooting
iMessage and BlueBubbles
iMessage and BlueBubbles failure signatures
Symptom
Fastest check
Fix
No inbound events
Verify webhook/server reachability and app permissions
Fix webhook URL or BlueBubbles server state.
Can send but no receive on macOS
Check macOS privacy permissions for Messages automation
Re-grant TCC permissions and restart channel process.
DM sender blocked
openclaw pairing list imessage
openclaw pairing list bluebubbles
Approve pairing or update allowlist.
Full troubleshooting:
/channels/imessage#troubleshooting-macos-privacy-and-security-tcc
/channels/bluebubbles#troubleshooting
Signal
Signal failure signatures
Symptom
Fastest check
Fix
Daemon reachable but bot silent
openclaw channels status --probe
Verify
signal-cli
daemon URL/account and receive mode.
DM blocked
openclaw pairing list signal
Approve sender or adjust DM policy.
Group replies do not trigger
Check group allowlist and mention patterns
Add sender/group or loosen gating.
Full troubleshooting:
/channels/signal#troubleshooting
Matrix
Matrix failure signatures
Symptom
Fastest check
Fix
Logged in but ignores room messages
openclaw channels status --probe
Check
groupPolicy
and room allowlist.
DMs do not process
openclaw pairing list matrix
Approve sender or adjust DM policy.
Encrypted rooms fail
Verify crypto module and encryption settings
Enable encryption support and rejoin/sync room.
Full troubleshooting:
/channels/matrix#troubleshooting
Channel Location Parsing

---
## Channels > Whatsapp

[Source: https://docs.openclaw.ai/channels/whatsapp]

WhatsApp - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Messaging platforms
WhatsApp
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
Chat Channels
Messaging platforms
WhatsApp
Telegram
Discord
IRC
Slack
Feishu
Google Chat
Mattermost
Signal
iMessage
Microsoft Teams
LINE
Matrix
Zalo
Zalo Personal
Configuration
Pairing
Group Messages
Groups
Broadcast Groups
Channel Routing
Channel Location Parsing
Channel Troubleshooting
WhatsApp (Web channel)
Quick setup
Deployment patterns
Runtime model
Access control and activation
Personal-number and self-chat behavior
Message normalization and context
Delivery, chunking, and media
Acknowledgment reactions
Multi-account and credentials
Tools, actions, and config writes
Troubleshooting
Configuration reference pointers
Related
Messaging platforms
WhatsApp
WhatsApp (Web channel)
Status: production-ready via WhatsApp Web (Baileys). Gateway owns linked session(s).
Pairing
Default DM policy is pairing for unknown senders.
Channel troubleshooting
Cross-channel diagnostics and repair playbooks.
Gateway configuration
Full channel config patterns and examples.
Quick setup
Configure WhatsApp access policy
Copy
channels
whatsapp
dmPolicy
&quot;pairing&quot;
allowFrom
&quot;+15551234567&quot;
groupPolicy
&quot;allowlist&quot;
groupAllowFrom
&quot;+15551234567&quot;
Link WhatsApp (QR)
Copy
openclaw
channels
login
--channel
whatsapp
For a specific account:
Copy
openclaw
channels
login
--channel
whatsapp
--account
work
Start the gateway
Copy
openclaw
gateway
Approve first pairing request (if using pairing mode)
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
COD
&gt;
Pairing requests expire after 1 hour. Pending requests are capped at 3 per channel.
OpenClaw recommends running WhatsApp on a separate number when possible. (The channel metadata and onboarding flow are optimized for that setup, but personal-number setups are also supported.)
Deployment patterns
Dedicated number (recommended)
This is the cleanest operational mode:
separate WhatsApp identity for OpenClaw
clearer DM allowlists and routing boundaries
lower chance of self-chat confusion
Minimal policy pattern:
Copy
channels
whatsapp
dmPolicy
&quot;allowlist&quot;
allowFrom
&quot;+15551234567&quot;
Personal-number fallback
Onboarding supports personal-number mode and writes a self-chat-friendly baseline:
dmPolicy: &quot;allowlist&quot;
allowFrom
includes your personal number
selfChatMode: true
In runtime, self-chat protections key off the linked self number and
allowFrom
WhatsApp Web-only channel scope
The messaging platform channel is WhatsApp Web-based (
Baileys
) in current OpenClaw channel architecture.
There is no separate Twilio WhatsApp messaging channel in the built-in chat-channel registry.
Runtime model
Gateway owns the WhatsApp socket and reconnect loop.
Outbound sends require an active WhatsApp listener for the target account.
Status and broadcast chats are ignored (
@status
@broadcast
Direct chats use DM session rules (
session.dmScope
; default
main
collapses DMs to the agent main session).
Group sessions are isolated (
agent:&lt;agentId&gt;:whatsapp:group:&lt;jid&gt;
Access control and activation
DM policy
Group policy + allowlists
Mentions + /activation
channels.whatsapp.dmPolicy
controls direct chat access:
pairing
(default)
allowlist
open
(requires
allowFrom
to include
&quot;*&quot;
disabled
allowFrom
accepts E.164-style numbers (normalized internally).
Multi-account override:
channels.whatsapp.accounts.&lt;id&gt;.dmPolicy
(and
allowFrom
) take precedence over channel-level defaults for that account.
Runtime behavior details:
pairings are persisted in channel allow-store and merged with configured
allowFrom
if no allowlist is configured, the linked self number is allowed by default
outbound
fromMe
DMs are never auto-paired
Group access has two layers:
Group membership allowlist
channels.whatsapp.groups
groups
is omitted, all groups are eligible
groups
is present, it acts as a group allowlist (
&quot;*&quot;
allowed)
Group sender policy
channels.whatsapp.groupPolicy
groupAllowFrom
open
: sender allowlist bypassed
allowlist
: sender must match
groupAllowFrom
(or
disabled
: block all group inbound
Sender allowlist fallback:
groupAllowFrom
is unset, runtime falls back to
allowFrom
when available
Note: if no
channels.whatsapp
block exists at all, runtime group-policy fallback is effectively
open
Group replies require mention by default.
Mention detection includes:
explicit WhatsApp mentions of the bot identity
configured mention regex patterns (
agents.list[].groupChat.mentionPatterns
, fallback
messages.groupChat.mentionPatterns
implicit reply-to-bot detection (reply sender matches bot identity)
Session-level activation command:
/activation mention
/activation always
activation
updates session state (not global config). It is owner-gated.
Personal-number and self-chat behavior
When the linked self number is also present in
allowFrom
, WhatsApp self-chat safeguards activate:
skip read receipts for self-chat turns
ignore mention-JID auto-trigger behavior that would otherwise ping yourself
messages.responsePrefix
is unset, self-chat replies default to
[{identity.name}]
[openclaw]
Message normalization and context
Inbound envelope + reply context
Incoming WhatsApp messages are wrapped in the shared inbound envelope.
If a quoted reply exists, context is appended in this form:
Copy
[Replying to &lt;sender&gt; id:&lt;stanzaId&gt;]
&lt;quoted body or media placeholder&gt;
[/Replying]
Reply metadata fields are also populated when available (
ReplyToId
ReplyToBody
ReplyToSender
, sender JID/E.164).
Media placeholders and location/contact extraction
Media-only inbound messages are normalized with placeholders such as:
&lt;media:image&gt;
&lt;media:video&gt;
&lt;media:audio&gt;
&lt;media:document&gt;
&lt;media:sticker&gt;
Location and contact payloads are normalized into textual context before routing.
Pending group history injection
For groups, unprocessed messages can be buffered and injected as context when the bot is finally triggered.
default limit:
config:
channels.whatsapp.historyLimit
fallback:
messages.groupChat.historyLimit
disables
Injection markers:
[Chat messages since your last reply - for context]
[Current message - respond to this]
Read receipts
Read receipts are enabled by default for accepted inbound WhatsApp messages.
Disable globally:
Copy
channels
whatsapp
sendReadReceipts
false
Per-account override:
Copy
channels
whatsapp
accounts
work
sendReadReceipts
false
Self-chat turns skip read receipts even when globally enabled.
Delivery, chunking, and media
Text chunking
default chunk limit:
channels.whatsapp.textChunkLimit = 4000
channels.whatsapp.chunkMode = &quot;length&quot; | &quot;newline&quot;
newline
mode prefers paragraph boundaries (blank lines), then falls back to length-safe chunking
Outbound media behavior
supports image, video, audio (PTT voice-note), and document payloads
audio/ogg
is rewritten to
audio/ogg; codecs=opus
for voice-note compatibility
animated GIF playback is supported via
gifPlayback: true
on video sends
captions are applied to the first media item when sending multi-media reply payloads
media source can be HTTP(S),
file://
, or local paths
Media size limits and fallback behavior
inbound media save cap:
channels.whatsapp.mediaMaxMb
(default
outbound media cap for auto-replies:
agents.defaults.mediaMaxMb
(default
5MB
images are auto-optimized (resize/quality sweep) to fit limits
on media send failure, first-item fallback sends text warning instead of dropping the response silently
Acknowledgment reactions
WhatsApp supports immediate ack reactions on inbound receipt via
channels.whatsapp.ackReaction
Copy
channels
whatsapp
ackReaction
emoji
&quot;👀&quot;
direct
true
group
&quot;mentions&quot;
// always | mentions | never
Behavior notes:
sent immediately after inbound is accepted (pre-reply)
failures are logged but do not block normal reply delivery
group mode
mentions
reacts on mention-triggered turns; group activation
always
acts as bypass for this check
WhatsApp uses
channels.whatsapp.ackReaction
(legacy
messages.ackReaction
is not used here)
Multi-account and credentials
Account selection and defaults
account ids come from
channels.whatsapp.accounts
default account selection:
default
if present, otherwise first configured account id (sorted)
account ids are normalized internally for lookup
Credential paths and legacy compatibility
current auth path:
~/.openclaw/credentials/whatsapp/&lt;accountId&gt;/creds.json
backup file:
creds.json.bak
legacy default auth in
~/.openclaw/credentials/
is still recognized/migrated for default-account flows
Logout behavior
openclaw channels logout --channel whatsapp [--account &lt;id&gt;]
clears WhatsApp auth state for that account.
In legacy auth directories,
oauth.json
is preserved while Baileys auth files are removed.
Tools, actions, and config writes
Agent tool support includes WhatsApp reaction action (
react
Action gates:
channels.whatsapp.actions.reactions
channels.whatsapp.actions.polls
Channel-initiated config writes are enabled by default (disable via
channels.whatsapp.configWrites=false
Troubleshooting
Not linked (QR required)
Symptom: channel status reports not linked.
Fix:
Copy
openclaw
channels
login
--channel
whatsapp
openclaw
channels
status
Linked but disconnected / reconnect loop
Symptom: linked account with repeated disconnects or reconnect attempts.
Fix:
Copy
openclaw
doctor
openclaw
logs
--follow
If needed, re-link with
channels login
No active listener when sending
Outbound sends fail fast when no active gateway listener exists for the target account.
Make sure gateway is running and the account is linked.
Group messages unexpectedly ignored
Check in this order:
groupPolicy
groupAllowFrom
allowFrom
groups
allowlist entries
mention gating (
requireMention
+ mention patterns)
Bun runtime warning
WhatsApp gateway runtime should use Node. Bun is flagged as incompatible for stable WhatsApp/Telegram gateway operation.
Configuration reference pointers
Primary reference:
Configuration reference - WhatsApp
High-signal WhatsApp fields:
access:
dmPolicy
allowFrom
groupPolicy
groupAllowFrom
groups
delivery:
textChunkLimit
chunkMode
mediaMaxMb
sendReadReceipts
ackReaction
multi-account:
accounts.&lt;id&gt;.enabled
accounts.&lt;id&gt;.authDir
, account-level overrides
operations:
configWrites
debounceMs
web.enabled
web.heartbeatSeconds
web.reconnect.*
session behavior:
session.dmScope
historyLimit
dmHistoryLimit
dms.&lt;id&gt;.historyLimit
Related
Pairing
Channel routing
Troubleshooting
Chat Channels
Telegram

---
## Channels > Zalo

[Source: https://docs.openclaw.ai/channels/zalo]

Zalo - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Messaging platforms
Zalo
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
Chat Channels
Messaging platforms
WhatsApp
Telegram
Discord
IRC
Slack
Feishu
Google Chat
Mattermost
Signal
iMessage
Microsoft Teams
LINE
Matrix
Zalo
Zalo Personal
Configuration
Pairing
Group Messages
Groups
Broadcast Groups
Channel Routing
Channel Location Parsing
Channel Troubleshooting
Zalo (Bot API)
Plugin required
Quick setup (beginner)
What it is
Setup (fast path)
1) Create a bot token (Zalo Bot Platform)
2) Configure the token (env or config)
How it works (behavior)
Limits
Access control (DMs)
DM access
Long-polling vs webhook
Supported message types
Capabilities
Delivery targets (CLI/cron)
Troubleshooting
Configuration reference (Zalo)
Messaging platforms
Zalo
Zalo (Bot API)
Status: experimental. Direct messages only; groups coming soon per Zalo docs.
Plugin required
Zalo ships as a plugin and is not bundled with the core install.
Install via CLI:
openclaw plugins install @openclaw/zalo
Or select
Zalo
during onboarding and confirm the install prompt
Details:
Plugins
Quick setup (beginner)
Install the Zalo plugin:
From a source checkout:
openclaw plugins install ./extensions/zalo
From npm (if published):
openclaw plugins install @openclaw/zalo
Or pick
Zalo
in onboarding and confirm the install prompt
Set the token:
Env:
ZALO_BOT_TOKEN=...
Or config:
channels.zalo.botToken: &quot;...&quot;
Restart the gateway (or finish onboarding).
DM access is pairing by default; approve the pairing code on first contact.
Minimal config:
Copy
channels
zalo
enabled
true
botToken
&quot;12345689:abc-xyz&quot;
dmPolicy
&quot;pairing&quot;
What it is
Zalo is a Vietnam-focused messaging app; its Bot API lets the Gateway run a bot for 1:1 conversations.
It is a good fit for support or notifications where you want deterministic routing back to Zalo.
A Zalo Bot API channel owned by the Gateway.
Deterministic routing: replies go back to Zalo; the model never chooses channels.
DMs share the agent’s main session.
Groups are not yet supported (Zalo docs state “coming soon”).
Setup (fast path)
1) Create a bot token (Zalo Bot Platform)
Go to
https://bot.zaloplatforms.com
and sign in.
Create a new bot and configure its settings.
Copy the bot token (format:
12345689:abc-xyz
2) Configure the token (env or config)
Example:
Copy
channels
zalo
enabled
true
botToken
&quot;12345689:abc-xyz&quot;
dmPolicy
&quot;pairing&quot;
Env option:
ZALO_BOT_TOKEN=...
(works for the default account only).
Multi-account support: use
channels.zalo.accounts
with per-account tokens and optional
name
Restart the gateway. Zalo starts when a token is resolved (env or config).
DM access defaults to pairing. Approve the code when the bot is first contacted.
How it works (behavior)
Inbound messages are normalized into the shared channel envelope with media placeholders.
Replies always route back to the same Zalo chat.
Long-polling by default; webhook mode available with
channels.zalo.webhookUrl
Limits
Outbound text is chunked to 2000 characters (Zalo API limit).
Media downloads/uploads are capped by
channels.zalo.mediaMaxMb
(default 5).
Streaming is blocked by default due to the 2000 char limit making streaming less useful.
Access control (DMs)
DM access
Default:
channels.zalo.dmPolicy = &quot;pairing&quot;
. Unknown senders receive a pairing code; messages are ignored until approved (codes expire after 1 hour).
Approve via:
openclaw pairing list zalo
openclaw pairing approve zalo &lt;CODE&gt;
Pairing is the default token exchange. Details:
Pairing
channels.zalo.allowFrom
accepts numeric user IDs (no username lookup available).
Long-polling vs webhook
Default: long-polling (no public URL required).
Webhook mode: set
channels.zalo.webhookUrl
and
channels.zalo.webhookSecret
The webhook secret must be 8-256 characters.
Webhook URL must use HTTPS.
Zalo sends events with
X-Bot-Api-Secret-Token
header for verification.
Gateway HTTP handles webhook requests at
channels.zalo.webhookPath
(defaults to the webhook URL path).
Note:
getUpdates (polling) and webhook are mutually exclusive per Zalo API docs.
Supported message types
Text messages
: Full support with 2000 character chunking.
Image messages
: Download and process inbound images; send images via
sendPhoto
Stickers
: Logged but not fully processed (no agent response).
Unsupported types
: Logged (e.g., messages from protected users).
Capabilities
Feature
Status
Direct messages
✅ Supported
Groups
❌ Coming soon (per Zalo docs)
Media (images)
✅ Supported
Reactions
❌ Not supported
Threads
❌ Not supported
Polls
❌ Not supported
Native commands
❌ Not supported
Streaming
⚠️ Blocked (2000 char limit)
Delivery targets (CLI/cron)
Use a chat id as the target.
Example:
openclaw message send --channel zalo --target 123456789 --message &quot;hi&quot;
Troubleshooting
Bot doesn’t respond:
Check that the token is valid:
openclaw channels status --probe
Verify the sender is approved (pairing or allowFrom)
Check gateway logs:
openclaw logs --follow
Webhook not receiving events:
Ensure webhook URL uses HTTPS
Verify secret token is 8-256 characters
Confirm the gateway HTTP endpoint is reachable on the configured path
Check that getUpdates polling is not running (they’re mutually exclusive)
Configuration reference (Zalo)
Full configuration:
Configuration
Provider options:
channels.zalo.enabled
: enable/disable channel startup.
channels.zalo.botToken
: bot token from Zalo Bot Platform.
channels.zalo.tokenFile
: read token from file path.
channels.zalo.dmPolicy
pairing | allowlist | open | disabled
(default: pairing).
channels.zalo.allowFrom
: DM allowlist (user IDs).
open
requires
&quot;*&quot;
. The wizard will ask for numeric IDs.
channels.zalo.mediaMaxMb
: inbound/outbound media cap (MB, default 5).
channels.zalo.webhookUrl
: enable webhook mode (HTTPS required).
channels.zalo.webhookSecret
: webhook secret (8-256 chars).
channels.zalo.webhookPath
: webhook path on the gateway HTTP server.
channels.zalo.proxy
: proxy URL for API requests.
Multi-account options:
channels.zalo.accounts.&lt;id&gt;.botToken
: per-account token.
channels.zalo.accounts.&lt;id&gt;.tokenFile
: per-account token file.
channels.zalo.accounts.&lt;id&gt;.name
: display name.
channels.zalo.accounts.&lt;id&gt;.enabled
: enable/disable account.
channels.zalo.accounts.&lt;id&gt;.dmPolicy
: per-account DM policy.
channels.zalo.accounts.&lt;id&gt;.allowFrom
: per-account allowlist.
channels.zalo.accounts.&lt;id&gt;.webhookUrl
: per-account webhook URL.
channels.zalo.accounts.&lt;id&gt;.webhookSecret
: per-account webhook secret.
channels.zalo.accounts.&lt;id&gt;.webhookPath
: per-account webhook path.
channels.zalo.accounts.&lt;id&gt;.proxy
: per-account proxy URL.
Matrix
Zalo Personal

---
## Channels > Zalouser

[Source: https://docs.openclaw.ai/channels/zalouser]

Zalo Personal - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Messaging platforms
Zalo Personal
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
Chat Channels
Messaging platforms
WhatsApp
Telegram
Discord
IRC
Slack
Feishu
Google Chat
Mattermost
Signal
iMessage
Microsoft Teams
LINE
Matrix
Zalo
Zalo Personal
Configuration
Pairing
Group Messages
Groups
Broadcast Groups
Channel Routing
Channel Location Parsing
Channel Troubleshooting
Zalo Personal (unofficial)
Plugin required
Prerequisite: zca-cli
Quick setup (beginner)
What it is
Naming
Finding IDs (directory)
Limits
Access control (DMs)
Group access (optional)
Multi-account
Troubleshooting
Messaging platforms
Zalo Personal
Zalo Personal (unofficial)
Status: experimental. This integration automates a
personal Zalo account
via
zca-cli
Warning:
This is an unofficial integration and may result in account suspension/ban. Use at your own risk.
Plugin required
Zalo Personal ships as a plugin and is not bundled with the core install.
Install via CLI:
openclaw plugins install @openclaw/zalouser
Or from a source checkout:
openclaw plugins install ./extensions/zalouser
Details:
Plugins
Prerequisite: zca-cli
The Gateway machine must have the
zca
binary available in
PATH
Verify:
zca --version
If missing, install zca-cli (see
extensions/zalouser/README.md
or the upstream zca-cli docs).
Quick setup (beginner)
Install the plugin (see above).
Login (QR, on the Gateway machine):
openclaw channels login --channel zalouser
Scan the QR code in the terminal with the Zalo mobile app.
Enable the channel:
Copy
channels
zalouser
enabled
true
dmPolicy
&quot;pairing&quot;
Restart the Gateway (or finish onboarding).
DM access defaults to pairing; approve the pairing code on first contact.
What it is
Uses
zca listen
to receive inbound messages.
Uses
zca msg ...
to send replies (text/media/link).
Designed for “personal account” use cases where Zalo Bot API is not available.
Naming
Channel id is
zalouser
to make it explicit this automates a
personal Zalo user account
(unofficial). We keep
zalo
reserved for a potential future official Zalo API integration.
Finding IDs (directory)
Use the directory CLI to discover peers/groups and their IDs:
Copy
openclaw
directory
self
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
groups
list
--channel
zalouser
--query
&quot;work&quot;
Limits
Outbound text is chunked to ~2000 characters (Zalo client limits).
Streaming is blocked by default.
Access control (DMs)
channels.zalouser.dmPolicy
supports:
pairing | allowlist | open | disabled
(default:
pairing
channels.zalouser.allowFrom
accepts user IDs or names. The wizard resolves names to IDs via
zca friend find
when available.
Approve via:
openclaw pairing list zalouser
openclaw pairing approve zalouser &lt;code&gt;
Group access (optional)
Default:
channels.zalouser.groupPolicy = &quot;open&quot;
(groups allowed). Use
channels.defaults.groupPolicy
to override the default when unset.
Restrict to an allowlist with:
channels.zalouser.groupPolicy = &quot;allowlist&quot;
channels.zalouser.groups
(keys are group IDs or names)
Block all groups:
channels.zalouser.groupPolicy = &quot;disabled&quot;
The configure wizard can prompt for group allowlists.
On startup, OpenClaw resolves group/user names in allowlists to IDs and logs the mapping; unresolved entries are kept as typed.
Example:
Copy
channels
zalouser
groupPolicy
&quot;allowlist&quot;
groups
&quot;123456789&quot;
allow
true
&quot;Work Chat&quot;
allow
true
Multi-account
Accounts map to zca profiles. Example:
Copy
channels
zalouser
enabled
true
defaultAccount
&quot;default&quot;
accounts
work
enabled
true
profile
&quot;work&quot;
Troubleshooting
zca
not found:
Install zca-cli and ensure it’s on
PATH
for the Gateway process.
Login doesn’t stick:
openclaw channels status --probe
Re-login:
openclaw channels logout --channel zalouser &amp;&amp; openclaw channels login --channel zalouser
Zalo
Pairing