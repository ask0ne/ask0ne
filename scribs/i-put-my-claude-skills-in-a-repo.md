---
title: "i put my claude skills in a repo"
date: 2026-11-01T12:00:00
tags: ["claude", "tools"]
---

i have been using [orca](https://www.onorca.dev) for the past few months...and am not surprised that my [last post](/thoughts/microdecisions-and-llms) aged like milk (the ape is fine, thanks for asking)

since then i have multiple claude code sessions open all day (worktrees ftw!), and i haven't opened vscode for anything except updating env variables.

on this journey i think people underestimate how hard agents are to master. they're easy to learn and difficult to master, a bit like driving. the gap between an average driver and a professional racer is skill, and sometimes the vehicle. for example when [linus torvalds used an llm and clocked a 23x jump](https://www.tomshardware.com/software/linux/linus-torvalds-posts-his-first-llm-assisted-patch-to-the-linux-kernel-after-issuing-clear-pro-ai-directives-the-bossman-makes-use-of-ai-tooling-himself). but for npcs like us it's not that bad and in the end it's just a tool, and how you wield it matters.

so, here's my stash (sort of)

**1. statusline**

model, branch, cost, context used and burn rate in one line. it changes colour when the context gets scary.

```prompt
install this claude code status line (needs jq): save https://raw.githubusercontent.com/ask0ne/skills/main/statusline/statusline.sh to ~/.claude/statusline.sh and chmod +x it. then set "statusLine" in ~/.claude/settings.json to the json at https://raw.githubusercontent.com/ask0ne/skills/main/statusline/statusline.json, keeping every other key. tell me what each part of the line shows.
```

**2. edit-lint (hook)**

blocks long comment blocks, 62 times in six weeks. the why goes in the commit message, not above a three line function.

```prompt
install the claude code hook "edit-lint" (needs jq): save https://raw.githubusercontent.com/ask0ne/skills/main/hooks/edit-lint.sh to ~/.claude/hooks/edit-lint.sh and chmod +x it. then merge a settings.json entry for it under hooks.PostToolUse, using the event, matcher and timeout in https://raw.githubusercontent.com/ask0ne/skills/main/hooks/edit-lint.json; the command is: bash "$HOME/.claude/hooks/edit-lint.sh". keep every existing hook, no duplicates. tell me what it does and how to test it.
```

**3. /ui-design**

no ui code until i've picked an ascii mockup. twenty seconds there beats an hour in the running app.

```prompt
install the claude code skill "ui-design": fetch https://raw.githubusercontent.com/ask0ne/skills/main/skills/engineering/ui-design/SKILL.md and save it, unchanged, to ~/.claude/skills/ui-design/SKILL.md. then tell me how to trigger it.
```

**4. /boost**

checks whether slow work can actually be split before spawning agents. its best answer is "it can't".

```prompt
install the claude code skill "boost": fetch https://raw.githubusercontent.com/ask0ne/skills/main/skills/productivity/boost/SKILL.md and save it, unchanged, to ~/.claude/skills/boost/SKILL.md. then tell me how to trigger it.
```

**5. /wip**

a read-only checklist of what's really done, with the proof re-checked. useful when a session has gone long or you just spaced out after a heavy lunch.

```prompt
install the claude code skill "wip": fetch https://raw.githubusercontent.com/ask0ne/skills/main/skills/productivity/wip/SKILL.md and save it, unchanged, to ~/.claude/skills/wip/SKILL.md. then tell me how to trigger it.
```

**6. parity-auditor (subagent)**

after a rewrite, lists everything the old version could do and checks each one still works. also good for those messy git merges.

```prompt
install the claude code subagent "parity-auditor": fetch https://raw.githubusercontent.com/ask0ne/skills/main/agents/parity-auditor.md and save it, unchanged, to ~/.claude/agents/parity-auditor.md. then tell me how to use it.
```

these and more are at [ask0ne/skills](https://github.com/ask0ne/skills), including nox and gm: one saves where i stopped for the day, the other picks it up next morning in the same worktree. a lot of the repo is hooks, because most of my rules turned out to be "stop doing that".

the secret sauce is i try to deep dive every few weeks into my older prompt history and figure out things that could take me out of the loop and give me more time to play videogames or sip coffees. the goal for me has not been to increase efficiency but to enable my laziness (probably).

p.s: skills i use a lot but didn't write, so they're not in the repo: [mattpocock's skills](https://github.com/mattpocock/skills), [google's elephant-goldfish-model](https://github.com/google/elephant-goldfish-model) (egm, which i only picked up on oct 29), and [musings](https://musings-blog-66c2.web.app/posts/arise-skills-registry/) (my tech-design skill started there).
