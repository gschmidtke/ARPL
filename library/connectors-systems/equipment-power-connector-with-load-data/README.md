# ARPL-CON-0001 rev 1: Power connector without load parameters

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 3 |
| Work class | W1 |
| Status | candidate |
| Use when | adding electrical power connectors to equipment families; connecting a family to an electrical circuit |
| Not for | piping or duct connectors |
| Workflows | connectors-systems, family-authoring, parameters-data |
| Disciplines | electrical, food-service, mechanical, audio-av |
| Project types | generic |
| Revit tested | 2024 |
| API | ConnectorElement.CreateElectricalConnector, ElectricalSystemType.PowerBalanced, FamilyManager.AssociateElementParameterToFamilyParameter |
| Failure patterns | FP05 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** Give the LOD 350 brewer a 120 V power connector with apparent load

**LOD:** LOD 350

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | ConnectorElement.CreateElectricalConnector(doc, ElectricalSystemType.PowerCircuit, ref) | Connector created | No Voltage, Apparent Load, Poles or Power Factor parameters on the connector | parameter probe |
| v02 | ElectricalSystemType.PowerBalanced; associate after CanElementParameterBeAssociated | Connector 120 V / 1668 VA / 1 pole, associated to family parameters |  |  |

## Lesson
The PowerCircuit connector type carries no load data.

## Rule
Use PowerBalanced for equipment power connectors and probe associability before associating.

## Validation
- Connector parameters read back
- Flex test of the associated parameters
