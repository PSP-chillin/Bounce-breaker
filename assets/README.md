# Bounce Breaker Assets

The catalog is procedural and data-driven, so the project does not need hundreds of binary image files.

- `BASKET_ASSETS`: 100 basket profiles with stable ids, styles, colors, dimensions, and movement speeds.
- `BALL_ASSETS`: 100 ball profiles with stable ids, colors, radii, speeds, gravity values, bounce multipliers, and break speeds.
- `BACKGROUND_ASSETS`: 20 named themes, including Black, Basketball Court, Neon Grid, Sunset, Ocean, Forest, and more.

`GameEngine(background_index=0)` selects a background catalog entry. The default remains the black theme. Ball profiles are selected when balls spawn, and the default basket profile is used by the current game.
