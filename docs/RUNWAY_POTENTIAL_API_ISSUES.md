# Potential Runway Workflow / Developer API Issues

This note summarizes possible Runway backend or Workflow API issues observed during the Top Comment Studio hackathon buildout. Some of these may be expected behavior or undocumented constraints, but they caused enough integration friction that they are worth sharing with the Runway team.

## Context

Top Comment Studio turns an approved audience comment into a creator-reviewed YouTube Shorts production package, then submits a published Runway Workflow through the Developer API.

Integration surfaces used:

- Runway app Workflow canvas / internal dynamic workflow surface.
- Published Workflow Developer API endpoints on `api.dev.runwayml.com`.
- Direct Developer API model tasks for comparison.

No secrets, bearer tokens, cookies, or signed asset URLs are included in this report.

## High-Level Pattern

The most confusing failure mode was:

1. A graph validated or published successfully.
2. A paid invocation completed with `SUCCEEDED`.
3. The invocation returned an empty or missing final output.
4. The response had no clear failure state or no actionable node-level error.

This made it hard to know whether a Workflow graph was actually valid until after spending runtime credits.

## Potential Issues Observed

### 1. Published Workflow invocations can report `SUCCEEDED` with empty output

Several Workflow invocations completed with `SUCCEEDED` but returned no usable exposed output, no clear failure, and sometimes no useful node-error metadata.

Observed examples:

- Endpoint `8ab20d96-444e-4751-aa91-9c0b44c5036c`
  - Nine generated image outputs routed into Seedance `referenceImages`.
  - Invocation completed `SUCCEEDED`.
  - Output was empty.
  - No clear failure or useful node errors were returned.
- Endpoint `7ab7c6c7-6f54-4d40-a838-63fa72b1fe33`
  - One generated Gemini image routed into Seedance `referenceImages[0]`.
  - Invocation completed `SUCCEEDED`.
  - Output was empty.
- Endpoint `6ce25c70-8c4e-454b-9816-3c5569aff0f3`
  - Static Runway image asset routed into Seedance `referenceImages[0]`.
  - Raw curl invocation completed `SUCCEEDED`.
  - Output was empty, with no clear failure metadata.

Expected behavior:

- If a terminal video node cannot produce an output, the invocation should fail or include actionable node-level error metadata.

Workaround used:

- Avoid Seedance references inside published Workflows.
- Move reference-image usage to direct API lanes where possible.

### 2. Direct Seedance references worked, but Workflow Seedance references did not

A direct Seedance API call with image references succeeded and returned video output, while similar reference-image routing inside published Workflows repeatedly returned empty successful outputs.

Observed direct success:

- Direct Seedance text-to-video task with nine image references.
- Task `5bf9b443-cdf0-443c-b752-9e292592e69b`.
- Completed `SUCCEEDED`.
- Returned one MP4.

Expected behavior:

- If Seedance supports references directly, equivalent Workflow graph routing should either work or fail with a clear unsupported-routing error.

Actual behavior:

- Direct API worked.
- Workflow path silently produced empty successful invocations.

### 3. Disconnected Workflow nodes appeared to still schedule or execute

Disconnected or abandoned nodes in a published graph appeared to still run and fail, even when they were not part of the intended final output path.

Observed example:

- Endpoint `45745fae-baed-498c-b84e-84c9ff5549bb`.
- Invocation `4290417d-7633-457f-8651-6de272fc3a69`.
- A disconnected Claude node still executed and failed because its prompt was undefined.

Expected behavior:

- Disconnected nodes should not execute, or publish/validation should warn that disconnected runnable model nodes may still execute.

Workaround used:

- Delete disconnected model nodes before publishing.

### 4. Workflow validation accepted graphs that failed at runtime

Some graphs passed static validation or published successfully, but failed later during paid runtime due to runtime-only issues.

Observed examples:

- Veo Workflow node using indexed `promptImage[0]`
  - Endpoint `1766f759-d1ec-4cce-9a82-7386e8a72983`.
  - Invocation `b994efd0-6c3a-427d-a539-7ffe87c384d3`.
  - Runtime error: `Invalid task options: startFrame: Invalid input: expected object, received undefined`.
  - Workaround: use scalar `startFrame` / `endFrame` fields.
- Gemini API node published with `appNodeType: gemini-api`
  - Passed static checks.
  - Failed paid runtime.
  - Workaround: use `appNodeType: gemini`.

Expected behavior:

- Validation or publish should catch invalid model handoff fields and unsupported runtime app node types before paid execution.

### 5. Published endpoint metadata differed from saved canvas metadata

A saved canvas version looked correct, but the published Developer API endpoint lost important metadata.

Observed example:

- Endpoint `c5882933-e837-432d-b59e-d255be020d29`, version 65.
- Saved canvas had the intended 1080p graph.
- Published endpoint dropped TCS input labels and exposed final output metadata.
- Version 66 republishing fixed the issue.

Expected behavior:

- The published Developer API graph should preserve exposed inputs and outputs from the saved canvas version, or publish should fail if metadata cannot be preserved.

### 6. Combine Text wide fan-in caused scheduler errors

A wide parallel Combine Text fan-in produced runtime scheduler errors.

Observed example:

- Endpoint `ff2496e8-f10b-4b2a-a98a-fa474bc0b599`.
- Invocation returned `SUCCEEDED` with empty output.
- Combine node errors included: `Node is already running in this execution`.

Expected behavior:

- Wide fan-in should either be supported or validation should reject the graph shape.

Workaround used:

- Change to a serial Combine Text chain.

### 7. Some model node types could publish but had no runtime mapping

Published GPT Image Workflow nodes resolving to `appNodeType: gpt-tidepool-alpha` failed at runtime.

Observed error:

```text
No model variant mapping for app node type: gpt-tidepool-alpha
```

Expected behavior:

- Publish or validation should reject unsupported app node types before runtime.

Workaround used:

- Avoid those nodes in published demo workflows.

### 8. Veo Workflow duration seemed stricter than documented public API duration

The public API docs indicated vertical video duration could be 2-10 seconds, but a Workflow Veo 3.1 node rejected `seconds=10`.

Observed example:

- Endpoint `fb490b2c-aa0e-4e31-95eb-12b88c7bc6fc`.
- Error: `Invalid task options: seconds: Invalid input`.

Expected behavior:

- Workflow node constraints should match public API docs, or Workflow-specific limits should be documented clearly.

Workaround used:

- Use `seconds=4` for Workflow Veo nodes.

### 9. Canvas workflow IDs and published endpoint IDs are easy to confuse

This may not be a backend bug, but it caused confusing 404s.

Observed distinction:

- Canvas workflow ID: `ba325b07-a845-4fe6-901e-9242666ef8c7`.
- Published Developer API endpoint ID: `c1b49d17-c80f-4705-b0e6-86c89a070464`.

Using the canvas workflow ID with the Developer API route returns 404.

Request:

- Clearer docs or error messaging would help, for example: "This looks like a canvas workflow ID, not a published endpoint ID."

## Request To Runway

The biggest improvements for Workflow API developers would be:

- Treat terminal-node empty output as a failure, or expose a clear warning state.
- Include actionable node-level errors whenever a model handoff fails.
- Make publish/validation catch unsupported runtime `appNodeType` values.
- Validate Workflow-specific model option constraints before paid runtime.
- Document differences between direct model APIs and Workflow node routing.
- Improve error messaging for canvas IDs used where published endpoint IDs are expected.

Thanks for taking a look. Happy to provide more endpoint IDs, invocation IDs, or graph details if useful.
