import {build} from 'esbuild';
await build({entryPoints:['entry.tsx'],bundle:true,format:'iife',minify:true,define:{'process.env.NODE_ENV':'"production"'},outfile:'../assets/hero-remotion.js'});
