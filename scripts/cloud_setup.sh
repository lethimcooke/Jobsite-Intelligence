#!/usr/bin/env bash
# Cloud environment setup for Jobsite Intelligence (copied from Austin-Signage scripts/cloud_setup.sh).
# Paste this whole file into the environment's "Setup script" field.
# It is self-contained: it does not read anything from the repo checkout.
#
# Installs the CLI dependencies used by the repo-scoped skills in .claude/skills/:
#   - agent-reach (CLI + doctor) and its bundled yt-dlp / feedparser
#   - mcporter (MCP client used for Exa web search) + the Exa remote MCP entry
# The claude-automation-recommender skill needs no CLI dependencies.
#
# It does NOT install login-backed channels (Twitter, Reddit, XiaoHongShu,
# Facebook, Instagram, LinkedIn, Boss): they need personal cookies/browser
# sessions and are out of scope for this project.
#
# Safe to re-run. Every step logs; a failing optional step does not abort.

set -u
log() { printf '[cloud_setup] %s\n' "$*"; }

# Pinned upstream revision of Panniantong/Agent-Reach (v1.5.0, 2026-09-16).
AGENT_REACH_REF="${AGENT_REACH_REF:-a19a171fa980a0785849596492e0af4db800c82f}"
# git+https, not the /archive/ zip: the cloud proxy returns 403 for archive downloads.
AGENT_REACH_URL="git+https://github.com/Panniantong/Agent-Reach@${AGENT_REACH_REF}"
# 0.14.2 declares node>=24 but was tested working on this image's Node 22 (2026-10-07).
MCPORTER_VERSION="${MCPORTER_VERSION:-0.14.2}"

export PATH="$HOME/.local/bin:$PATH"

# 1. agent-reach CLI, isolated from system Python.
if command -v uv >/dev/null 2>&1; then
  log "installing agent-reach via uv tool ($AGENT_REACH_REF)"
  uv tool install --force --with-executables-from yt-dlp "$AGENT_REACH_URL" \
    || log "WARN: uv tool install failed"
fi
if ! command -v agent-reach >/dev/null 2>&1; then
  log "falling back to a venv at ~/.agent-reach-venv"
  python3 -m venv "$HOME/.agent-reach-venv" \
    && "$HOME/.agent-reach-venv/bin/pip" install --quiet "$AGENT_REACH_URL" \
    && mkdir -p "$HOME/.local/bin" \
    && ln -sf "$HOME/.agent-reach-venv/bin/agent-reach" "$HOME/.local/bin/agent-reach" \
    && ln -sf "$HOME/.agent-reach-venv/bin/yt-dlp" "$HOME/.local/bin/yt-dlp" \
    || log "WARN: venv install of agent-reach failed"
fi

# 2. mcporter (Node) for Exa search.
if command -v npm >/dev/null 2>&1; then
  if ! command -v mcporter >/dev/null 2>&1; then
    log "installing mcporter@${MCPORTER_VERSION}"
    npm install -g --no-fund --no-audit "mcporter@${MCPORTER_VERSION}" || log "WARN: mcporter install failed"
  fi
else
  log "WARN: npm not found; Exa search will be unavailable"
fi

# 3. Register the Exa remote MCP endpoint in mcporter's home config (~/.mcporter, not the repo).
#    Keyless works but hits Exa's free rate limit quickly from shared cloud IPs.
#    Optional: set EXA_API_KEY as an environment variable in the cloud environment settings.
if command -v mcporter >/dev/null 2>&1; then
  EXA_URL="https://mcp.exa.ai/mcp"
  [ -n "${EXA_API_KEY:-}" ] && EXA_URL="https://mcp.exa.ai/mcp?exaApiKey=${EXA_API_KEY}"
  mcporter config remove exa --scope home >/dev/null 2>&1 || true
  mcporter config add exa "$EXA_URL" --scope home >/dev/null 2>&1 \
    && log "mcporter: exa configured ($([ -n "${EXA_API_KEY:-}" ] && echo 'with API key' || echo 'keyless'))" \
    || log "WARN: could not add exa to mcporter"
fi

# 3b. yt-dlp needs a JS runtime for YouTube (doctor's own recommended fix; Node is on the image).
mkdir -p "$HOME/.config/yt-dlp"
grep -qxF -- '--js-runtimes node' "$HOME/.config/yt-dlp/config" 2>/dev/null \
  || printf '%s\n' '--js-runtimes node' >> "$HOME/.config/yt-dlp/config"

# 3c. Contact-form browser (scripts/fill_form.cjs): Chromium reads the NSS store, which starts empty,
#     so it rejects the session's agent-proxy CA. Add that CA (trust it, don't skip verification).
PROXY_CA="/root/.ccr/agent-proxy-ca.crt"
if [ -f "$PROXY_CA" ]; then
  command -v certutil >/dev/null 2>&1 || { apt-get install -y -q libnss3-tools >/dev/null 2>&1 \
    || { apt-get update -q >/dev/null 2>&1 && apt-get install -y -q libnss3-tools >/dev/null 2>&1; }; }
  if command -v certutil >/dev/null 2>&1; then
    mkdir -p "$HOME/.pki/nssdb"
    [ -f "$HOME/.pki/nssdb/cert9.db" ] || certutil -N -d "sql:$HOME/.pki/nssdb" --empty-password
    certutil -D -d "sql:$HOME/.pki/nssdb" -n "CCR agent-proxy CA" >/dev/null 2>&1 || true
    certutil -A -d "sql:$HOME/.pki/nssdb" -t "C,," -n "CCR agent-proxy CA" -i "$PROXY_CA" \
      && log "browser: agent-proxy CA added to NSS store" || log "WARN: could not add proxy CA to NSS"
  else
    log "WARN: certutil unavailable; scripts/fill_form.cjs will fail TLS"
  fi
fi

# 4. Report. Doctor is read-only by default; it never installs or writes cookies.
log "versions:"
command -v agent-reach >/dev/null 2>&1 && agent-reach --version 2>&1 | head -1
command -v yt-dlp      >/dev/null 2>&1 && printf 'yt-dlp %s\n' "$(yt-dlp --version 2>&1 | head -1)"
command -v mcporter    >/dev/null 2>&1 && printf 'mcporter %s\n' "$(mcporter --version 2>&1 | head -1)"
command -v agent-reach >/dev/null 2>&1 && agent-reach doctor 2>&1 | tail -n 40

log "done"
exit 0
