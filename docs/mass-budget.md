# Mass budget and thrust-to-weight

Line items: docs/mass-budget.csv. All masses are estimates until parts are weighed. Limit: 1,500 g. Motor figures need checking at thrustcurve.org (see decision 003).

| Vehicle | Roadmap mass | Bottom-up mass | With +10% growth | Margin to 1,500 g |
|---|---|---|---|---|
| S1 (74 mm printed, 1 x D12) | ~350 g | **376 g** | 413 g | ~1,090 g |
| S2 (74 mm printed, 2 x E12, 3 legs) | ~900 g | **659 g** | 725 g | ~775 g |
| S3, S4 | 1,200 / 1,400 g | not itemized | | roadmap values only |

S3 and S4 stay below the limit on paper, but 1,400 g leaves only 100 g of slack. Itemize them before committing.

## Thrust-to-weight (average thrust / weight)
| Case | Mass | T/W | Need |
|---|---|---|---|
| S1, D12 | 376 g | 2.85 | >1.3 |
| S1, C6 | 355 g | 1.44 | >1.3 |
| S2 liftoff, E12 | 659 g | 1.70 (1.55 at 725 g) | >1.3 |
| S2 landing burn, E12 | 631 g | 1.78 | >1 |
| S2 liftoff / landing, F15 landing motor | 698 / 670 g | 1.61 / 2.28 | >1.3 / >1 |
| S2 at roadmap 900 g, E12 liftoff | 900 g | **1.25 FAIL** | >1.3 |

## Flag: S2 at 900 g is too heavy for an E12
At 900 g the E12 gives 1.25, below the 1.3 rule. It needs **862 g or less**; for a safe 1.5 it needs **about 750 g or less**. Our itemized estimate is 659 g, so either the 900 g is old padding or items are missing (check the list). Do not add mass to "use up" the budget.

Biggest S2 items: body 160 g, motors 112 g, legs 75 g, nose 35 g, gimbal 35 g. Cheapest savings: 66 mm cardboard body (-90 g), fewer printed walls, Teensy instead of ESP32 (-4 g). Swapping to 20 kg servos adds 93 g.

Method note: average thrust ignores the early spike and the thrust drop off at the end, and the climb motor mass drops as it burns. Real flights should be simulated (OpenRocket for ascent).
