# Benchmark hero graph

A Remotion browser Player renders the landing page hero from frozen showcase data passed by viewer/app.js. The three views cover published Mac comparisons, differing market configurations and the five retained M5 measurements. Measurement generation and inference are outside this frontend.

```sh
npm ci --prefix viewer/remotion
npm run build --prefix viewer/remotion
npm test --prefix viewer/remotion
```

The build writes viewer/assets/hero-remotion.js. The checked-in bundle allows the Python read-only preview to serve the page directly. There is no offline render command. The Player holds its final frame, supports replay, adapts to a compact composition, and respects reduced-motion preference. Exact rates appear in the SVG accessible label even during the animation.

Pinned dependencies and their licenses are recorded by package-lock.json and the installed packages; Remotion use is subject to its [license](https://www.remotion.dev/license).
