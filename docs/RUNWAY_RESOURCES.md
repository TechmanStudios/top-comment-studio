# Runway Resources Inventory

This document keeps the Runway API and GitHub resources close at hand for Top Comment Studio. Do not store secrets here. The local Runway key belongs in `.env` as `RUNWAYML_API_SECRET`.

## Hackathon

- API Hackathon: https://runwayml.com/api-hackathon
- Terms: https://runwayml.com/api-hackathon-terms
- Submission deadline from the hackathon page: Monday, May 11, 2026 at 9am ET.
- Submission expects a short project description and demo video.
- Judging criteria: creativity, technical depth, impact, polish.

## API Basics

- Developer docs: https://docs.dev.runwayml.com/
- Developer portal: https://dev.runwayml.com/
- API reference: https://docs.dev.runwayml.com/api
- Base URL: `https://api.dev.runwayml.com`
- Auth header: `Authorization: Bearer <RUNWAYML_API_SECRET>`
- Version header: `X-Runway-Version: 2024-11-06`

## Runway Account Surfaces

The project has access to two signed-in Runway surfaces during local development:

- Runway app workflows: https://app.runwayml.com/video-tools/teams/techmandesign/ai-tools/workflows
- Runway Developer Portal: https://dev.runwayml.com/
- Custom workflow API endpoints: https://dev.runwayml.com/organization/8f8366b8-b7b6-4f9c-baae-f72c16c9f79f/workflows

Do not commit browser cookies, storage state, login exports, or session files. Local cookie/session exports are intentionally ignored by `.gitignore`.

## Developer Portal Model Catalog

The Developer Portal currently exposes these model/feature shortcuts for Top Comment Studio planning:

- `runway/gwm-avatars` - real-time interactive avatars powered by GWM-1.
- `runway/Gen-4.5` - text-to-video and image-to-video.
- `runway/Gen-4 Turbo` - fast image-to-video.
- `runway/Gen-4 Aleph` - video-to-video editing, transformation, and generation.
- `runway/Gen-4 Image` - text/image-to-image generation.
- `runway/Gen-4 Image Turbo` - faster, more cost-efficient text/image-to-image generation.
- `runway/Gen-3 Turbo` - legacy image-to-video.
- `runway/Act Two` - motion capture, image/video-to-video.
- `google/Gemini 3 Pro` - image generation with 4K support.
- `google/Gemini 2.5 Flash` - image generation and editing.
- `openai/GPT Image 2` - image generation up to 4K.
- `google/Veo 3` and `google/Veo 3.1` - text/image-to-video with sound.
- `elevenlabs/Text to Speech` - speech generation.
- `elevenlabs/Voice Isolation` - background noise removal.
- `elevenlabs/Sound Effect` - text-to-audio effects.
- `elevenlabs/Voice Dubbing` - audio translation/dubbing.
- `elevenlabs/Speech to Speech` - voice conversion while preserving tone.

## Runway App Workflows

The Runway app has a node-based Workflows area for chaining models and intermediate steps. Useful featured templates to inspect or clone for the Top Comment Studio pipeline include:

- Story Panels
- B Roll Generator
- Seamless Transitions
- New Angles
- Storyboard to Film
- Video to Video - Scene Edit
- Video to Video - Style Transfer
- Fabric, Color, Texture Swap

Initial workflow direction: create a custom workflow that takes a reviewed top-comment creative seed, generates storyboard panels or reference images, produces a vertical video draft, and optionally adds voiceover/sound effects after creator approval.

When a custom workflow is created in the Runway app, its API endpoint should appear in the Developer Portal workflow endpoint list for the Techman Studios organization:

- https://dev.runwayml.com/organization/8f8366b8-b7b6-4f9c-baae-f72c16c9f79f/workflows

## High-Value Docs Pages

