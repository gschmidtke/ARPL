# ARPL-CON-0001: Power connector without load parameters

| | |
|---|---|
| Level | 3 |
| Work class | W1 |
| Workflows | connectors-systems, family-authoring, parameters-data |
| Disciplines | electrical, food-service, mechanical, audio-av |
| Project types | generic |
| Revit tested | 2024 |
| Status | candidate |

**Intent:** Give the LOD 350 brewer a 120 V power connector with apparent load

## Learning curve

| Version | Instruction | Result | Problem |
|---|---|---|---|
| v01 | ConnectorElement.CreateElectricalConnector(doc, ElectricalSystemType.PowerCircuit, ref) | Connector created | No Voltage, Apparent Load, Poles or Power Factor parameters on the connector |
| v02 | ElectricalSystemType.PowerBalanced; associate after CanElementParameterBeAssociated | Connector 120 V / 1668 VA / 1 pole, associated to family parameters |  |

## Lesson
The PowerCircuit connector type carries no load data.

## Rule
Use PowerBalanced for equipment power connectors and probe associability before associating.

## Validation
- Connector parameters read back
- Flex test of the associated parameters
