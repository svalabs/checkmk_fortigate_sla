#!/usr/bin/env python3

# +------------------------------------------------------------+
# |                                                            |
# |             | |             | |            | |             |
# |          ___| |__   ___  ___| | ___ __ ___ | | __          |
# |         / __| '_ \ / _ \/ __| |/ / '_ ` _ \| |/ /          |
# |        | (__| | | |  __/ (__|   <| | | | | |   <           |
# |         \___|_| |_|\___|\___|_|\_\_| |_| |_|_|\_\          |
# |                                   custom code by SVA       |
# |                                                            |
# |                                                            |
# +------------------------------------------------------------+
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   Copyright (C) 2025  SVA System Vertrieb Alexander GmbH
#                       by sebastian.haeger@sva.de
#
#   Last modified: 05.12.2025

# Authors: Edificom SA <dev-auto@edificom.ch>; martinmartossimon@gmail.com

import datetime
from dataclasses import dataclass
from typing import List

from cmk.agent_based.v2 import (
    CheckPlugin,
    Result,
    Service,
    State,
    check_levels,
    Metric,
    SimpleSNMPSection,
    SNMPTree,
    exists,
    all_of,
    startswith,
    StringTable,
    DiscoveryResult,
    CheckResult,
)


@dataclass
class sla_fortinet:
    LinkIfName: str
    LinkState: int
    LinkPacketLoss: float
    LinkLatency: float
    LinkJitter: float
    LinkName: str
    LinkVdom: str


def parse_sla(string_table: StringTable) -> List[sla_fortinet]:
    listLinkInfos = []
    for linkInfo in string_table:
        (
            LinkIfName,
            LinkState,
            LinkLatency,
            LinkPacketLoss,
            LinkJitter,
            LinkName,
            LinkVdom,
        ) = linkInfo
        listLinkInfos.append(
            sla_fortinet(
                LinkIfName=LinkIfName,
                LinkState=int(LinkState),
                LinkPacketLoss=float(LinkPacketLoss),
                LinkLatency=float(LinkLatency),
                LinkJitter=float(LinkJitter),
                LinkName=str(LinkName),
                LinkVdom=str(LinkVdom),
            )
        )
    return listLinkInfos


def discovery_sla_fortinet(section) -> DiscoveryResult:
    for service in section:
        yield Service(
            item=service.LinkIfName + " " + service.LinkName,
            parameters={
                "latency": ("fixed", (100, 200)),
                "packetloss": ("fixed", (5.0, 20.0)),
                "jitter": ("fixed", (20, 30)),
            },
        )


def check_sla_fortinet(item, params, section) -> CheckResult:
    now = datetime.datetime.now()
    if section:
        for item2 in section:
            if item == item2.LinkIfName + " " + item2.LinkName:
                if item2.LinkState == 0:
                    yield from check_levels(
                        int(item2.LinkState),
                        label="State: {}".format(
                            item2.LinkState,
                        ),
                        metric_name="fortigate_sla_state",
                        render_func=int,
                    )

                    yield from check_levels(
                        item2.LinkLatency,
                        levels_upper=params["latency"],
                        label="Latency: {}".format(
                            item2.LinkLatency,
                        ),
                        metric_name="fortigate_sla_latency",
                    )

                    yield from check_levels(
                        item2.LinkPacketLoss,
                        levels_upper=params["packetloss"],
                        label="PacketLoss: {}".format(
                            item2.LinkPacketLoss,
                        ),
                        metric_name="fortigate_sla_packetLoss",
                    )

                    yield from check_levels(
                        item2.LinkJitter,
                        levels_upper=params["jitter"],
                        label="Jitter: {}".format(
                            item2.LinkJitter,
                        ),
                        metric_name="fortigate_sla_jitter",
                    )

    else:
        yield Result(
            state=State.UNKNOWN,
            summary=f"No metrics collected on last check: {now}",
        )


snmp_section_fortigate_sla = SimpleSNMPSection(
    name="fortigate_sla",
    parse_function=parse_sla,
    detect=all_of(
        startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.12356.*"),
        exists(".1.3.6.1.4.1.12356.101.4.9.2.1.*"),
    ),
    # detect = startswith(".1.3.6.1.2.1.47.1.1.1.1.2.1", "fortinet"),
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.12356.101.4.9.2.1",
        oids=[
            "14",  # LinkIfName
            "4",  # LinkState
            "5",  # LinkLatency
            "9",  # LinkPacketLoss
            "6",  # LinkJitter
            "2",  # LinkName
            "10",  # LinkVdom
            # "1",  # LinkID
            # "3",  # LinkSeq
            # "11",  # LinkBandwidthIn
            # "12",  # LinkBandwidthOut
            # "13",  # LinkBandwidthBi
        ],
    ),
)

check_plugin_fortigate_sla = CheckPlugin(
    name="fortigate_sla",
    service_name="SLA %s",
    discovery_function=discovery_sla_fortinet,
    check_function=check_sla_fortinet,
    check_ruleset_name="fortigate_sla",
    check_default_parameters={
        "latency": ("fixed", (100, 200)),
        "packetloss": ("fixed", (5, 20)),
        "jitter": ("fixed", (20, 30)),
    },
)
