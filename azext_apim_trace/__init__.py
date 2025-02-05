from .trace import get_trace_token, call_with_trace, get_trace
import importlib

from azure.cli.core import AzCommandsLoader
from azure.cli.core.commands.parameters import get_enum_type
from azure.cli.command_modules.apim._client_factory import cf_apim

# Imported modules must implement load_command_table and load_arguments
module_names = ['trace']

modules = list(map(importlib.import_module, map(
    lambda m: '{}.{}'.format('azext_apim_trace', m), module_names)))


__all__ = ['get_trace_token', 'call_with_trace', 'get_trace']


class ApimExportCommandsLoader(AzCommandsLoader):

    def __init__(self, cli_ctx=None):
        from azure.cli.core.commands import CliCommandType
        custom_type = CliCommandType(
            operations_tmpl='azext_apim_trace#{}', client_factory=cf_apim)
        super(ApimExportCommandsLoader, self).__init__(cli_ctx=cli_ctx,
                                                       custom_command_type=custom_type)

    def load_command_table(self, args):
        with self.command_group('apim api trace') as g:
            g.custom_command('get-token', 'get_trace_token')
            g.custom_command('invoke', 'call_with_trace')
            g.custom_command('show', 'get_trace')

        return self.command_table

    def load_arguments(self, command):
        with self.argument_context('apim api trace get-token') as c:
            c.argument('service_name',
                       options_list=['--service-name'],
                       help='Name of the API Management service'
                       )
            c.argument(
                'api_id',
                options_list=['--api-id'],
                help='API identifier. Must be unique in the current API Management service instance. Non-current revision has ;rev=n as a suffix where n is the revision number.'
            )

        with self.argument_context('apim api trace invoke') as c:
            c.argument('service_name',
                       options_list=['--service-name'],
                       help='Name of the API Management service'
                       )
            c.argument(
                'api_id',
                options_list=['--api-id'],
                help='API identifier. Must be unique in the current API Management service instance. Non-current revision has ;rev=n as a suffix where n is the revision number.'
            )

            c.argument('method', options_list=['--method', '-m'],
                    arg_type=get_enum_type(['head', 'get', 'put', 'post', 'delete', 'options', 'patch'], default='get'),
                    help='HTTP request method')
            c.argument('url', options_list=['--url', '--uri', '-u'],
                    help='Request URL')
            c.argument('headers', nargs='+',
                        help="Space-separated headers in KEY=VALUE format or JSON string. Use @{file} to load from a file")
            c.argument('body', options_list=['--body', '-b'],
                    help='Request body. Use @{file} to load from a file. For quoting issues in different terminals, '
                            'see https://github.com/Azure/azure-cli/blob/dev/doc/use_cli_effectively.md#quoting-issues')

            c.argument('trace_output_file', help='File to save trace output to')
            c.argument('output_file', help='save response payload to a file')
            c.argument('allow_insecure_ssl', options_list=['--insecure'], help='Allow insecure server connections when calling API endpoint',)

        with self.argument_context('apim api trace show') as c:
            c.argument('service_name',
                       options_list=['--service-name'],
                       help='Name of the API Management service'
                       )
            c.argument("trace_id", options_list=['--trace-id'], help="ID of trace to display")

COMMAND_LOADER_CLS = ApimExportCommandsLoader