- Create account / setup: https://docs.dev.runwayml.com/guides/setup/
- Using the API: https://docs.dev.runwayml.com/guides/using-the-api/
- Models: https://docs.dev.runwayml.com/guides/models/
- Pricing: https://docs.dev.runwayml.com/guides/pricing/
- Go-live checklist: https://docs.dev.runwayml.com/guides/go-live/
- API changelog: https://docs.dev.runwayml.com/api-details/api_changelog/
- API versioning overview: https://docs.dev.runwayml.com/api-details/versioning/
- Version 2024-11-06: https://docs.dev.runwayml.com/api-details/versions/2024-11-06/
- Uploading assets: https://docs.dev.runwayml.com/assets/inputs#uploading-assets
- Troubleshooting: https://docs.dev.runwayml.com/errors/troubleshooting/
- Playground: https://dev.runwayml.com/models

## Seedance 2

- Guide: https://docs.dev.runwayml.com/guides/seedance/
- Supports text-to-video, image-to-video, and video-to-video.
- Supports optional image, video, and audio references depending on mode.
- Duration: 5 to 15 seconds.
- Useful vertical ratios include `720:1280`, `834:1112`, `496:864`, and `560:752`.
- Audio references require a prompt; text-to-video audio references also need at least one image or video reference.
- The docs note that curl may be the most reliable test path until SDK types catch up for newer Seedance-specific fields.

## Current API Changelog Notes

- `gemini_image3_pro` / Nano Banana Pro image generation is available.
- `gpt_image_2` is available via text-to-image.
- `gen4.5` is available for high-quality text-to-video and image-to-video.
- ElevenLabs text-to-speech, sound effects, voice isolation, dubbing, and speech-to-speech are available through the API.
- Google Veo 3.1 is available.
- Third-party models include Veo3 and Gemini image models.
- Runway API MCP server is available at https://github.com/runwayml/runway-api-mcp-server.

## Characters / Avatar Docs

- Characters overview: https://docs.dev.runwayml.com/characters/
- Quickstart: https://docs.dev.runwayml.com/characters/quickstart/
- Custom avatars: https://docs.dev.runwayml.com/characters/create-your-own/
- Core concepts: https://docs.dev.runwayml.com/characters/concepts/
- Building integration: https://docs.dev.runwayml.com/characters/integration/
- Embedded widget: https://docs.dev.runwayml.com/characters/widget/
- Knowledge base: https://docs.dev.runwayml.com/characters/documents/
- Custom voices: https://docs.dev.runwayml.com/characters/custom-voice/
- Client tools: https://docs.dev.runwayml.com/characters/tools/client-tools/
- Server tools: https://docs.dev.runwayml.com/characters/tools/server-tools/
- Tools best practices: https://docs.dev.runwayml.com/characters/tools/best-practices/
- Tools reference: https://docs.dev.runwayml.com/characters/tools/reference/
- Video meeting: https://docs.dev.runwayml.com/characters/video-meeting/
- Camera and screen sharing: https://docs.dev.runwayml.com/characters/screens/
- LiveKit Agents: https://docs.dev.runwayml.com/characters/livekit/
- Troubleshooting: https://docs.dev.runwayml.com/characters/troubleshooting/

## Runway GitHub Organization

Organization: https://github.com/runwayml

The org page reported 61 public repositories. The most relevant for this project are:

- https://github.com/runwayml/sdk-python - Python SDK.
- https://github.com/runwayml/sdk-node - Node/TypeScript SDK.
- https://github.com/runwayml/openapi - Runway API OpenAPI spec.
- https://github.com/runwayml/skills - agent skills for generation and integration.
- https://github.com/runwayml/runway-api-mcp-server - MCP server for Runway generation workflows.
- https://github.com/runwayml/avatars-sdk-react - React SDK for real-time AI avatar interactions.
- https://github.com/runwayml/avatars-node-rpc - Node backend RPC tools for avatar sessions.
- https://github.com/runwayml/runway-studio-skills - Runway Studio agent skills.
- https://github.com/runwayml/runway-characters-meet - example characters meeting app.
- https://github.com/runwayml/live-avatar.github.io - live avatar API docs.

## Full Public Repo Inventory

