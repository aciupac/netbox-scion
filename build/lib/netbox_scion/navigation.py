from netbox.plugins import PluginMenuButton, PluginMenuItem
from netbox.choices import ButtonColorChoices

menu_items = (
    PluginMenuItem(
        link='plugins:netbox_scion:organization_list',
        link_text='Organizations',
        buttons=(
            PluginMenuButton(
                link='plugins:netbox_scion:organization_add',
                title='Add',
                icon_class='mdi mdi-plus-thick',
                color=ButtonColorChoices.GREEN
            ),
        )
    ),
    PluginMenuItem(
        link='plugins:netbox_scion:isdas_list',
        link_text='ISD-ASes',
        buttons=(
            PluginMenuButton(
                link='plugins:netbox_scion:isdas_add',
                title='Add',
                icon_class='mdi mdi-plus-thick',
                color=ButtonColorChoices.GREEN
            ),
        )
    ),
    PluginMenuItem(
        link='plugins:netbox_scion:scionlinkassignment_list',
        link_text='SCION Link Assignments',
        buttons=(
            PluginMenuButton(
                link='plugins:netbox_scion:scionlinkassignment_add',
                title='Add',
                icon_class='mdi mdi-plus-thick',
                color=ButtonColorChoices.GREEN
            ),
        )
    ),
)
