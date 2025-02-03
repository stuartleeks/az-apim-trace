# az-apim-trace

**NOTE: This extension is experimental and not supported**

This repository contains an extension for the Azure CLI (`az`) for working with API tracing in Azure API Management (APIM).

- [az-apim-trace](#az-apim-trace)
	- [Installation](#installation)
	- [Usage](#usage)
		- [`az apim api trace get-token`](#az-apim-api-trace-get-token)
		- [`az apim api trace invoke`](#az-apim-api-trace-invoke)
			- [--headers](#--headers)
	- [CHANGELOG](#changelog)
		- [0.0.3 - 2025-02-03](#003---2025-02-03)
		- [0.0.2 - 2025-02-03](#002---2025-02-03)
		- [0.0.1 - 2025-01-31](#001---2025-01-31)


## Installation

The repository has a GitHub release that contains a wheel file for the extension.
To install directly from GitHub, run the following command:

```bash
# Download and install from the GitHub release
az extension add --source https://github.com/stuartleeks/az-apim-trace/releases/download/v0.0.3/apim_trace-0.0.3-py2.py3-none-any.whl --upgrade
```

If you prefer to build the extension yourself, run `make build-wheel` from the root of the project repo.
The repo contains a VS Code dev container that has all the required dependencies installed.

After building the extension, you can install it using `make add-extension`.
If you want to install the extension in a different environment after building then run `az extension add --source <path to wheel file>`.

## Usage

The extension provides the following commands:

| Command                       | Description                                                     |
| ----------------------------- | --------------------------------------------------------------- |
| `az apim api trace get-token` | Get a token for tracing for an API                              |
| `az apim api trace invoke`    | Call an API with a trace token and download the resulting trace |

### `az apim api trace get-token`

This command retrieves a token that can be used to trace calls to an API in APIM.
The command has the following parameters:

| Name                    | Description                                                               |
| ----------------------- | ------------------------------------------------------------------------- |
| `--resource-group`/`-g` | [Required] The name of the resource group that contains the APIM service. |
| `--service-name`        | [Required] The name of the APIM service.                                  |
| `--api-id`              | [Required] The ID of the API to trace.                                    |

The command returns a JSON object with a `token` property that contains the trace token.

### `az apim api trace invoke`

This command calls an API in APIM with a trace token and downloads the resulting trace.

The command has the following parameters:

| Name                    | Description                                                               |
| ----------------------- | ------------------------------------------------------------------------- |
| `--resource-group`/`-g` | [Required] The name of the resource group that contains the APIM service. |
| `--service-name`        | [Required] The name of the APIM service.                                  |
| `--api-id`              | [Required] The ID of the API to trace.                                    |
| `--method`              | [Required] The HTTP method to use when calling the API.                   |
| `--url`                 | [Required] The URL to call.                                               |
| `--trace-output`        | [Required] The file to write the trace output to.                         |
| `--headers`             | [Optional] Headers to include in the request (see below).                 |

The command will get a trace token for the specified API, call the API specified by `--url` and `--method` attaching the trace token as a header, and write the resulting trace to the file specified by `--trace-output`.

#### --headers

The `--headers` parameter can be used to specify headers to include in the request.
The syntax is similar to the `az rest` command.

For example, to include a `Content-Type` header you can use the `key=value` form:

```bash
az apim api trace ... --headers "Content-Type=application/json"
```

To include multiple headers, separate them with spaces:

```bash
az apim api trace ... --headers "Content-Type=application/json" "Accept=application/json"
```

You can also specify headers as a JSON object:

```bash
az apim api trace ... --headers '{"Content-Type": "application/json", "Accept": "application/json"}'
```

## CHANGELOG

### 0.0.3 - 2025-02-03

- Update `invoke` command to use `requests` package directly for the API call as this avoids issues with unexpected headers being added to the request.

### 0.0.2 - 2025-02-03

- Add support for specifying headers in the `az apim api trace invoke` command

### 0.0.1 - 2025-01-31

- Initial release


