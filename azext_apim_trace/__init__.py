from .trace import get_trace_token, call_with_trace
import importlib

from azure.cli.core import AzCommandsLoader
from azure.cli.command_modules.apim._client_factory import cf_apim

# Imported modules must implement load_command_table and load_arguments
module_names = ['trace']

modules = list(map(importlib.import_module, map(
    lambda m: '{}.{}'.format('azext_apim_trace', m), module_names)))


__all__ = ['get_trace_token', 'call_with_trace']


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

        for m in modules:
            if hasattr(m, 'load_command_table'):
                m.load_command_table(self, args)

        return self.command_table

    def load_arguments(self, command):
        with self.argument_context('apim api trace get-token') as c:
            c.argument('service_name',
                       options_list=['--service-name'],
                       help='Name of the API Management service'
                       )
            c.argument(
                'api-id',
                options_list=['--api-id'],
                help='API identifier. Must be unique in the current API Management service instance. Non-current revision has ;rev=n as a suffix where n is the revision number.'
            )

        for m in modules:
            if hasattr(m, 'load_arguments'):
                m.load_arguments(self, command)


COMMAND_LOADER_CLS = ApimExportCommandsLoader

