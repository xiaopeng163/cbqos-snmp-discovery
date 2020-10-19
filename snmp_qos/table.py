from rich.console import Console
from rich.table import Table


def print_table(service_policy_obj_list):
    # cbQosCMPrePolicyByte64  1.3.6.1.4.1.9.9.166.1.15.1.1.6
    # cbQosCMPostPolicyByte64  1.3.6.1.4.1.9.9.166.1.15.1.1.10
    # cbQosCMDropByte64 1.3.6.1.4.1.9.9.166.1.15.1.1.17
    console = Console()
    for sp_obj in service_policy_obj_list:
        result = sp_obj.class_map_dict()
        interface = result['interface']['name']
        direction = result['direction']
        policy_name = result['policy_name']
        policy_index = result['policy_index']
        console.print(
            f"interface=[bold red]{interface}[/bold red] direction=[bold red]{direction}[/bold red] policy_name=[bold red]{policy_name}[/bold red]")
        table = Table(show_header=True)
        table.add_column("classmap", justify="right")
        table.add_column("policy_index", justify="right")
        table.add_column("object_index", justify="right")
        table.add_column("cbQosCMPrePolicyByte64", justify="right")
        table.add_column("cbQosCMPostPolicyByte64", justify="right")
        table.add_column("cbQosCMDropByte64", justify="right")
        for class_map in result['classmap']:
            rows = [
                class_map['cfg_name'],
                policy_index,
                class_map['object_index'],
                f"1.3.6.1.4.1.9.9.166.1.15.1.1.6.[bold red]{policy_index}[/bold red].[bold green]{class_map['object_index']}[/bold green]",
                f"1.3.6.1.4.1.9.9.166.1.15.1.1.10.[bold red]{policy_index}[/bold red].[bold green]{class_map['object_index']}[/bold green]",
                f"1.3.6.1.4.1.9.9.166.1.15.1.1.17.[bold red]{policy_index}[/bold red].[bold green]{class_map['object_index']}[/bold green]"
            ]
            table.add_row(*rows)
    # table.add_row(
    #     "Dev 20, 2019", "Star Wars: The Rise of Skywalker", "$275,000,000", "$375,126,118"
    # )
    # table.add_row(
    #     "May 25, 2018",
    #     "[red]Solo[/red]: A Star Wars Story",
    #     "$275,000,000",
    #     "$393,151,347",
    # )
    # table.add_row(
    #     "Dec 15, 2017",
    #     "Star Wars Ep. VIII: The Last Jedi",
    #     "$262,000,000",
    #     "[bold]$1,332,539,889[/bold]",
    # )

        console.print(table)
