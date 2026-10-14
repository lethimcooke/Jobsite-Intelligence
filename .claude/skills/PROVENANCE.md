# Repo-scoped skills: where they come from

These skills live in the repo so every cloud session loads them from
`.claude/skills/` at checkout. Nothing here depends on user-scope plugins,
`enabledPlugins`, or `~/.claude/skills`, which do not survive a fresh cloud
container.

| Skill | Upstream | Pinned revision | License | Local changes |
|---|---|---|---|---|
| `agent-reach/` | github.com/Panniantong/Agent-Reach, `agent_reach/skill/` | `a19a171fa980a0785849596492e0af4db800c82f` (v1.5.0, 2026-09-16) | MIT (`agent-reach/LICENSE`) | `SKILL.md` = upstream `SKILL_en.md` body unchanged, with a project frontmatter `description` (scoped to this project) and a "Project overlay" section added above it. `references/` copied unchanged (Chinese prose, commands are universal). |
| `claude-automation-recommender/` | github.com/anthropics/claude-plugins-official, `plugins/claude-code-setup/skills/claude-automation-recommender/` | `6eb6a30bf024b182d418d3bbd11f156e360365af` (plugin v1.0.0, fetched 2026-10-07) | Apache-2.0 (`claude-automation-recommender/LICENSE`) | None. Copied verbatim. Read-only skill; no CLI dependencies. |

**Updating:** re-copy from upstream at a new revision, re-apply the agent-reach
overlay, bump the revision here and `AGENT_REACH_REF` in `scripts/cloud_setup.sh`
together, then re-run the tests listed in `CLAUDE.md`.
