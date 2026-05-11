# Live Deployment

Top Comment Studio needs a server-backed host for the live judging URL. GitHub Pages can publish a static site, but it cannot run the FastAPI app or keep the Runway API secret private.

## Recommended Shape

Use three pieces:

1. Public GitHub repository for the open-source code.
2. Server-backed web host for the FastAPI app.
3. Techman Studios subdomain pointed at that host, such as `top-comment.techmanstudios.com`.

The live URL should point to the server-backed app, not to GitHub Pages.

## Fastest Hosting Path: Render

This repo includes a root [Render Blueprint](../render.yaml). After it is pushed to GitHub, create the Render service from:

```text
https://render.com/deploy?repo=https://github.com/TechmanStudios/top-comment-studio
```

During setup, Render will prompt for `RUNWAYML_HACKATHON_API_SECRET` because the Blueprint marks it with `sync: false`. Paste the real secret there, not into the repository.

The Blueprint creates:

- One Docker web service named `top-comment-studio`.
- A `/health` health check.
- A small persistent disk mounted at `/data` for local JSON episode records.
- Production env defaults for the v66 workflow ID and node map.

Use the generated `*.onrender.com` URL for the first smoke test. After that works, add the Techman Studios subdomain in Render and DreamHost DNS.

## Other Hosting Paths

Use a managed host that supports Python web services or Docker, such as Render, Railway, Fly.io, DigitalOcean App Platform, or a DreamHost VPS.

Recommended start command for non-Docker Python hosts:

```bash
uv run uvicorn top_comment_studio.app:app --host 0.0.0.0 --port $PORT
```

Recommended container command is already in the root `Dockerfile`.

Health check path:

```text
/health
```

## Required Environment Variables

Set these in the host dashboard. Do not commit real values.

```bash
APP_ENV=production
LOG_LEVEL=info
APP_NAME=Top Comment Studio
RUNWAYML_HACKATHON_API_SECRET=<real secret stored only on the host>
RUNWAYML_API_BASE_URL=https://api.dev.runwayml.com
RUNWAYML_API_VERSION=2024-11-06
RUNWAY_WORKFLOW_ID=c1b49d17-c80f-4705-b0e6-86c89a070464
RUNWAY_WORKFLOW_NAME=TCS Gen/Veo Director v2
RUNWAY_WORKFLOW_NODE_MAP_JSON=<copy the full JSON from .env.example>
TOP_COMMENT_STUDIO_DATA_DIR=/data/local
```

The existing v66 workflow duration and aspect ratio are locked in code, so judges cannot break those values from the UI.

## Storage

The app stores local episode records as JSON files. For a short judging demo, ephemeral storage can work as long as the instance does not restart during a render. For a more reliable live link, attach a small persistent disk or volume and mount it at `/data`.

## Techman Studios Domain

After the server host gives you its public URL:

1. Add a custom domain in the host dashboard, for example `top-comment.techmanstudios.com`.
2. In DreamHost DNS for `techmanstudios.com`, add the DNS record requested by the host.
3. Most managed hosts ask for a `CNAME` to their generated domain. VPS deployments usually use an `A` record to the server IP.
4. Wait for DNS and HTTPS provisioning.
5. Submit the final HTTPS URL as the live project link.

## DreamHost Notes

DreamHost shared hosting is usually best for static sites or traditional WSGI-style apps. This project is a FastAPI ASGI app that needs a long-running Python process and server-side environment secrets, so the safer DreamHost option is a VPS or DreamCompute instance.

On a DreamHost VPS, run the app behind Apache or Nginx as a reverse proxy:

```bash
git clone https://github.com/TechmanStudios/top-comment-studio.git
cd top-comment-studio
uv sync --frozen --no-dev
uv run uvicorn top_comment_studio.app:app --host 127.0.0.1 --port 8000
```

Then proxy `https://top-comment.techmanstudios.com` to `http://127.0.0.1:8000` and store the environment variables in the service manager, not in the public repo.

## Lightweight Privacy

For the hackathon, the simplest judge-friendly setup is an unlisted subdomain and removing or disabling it after judging. If you want a light gate, prefer host-level Basic Auth or an access-control product so the app code and Runway integration stay simple.

Do not put the Runway secret in browser JavaScript, GitHub Pages, screenshots, or repository files.
