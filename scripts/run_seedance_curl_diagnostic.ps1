param(
    [ValidateSet('direct', 'workflow', 'task-status', 'workflow-status')]
    [string]$Mode = 'direct',
    [string]$Id = '',
    [string]$WorkflowId = '7ab7c6c7-6f54-4d40-a838-63fa72b1fe33',
    [string]$Episode = 'episode_001',
    [int]$ReferenceCount = 1,
    [int]$Duration = 5
)

$ErrorActionPreference = 'Stop'

function Read-DotEnv {
    $values = @{}
    if (-not (Test-Path '.env')) {
        return $values
    }

    Get-Content '.env' | ForEach-Object {
        if ($_ -match '^\s*#' -or $_ -notmatch '^\s*([^=]+)=(.*)$') {
            return
        }
        $key = $matches[1].Trim()
        $value = $matches[2].Trim().Trim('"').Trim("'")
        $values[$key] = $value
    }
    return $values
}

function Get-RunwaySecret {
    param([hashtable]$EnvValues)

    if ($env:RUNWAYML_HACKATHON_API_SECRET) {
        return $env:RUNWAYML_HACKATHON_API_SECRET
    }
    if ($env:RUNWAYML_API_SECRET) {
        return $env:RUNWAYML_API_SECRET
    }
    if ($EnvValues['RUNWAYML_HACKATHON_API_SECRET']) {
        return $EnvValues['RUNWAYML_HACKATHON_API_SECRET']
    }
    if ($EnvValues['RUNWAYML_API_SECRET']) {
        return $EnvValues['RUNWAYML_API_SECRET']
    }
    throw 'Set RUNWAYML_HACKATHON_API_SECRET in the shell or local .env before calling Runway.'
}

function Get-BoardImageUrls {
    param([string]$EpisodeId)

    $recordPath = Join-Path 'data/local/chains/main' "$EpisodeId.json"
    if (-not (Test-Path $recordPath)) {
        throw "Episode record not found: $recordPath"
    }

    $record = Get-Content $recordPath -Raw | ConvertFrom-Json
    $imageUrls = @()
    foreach ($row in $record.runway_image_board.rows) {
        foreach ($url in $row.output_urls) {
            if ($url -match '\.(png|jpg|jpeg|webp)(\?|$)') {
                $imageUrls += $url
            }
        }
    }
    return $imageUrls
}

function Invoke-RunwayCurlJson {
    param(
        [string]$Method,
        [string]$Path,
        [string]$Secret,
        [string]$Body = ''
    )

    $url = "https://api.dev.runwayml.com$Path"
    if ($Body) {
        $responseText = $Body | curl.exe -sS -X $Method $url `
            -H "Authorization: Bearer $Secret" `
            -H 'X-Runway-Version: 2024-11-06' `
            -H 'Content-Type: application/json' `
            --data-binary '@-'
    }
    else {
        $responseText = curl.exe -sS -X $Method $url `
            -H "Authorization: Bearer $Secret" `
            -H 'X-Runway-Version: 2024-11-06'
    }

    return $responseText | ConvertFrom-Json
}

function Get-OutputCount {
    param($Output)

    if ($null -eq $Output) {
        return 0
    }
    if ($Output -is [array]) {
        return $Output.Count
    }
    if ($Output -is [pscustomobject]) {
        return @($Output.PSObject.Properties).Count
    }
    return 1
}

function Write-SanitizedTaskStatus {
    param($Response, [string]$Kind)

    [pscustomobject]@{
        kind         = $Kind
        id           = $Response.id
        status       = $Response.status
        progress     = $Response.progress
        output_count = Get-OutputCount $Response.output
        failure      = ($Response.failure ?? $Response.failureCode ?? '')
    } | ConvertTo-Json -Depth 4
}

$envValues = Read-DotEnv
$secret = Get-RunwaySecret $envValues

switch ($Mode) {
    'direct' {
        $imageUrls = Get-BoardImageUrls $Episode
        if ($imageUrls.Count -lt $ReferenceCount) {
            throw "Need $ReferenceCount image references, found $($imageUrls.Count)."
        }

        $references = @()
        foreach ($url in $imageUrls[0..($ReferenceCount - 1)]) {
            $references += @{ uri = $url }
        }

        $body = [ordered]@{
            model      = 'seedance2'
            promptText = 'Create a vertical cinematic shot of a storm-powered floating city. Use the supplied reference image or images for subject and style continuity. Slow push-in camera, readable silhouette, safe fictional scene, no text overlays, no logos.'
            references = $references
            ratio      = '720:1280'
            duration   = $Duration
        } | ConvertTo-Json -Depth 10 -Compress

        $response = Invoke-RunwayCurlJson 'POST' '/v1/text_to_video' $secret $body
        [pscustomobject]@{
            kind            = 'direct_seedance_curl_submit'
            task_id         = $response.id
            status          = $response.status
            reference_count = $ReferenceCount
            duration        = $Duration
        } | ConvertTo-Json -Depth 4
    }
    'workflow' {
        $payload = uv run python -c "import json; from top_comment_studio.settings import get_settings; from top_comment_studio.storage import ChainStore; from top_comment_studio.runway.workflows import build_logical_inputs, build_node_outputs, parse_node_map; settings=get_settings(); record=ChainStore(settings.data_dir).get('$Episode'); node_map, issues=parse_node_map(settings.runway_workflow_node_map_json); assert record is not None; assert not issues, issues; print(json.dumps({'nodeOutputs': build_node_outputs(build_logical_inputs(record), node_map)}, separators=(',', ':')))"
        $response = Invoke-RunwayCurlJson 'POST' "/v1/workflows/$WorkflowId" $secret $payload
        $invocationId = if ($response.id) { $response.id } else { $response.workflowInvocationId }
        [pscustomobject]@{
            kind          = 'workflow_curl_submit'
            workflow_id   = $WorkflowId
            invocation_id = $invocationId
            status        = $response.status
        } | ConvertTo-Json -Depth 4
    }
    'task-status' {
        if (-not $Id) { throw 'Pass -Id <task_id> for task-status.' }
        $response = Invoke-RunwayCurlJson 'GET' "/v1/tasks/$Id" $secret
        Write-SanitizedTaskStatus $response 'direct_seedance_curl_status'
    }
    'workflow-status' {
        if (-not $Id) { throw 'Pass -Id <workflow_invocation_id> for workflow-status.' }
        $response = Invoke-RunwayCurlJson 'GET' "/v1/workflow_invocations/$Id" $secret
        Write-SanitizedTaskStatus $response 'workflow_curl_status'
    }
}
