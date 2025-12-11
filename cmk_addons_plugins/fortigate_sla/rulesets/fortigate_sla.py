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

from cmk.rulesets.v1 import (
    Title,
)

from cmk.rulesets.v1.form_specs import (
    Dictionary,
    DictElement,
    SimpleLevels,
    migrate_to_float_simple_levels,
    LevelDirection,
    InputHint,
    Float,
)

from cmk.rulesets.v1.rule_specs import (
    CheckParameters,
    HostAndItemCondition,
    Topic,
)


def migrate_to_ruleset_v1(params):
    if "warning_latency" in params and "critical_latency" in params:
        params["latency"] = (
            params.pop("warning_latency"),
            params.pop("critical_latency"),
        )
    if "warning_loss" in params and "critical_loss" in params:
        params["packetloss"] = (params.pop("warning_loss"), params.pop("critical_loss"))
    if "warning_jitter" in params and "critical_jitter" in params:
        params["jitter"] = (params.pop("warning_jitter"), params.pop("critical_jitter"))
    return params


def _parameter_valuespec_sla():
    return Dictionary(
        migrate=migrate_to_ruleset_v1,
        elements={
            "latency": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Threshold -> if latency over (>=) (ms):"),
                    form_spec_template=Float(),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=InputHint(value=(100, 200)),
                    migrate=migrate_to_float_simple_levels,
                ),
                required=True,
            ),
            "packetloss": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Threshold loss percentage (>=) [0-100]%:"),
                    form_spec_template=Float(),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=InputHint(value=(5, 20)),
                    migrate=migrate_to_float_simple_levels,
                ),
                required=True,
            ),
            "jitter": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Threshold jitter (>=) (ms):"),
                    form_spec_template=Float(),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=InputHint(value=(20, 30)),
                    migrate=migrate_to_float_simple_levels,
                ),
                required=True,
            ),
        },
    )


rule_spec_fortigate_sla = CheckParameters(
    name="fortigate_sla",
    topic=Topic.OPERATING_SYSTEM,
    condition=HostAndItemCondition(
        item_title=Title("Fortigate Latency, PacketLoss, Jitter")
    ),
    parameter_form=_parameter_valuespec_sla,
    title=Title("Fortigate Latency, PacketLoss, Jitter"),
)
