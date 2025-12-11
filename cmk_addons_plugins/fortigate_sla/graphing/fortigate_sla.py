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
#   Last modified: 20.11.2025

# Authors: Edificom SA <dev-auto@edificom.ch>; martinmartossimon@gmail.com
from cmk.gui.i18n import _
from cmk.gui.plugins.metrics import metric_info, perfometer_info
from cmk.gui.plugins.metrics.utils import check_metrics, m

metric_info["fortigate_sla_latency"] = {
    "title": _("Latency"),
    "unit": "s",
    "color": "26/a",
}

metric_info["fortigate_sla_packetLoss"] = {
    "title": _("PacketLoss"),
    "unit": "%",
    "color": "12/a",
}

metric_info["fortigate_sla_jitter"] = {
    "title": _("Jitter"),
    "unit": "s",
    "color": "13/a",
}

check_metrics["check_mk-fortigate_sla"] = {
    "Latency": {"scale": m},
    "Jitter": {"scale": m},
}

perfometer_info.append(
    (
        "dual",
        [
            {
                "type": "linear",
                "segments": [
                    "fortigate_sla_latency",
                    "fortigate_sla_jitter",
                ],
                "total": 0.2,
            },
            {
                "type": "linear",
                "segments": [
                    "fortigate_sla_packetLoss",
                ],
                "total": 100,
            },
        ],
    )
)