| Repo | Language | Archived | Notes |
|---|---:|---:|---|
| [livekit-agents](https://github.com/runwayml/livekit-agents) | Python | no | Realtime voice AI agents fork. |
| [runway-pipecat](https://github.com/runwayml/runway-pipecat) | Python | no | Voice and multimodal conversational AI fork. |
| [avatars-sdk-react](https://github.com/runwayml/avatars-sdk-react) | TypeScript | no | React SDK for GWM-1 avatars. |
| [sdk-python](https://github.com/runwayml/sdk-python) | Python | no | Runway Python SDK. |
| [sdk-node](https://github.com/runwayml/sdk-node) | TypeScript | no | Runway Node SDK. |
| [openapi](https://github.com/runwayml/openapi) | Shell | no | Runway API OpenAPI spec. |
| [confingy](https://github.com/runwayml/confingy) | Python | no | Configuration helper. |
| [runway-agents-js](https://github.com/runwayml/runway-agents-js) | TypeScript | no | Realtime multimodal AI agents with Node.js. |
| [runway-characters-meet](https://github.com/runwayml/runway-characters-meet) | HTML | no | Characters meeting example. |
| [runway-api-mcp-server](https://github.com/runwayml/runway-api-mcp-server) | TypeScript | no | Runway MCP server. |
| [skills](https://github.com/runwayml/skills) | Python | no | Runway coding agent skills. |
| [runway-studio-skills](https://github.com/runwayml/runway-studio-skills) | Python | no | Runway Studio skills. |
| [avatars-node-rpc](https://github.com/runwayml/avatars-node-rpc) | TypeScript | no | Backend RPC handler for avatar sessions. |
| [openclaw-skills](https://github.com/runwayml/openclaw-skills) | TypeScript | no | Openclaw skills. |
| [runway-characters-meeting-skill](https://github.com/runwayml/runway-characters-meeting-skill) | Python | no | Characters meeting skill. |
| [openclaw-skill-send-video-message](https://github.com/runwayml/openclaw-skill-send-video-message) | Python | no | Send-video-message Openclaw skill. |
| [live-avatar.github.io](https://github.com/runwayml/live-avatar.github.io) | HTML | no | Live avatar API documentation. |
| [hair-makeover-api-demo](https://github.com/runwayml/hair-makeover-api-demo) | TypeScript | no | API demo. |
| [figma-plugin](https://github.com/runwayml/figma-plugin) | HTML | no | Figma plugin. |
| [terraform-retool-modules](https://github.com/runwayml/terraform-retool-modules) | HCL | no | Terraform modules. |
| [try-on-chrome-extension](https://github.com/runwayml/try-on-chrome-extension) | JavaScript | no | Chrome extension. |
| [chrome-extension-tutorial](https://github.com/runwayml/chrome-extension-tutorial) | JavaScript | no | Chrome extension tutorial. |
| [terraform-aws-wandb](https://github.com/runwayml/terraform-aws-wandb) | HCL | no | Terraform module for Weights & Biases. |
| [fuse-device-plugin](https://github.com/runwayml/fuse-device-plugin) | Go | no | Kubernetes FUSE device plugin. |
| [RunwayML-for-Photoshop](https://github.com/runwayml/RunwayML-for-Photoshop) | TypeScript | yes | Photoshop integration. |
| [learn](https://github.com/runwayml/learn) | unknown | yes | Legacy tutorials and examples. |
| [maxmsp](https://github.com/runwayml/maxmsp) | Max | yes | Max/MSP integration. |
| [k8s-cloudwatch-adapter](https://github.com/runwayml/k8s-cloudwatch-adapter) | Go | no | Kubernetes CloudWatch adapter. |
| [awssecret2env](https://github.com/runwayml/awssecret2env) | Go | no | AWS Secrets Manager to env utility. |
| [circleci-gcp-oidc-terraform](https://github.com/runwayml/circleci-gcp-oidc-terraform) | HCL | no | CircleCI OIDC Terraform. |
| [react-hls](https://github.com/runwayml/react-hls) | TypeScript | no | HLS/RTMP React component. |
| [guided-inpainting](https://github.com/runwayml/guided-inpainting) | Python | no | Keyframe propagation models. |
| [amazon-guardduty-to-slack](https://github.com/runwayml/amazon-guardduty-to-slack) | unknown | no | GuardDuty Slack integration. |
| [hosted-models](https://github.com/runwayml/hosted-models) | TypeScript | yes | Legacy hosted model examples. |
| [model-template](https://github.com/runwayml/model-template) | Python | yes | Legacy model template. |
| [model-sdk](https://github.com/runwayml/model-sdk) | Python | yes | Legacy model SDK. |
| [CHANGELOG](https://github.com/runwayml/CHANGELOG) | unknown | no | Runway app changelog. |
| [ofxRunway](https://github.com/runwayml/ofxRunway) | Makefile | yes | openFrameworks integration. |
| [openh264](https://github.com/runwayml/openh264) | C++ | no | OpenH264 codec. |
| [taxjar-node](https://github.com/runwayml/taxjar-node) | JavaScript | yes | Sales tax API client. |
| [terraform-aws-wireguard](https://github.com/runwayml/terraform-aws-wireguard) | HCL | no | AWS WireGuard Terraform module. |
| [terraform-aws-eks](https://github.com/runwayml/terraform-aws-eks) | HCL | no | AWS EKS Terraform module. |
| [RunwayML-for-Grasshopper](https://github.com/runwayml/RunwayML-for-Grasshopper) | C# | yes | Grasshopper integration. |
| [processing-library](https://github.com/runwayml/processing-library) | Java | yes | Processing library. |
| [touchDesigner](https://github.com/runwayml/touchDesigner) | unknown | yes | TouchDesigner integration. |
| [p5js](https://github.com/runwayml/p5js) | JavaScript | yes | p5.js integration. |
| [Intro-Synthetic-Media](https://github.com/runwayml/Intro-Synthetic-Media) | JavaScript | no | Synthetic media class materials. |
| [model-face-recognition](https://github.com/runwayml/model-face-recognition) | Python | yes | Legacy face recognition model. |
| [design](https://github.com/runwayml/design) | unknown | no | Design resources. |
| [puredata](https://github.com/runwayml/puredata) | unknown | yes | Pure Data integration. |
| [OpenRNDR](https://github.com/runwayml/OpenRNDR) | Kotlin | yes | OpenRNDR integration. |
| [javascript](https://github.com/runwayml/javascript) | JavaScript | yes | Legacy JavaScript integration. |
| [arduino](https://github.com/runwayml/arduino) | C++ | yes | Arduino integration. |
| [processing](https://github.com/runwayml/processing) | Processing | yes | Archived Processing integration. |
| [RunwayML-for-Unity](https://github.com/runwayml/RunwayML-for-Unity) | C# | yes | Unity integration. |
| [unity](https://github.com/runwayml/unity) | C# | yes | Archived Unity integration. |
| [Arbitrary-Image-Stylization](https://github.com/runwayml/Arbitrary-Image-Stylization) | Python | yes | Legacy model. |
| [model-squeezenet](https://github.com/runwayml/model-squeezenet) | Python | yes | Legacy SqueezeNet model. |
| [alpha_models](https://github.com/runwayml/alpha_models) | PureBasic | yes | Alpha models. |
| [runway](https://github.com/runwayml/runway) | unknown | yes | Deprecated alpha app. |
| [alpha_website](https://github.com/runwayml/alpha_website) | JavaScript | yes | Alpha website. |

## Runway Skills Repo Notes

- Install skills for compatible agents with `npx skills add runwayml/skills`.
- Generation skills: `rw-generate-video`, `rw-generate-image`, `rw-generate-audio`.
- Integration skills: `rw-integrate-video`, `rw-integrate-image`, `rw-integrate-audio`.
- Setup/reference skills: `rw-recipe-full-setup`, `rw-check-compatibility`, `rw-setup-api-key`, `rw-check-org-details`, `rw-api-reference`, `rw-fetch-api-reference`.
- Utilities: `use-runway-api`, `rw-integrate-uploads`.

## Recommendation For Top Comment Studio

Start with server-side Runway calls only. Keep `RUNWAYML_API_SECRET` off the client, generate vertical Shorts prompts by default, and use manual approval before spending credits on video generation.
