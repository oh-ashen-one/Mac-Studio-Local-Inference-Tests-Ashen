import React from 'react';
import {createRoot,Root} from 'react-dom/client';
import {Player} from '@remotion/player';
import {HeroComparison,HeroProps} from './HeroComparison';
let root:Root|undefined,latest:HeroProps|undefined,replay=0,compact=false;
const paint=()=>{
 if(!latest)return;
 const mount=document.getElementById('hero-graph')!;
 if(!root){root=createRoot(mount);new ResizeObserver(()=>{const next=mount.clientWidth<480;if(next!==compact){compact=next;paint();}}).observe(mount);}
 compact=mount.clientWidth<480;
 const props={...latest,compact,height:compact?latest.rows.length*86+25:latest.height},width=compact?360:680,signature=props.title+'-'+props.rows.map(r=>r.rate).join('-')+'-'+width+'-'+replay;
 root.render(<Player key={signature} component={HeroComparison} inputProps={props} durationInFrames={120} fps={30} compositionWidth={width} compositionHeight={props.height} controls={false} initiallyMuted={true} autoPlay={!props.reducedMotion} initialFrame={props.reducedMotion?119:0} loop={false} moveToBeginningWhenEnded={false} clickToPlay={false} doubleClickToFullscreen={false} numberOfSharedAudioTags={0} style={{width:'100%',aspectRatio:width+' / '+props.height}}/>);
};
(window as any).renderRemotionHero=(props:HeroProps)=>{latest=props;paint();};
(window as any).replayHeroAnimation=()=>{replay++;paint();};
