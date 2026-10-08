# Bounce Breaker Assets

The catalog is procedural and data-driven, so the project does not need hundreds of binary image files.

- `BASKET_ASSETS`: 100 basket profiles with stable ids, styles, colors, dimensions, and movement speeds.
- `BALL_ASSETS`: 100 ball profiles with stable ids, colors, radii, speeds, gravity values, bounce multipliers, and break speeds.
- `BACKGROUND_ASSETS`: 20 named themes, including Black, Basketball Court, Neon Grid, Sunset, Ocean, Forest, and more.

`GameEngine(background_index=0, basket_index=0)` selects exact catalog entries. When no indices are provided, a basket and background are selected for each new game. Ball profiles are selected when balls spawn.
