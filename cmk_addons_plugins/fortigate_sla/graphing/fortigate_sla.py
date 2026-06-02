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
#   Copyright (C) 2026  SVA System Vertrieb Alexander GmbH
#                       by sebastian.haeger@sva.de
#
#   Last modified: 02.06.2026

from cmk.graphing.v1 import Title
from cmk.graphing.v1.graphs import Graph
from cmk.graphing.v1.metrics import (
    Color,
    DecimalNotation,
    Metric,
    StrictPrecision,
    Unit
)

metric_fortigate_sla_latency = Metric(
    name="fortigate_sla_latency",
    title=Title("Latency"),
    unit=Unit(DecimalNotation("ms"), StrictPrecision(2)),
    color=Color.BLUE,
)

metric_fortigate_sla_packetLoss = Metric(
    name="fortigate_sla_packetLoss",
    title=Title("PacketLoss"),
    unit=Unit(DecimalNotation("%"), StrictPrecision(2)),
    color=Color.DARK_BLUE,
)

metric_fortigate_sla_jitter = Metric(
    name="fortigate_sla_jitter",
    title=Title("Jitter"),
    unit=Unit(DecimalNotation("ms"), StrictPrecision(2)),
    color=Color.LIGHT_BLUE,
)

graph_fortigate_sla = Graph(
    name="fortigate_sla",
    title=Title("Fortigate SLA"),
    compound_lines=[
        "fortigate_sla_latency",
        "fortigate_sla_jitter"
    ]
)
