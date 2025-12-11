# Fortigate SLA
Fortinet Fortigate SLAs Parameters: LinkName, LinkState, LinkPacketLoss, LinkLatency and LinkJitter

Based on https://exchange.checkmk.com/p/fortigate-sla

## Requirements
- CMK 2.1, 2.2 and 2.3 needs https://exchange.checkmk.com/p/fortigate-sla
- CMK 2.3 and 2.4+ needs v2.2.x

## Checks
The following checks are included:  
| Check | Service Name |
| --- | --- |
| fortigate_sla | SLA %s |


## Compatibility
The plugin is tested with the following major versions:
* 2.3.0 -> v2.1.1 - v2.2.2
* 2.4.0 -> v2.2.2

### Releases

See exchange.checkmk.com

### Changes

- 2.2.2:
 - Ported for CMK 2.4

### Docs

GPL-Licensed

