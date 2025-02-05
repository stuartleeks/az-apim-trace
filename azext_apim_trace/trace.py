import json
import sys
import requests
from knack.help_files import helps
from knack.log import get_logger
from knack.util import CLIError
from requests.structures import CaseInsensitiveDict

from azure.cli.core._profile import Profile
from azure.cli.core.commands.transform import unregister_global_transforms
from azure.cli.core.util import send_raw_request, shell_safe_json_parse
import webbrowser
import re

logger = get_logger(__name__)

helps['apim api trace get-token'] = """
    type: command
    short-summary: Retrieves a trace token for calling an API in an API Management service and getting a trace of the call.
"""

helps['apim api trace invoke'] = """
    type: command
    short-summary: Invokes an API in an API Management service with a trace header and captures the trace result.
"""

helps['apim api trace show'] = """
    type: command
    short-summary: Display a trace from an API Management service API call.
"""

# https://github.com/Azure/azure-cli/blob/main/doc/authoring_command_modules/authoring_commands.md#write-the-command-loader


def get_trace_token(
        cmd,
        resource_group_name: str,
        service_name: str,
        api_id: str,
):
    print(
        '** NOTE: this extension is experimental, not supported, and may not work as expected! **', file=sys.stderr)

    # Couldn't find an SDK method to get the trace token, so using raw request
    # Want POST https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ApiManagement/service/{serviceName}/gateways/managed/listDebugCredentials?api-version=2023-05-01-preview
    # as per https://learn.microsoft.com/en-us/azure/api-management/api-management-howto-api-inspector#enable-tracing-for-an-api

    subscription_id = _get_subscription_id(cmd)

    url = f"/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.ApiManagement/service/{service_name}/gateways/managed/listDebugCredentials?api-version=2023-05-01-preview"
    api_full_id = f"/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.ApiManagement/service/{service_name}/apis/{api_id}"
    body = json.dumps({
        "credentialsExpireAfter": "PT1H",
        "apiId": api_full_id,
        "purposes": ["tracing"]
    })

    response: requests.Response = send_raw_request(
        cmd.cli_ctx,
        "POST",
        url,
        headers=["Content-Type=application/json"],
        body=body
    )
    result = response.json()
    token = result["token"]
    return {"token": token}


def call_with_trace(cmd, url, resource_group_name: str,
                    service_name: str,
                    api_id: str,
                    trace_output_file: str,
                    method=None,
                    headers=None,
                    body=None,
                    output_file=None,
                    allow_insecure_ssl: bool = False):

    #
    # Get trace token
    #
    subscription_id = _get_subscription_id(cmd)
    token_result = get_trace_token(
        cmd, resource_group_name, service_name, api_id)
    token = token_result["token"]

    #
    # Make API request
    #
    headers = _normalize_headers(headers)
    headers["Apim-Debug-Authorization"] = token
    method = method or "GET"
    r = requests.request(method, url, headers=headers, data=body, verify=not allow_insecure_ssl)
    if output_file:
        with open(output_file, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)

    if not output_file and r.content:
        try:
            return r.json()
        except ValueError:
            logger.warning('Not a json response, outputting to stdout. For binary data '
                           'suggest use "--output-file" to write to a file')
            print(r.text)

    #
    # Get trace
    #
    trace_id = r.headers.get("Apim-Trace-Id")
    if trace_id:
        trace = _get_trace(cmd, subscription_id,
                           resource_group_name, service_name, trace_id)
        with open(trace_output_file, "w") as f:
            f.write(json.dumps(trace, indent=4))
        webbrowser.open(trace_output_file)

    return None


def get_trace(cmd, resource_group_name: str,
              service_name: str,
              trace_id: str):
    subscription_id = _get_subscription_id(cmd)
    trace = _get_trace(cmd, subscription_id,
                       resource_group_name, service_name, trace_id)
    return trace


def _normalize_headers(headers):
    # NOTE: headers has nargs set when the argument is registered which means it will be a list
    # `az rest` also allows a single item with a JSON-ish encoded object, so we'll do the same
    # We need to add the Apim-Debug-Authorization header with the token
    # so we need to do the same parsing that send_raw_request does to be able to add the header
    result = CaseInsensitiveDict()
    for s in headers or []:
        try:
            temp = shell_safe_json_parse(s)
            result.update(temp)
        except CLIError:
            # didn't parse as json, try splitting on first '=' or ':'
            # regex to split on first ':' or '='
            match = re.match(r'(.+?)[:=](.+)', s)
            if not match:
                raise ValueError("Header must contain either ':' or '='")
            # unpack the key/value pair
            key, value = match.groups()
            result[key] = value
    headers = result
    return headers

def _get_subscription_id(cmd):
    profile = Profile(cli_ctx=cmd.cli_ctx)
    subscription_id = cmd.cli_ctx.data['subscription_id'] or profile.get_subscription_id(
    )
    logger.debug(f"Using subscription {subscription_id}")
    return subscription_id


def _get_trace(cmd, subscription_id: str, resource_group_name: str, service_name: str, trace_id: str):
    # POST https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ApiManagement/service/{serviceName}/gateways/managed/listTrace?api-version=2023-05-01-preview
    url = f"/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.ApiManagement/service/{service_name}/gateways/managed/listTrace?api-version=2023-05-01-preview"
    body = json.dumps({
        "traceId": trace_id
    })
    response: requests.Response = send_raw_request(
        cmd.cli_ctx,
        "POST",
        url,
        headers=["Content-Type=application/json"],
        body=body
    )
    return response.json()
