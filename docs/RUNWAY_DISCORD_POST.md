# Discord Post: Runway Potential API Issues

Hey Runway team — during the Top Comment Studio hackathon buildout, we ran into a few Workflow / Developer API behaviors that may be bugs, undocumented constraints, or backend edge cases.

The biggest pattern: some published Workflow invocations validated/published correctly and later returned `SUCCEEDED`, but with empty or missing final output and little/no actionable node-error metadata. This happened most often around Seedance references inside Workflows. Direct Seedance reference calls worked, but similar reference routing inside published Workflows repeatedly produced empty successful invocations.

Other things we worked around:

- Disconnected Workflow nodes appeared to still schedule/execute.
- Some graphs passed validation but failed only at paid runtime.
- A saved canvas version and the published Developer API endpoint sometimes differed in exposed input/output metadata.
- Wide Combine Text fan-in caused scheduler errors like `Node is already running in this execution`.
- Some published model nodes had app node types that failed runtime mapping.
- Workflow Veo duration constraints seemed stricter than the public direct API docs.
- Canvas workflow IDs vs published endpoint IDs caused confusing 404s.

I wrote up a shareable report with endpoint/invocation breadcrumbs and the workarounds we used:

`docs/RUNWAY_POTENTIAL_API_ISSUES.md`

None of this includes secrets/tokens/cookies — just IDs and behavior notes. Happy to provide more detail if helpful.
