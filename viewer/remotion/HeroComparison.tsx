import React from 'react';
import {AbsoluteFill, Easing, interpolate, useCurrentFrame} from 'remotion';

export type HeroRow={name:string;logo:string;rate:number;color:string;detail:string};
export type HeroProps={rows:HeroRow[];max:number;height:number;title:string;reducedMotion:boolean;compact?:boolean};

export const progressAtFrame=(frame:number,row:number,reducedMotion=false)=>reducedMotion?1:interpolate(frame,[8+row*3,66+row*3],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp',easing:Easing.bezier(.16,1,.3,1)});

export const HeroComparison:React.FC<HeroProps>=({rows,max,height,title,reducedMotion,compact=false})=>{
 const frame=useCurrentFrame(), width=compact?360:680, x=(value:number)=>(compact?14:190)+value/max*(compact?280:395);
 const ticks=max===100?[0,25,50,75,100]:max===40?[0,10,20,30,40]:[0,10,20,30];
 return <AbsoluteFill style={{backgroundColor:'transparent',fontFamily:'Manrope, sans-serif'}}>
  <svg width={width} height={height} viewBox={'0 0 '+width+' '+height} role="img" aria-label={title+'. '+rows.map(r=>r.name+' '+r.rate.toFixed(2)+' tokens per second').join('; ')} data-remotion-frame={frame} data-remotion-hero="true" data-compact={compact}>
   {ticks.map(v=><g key={'tick-'+v}>{compact?rows.map((_,i)=><line key={i} x1={x(v)} x2={x(v)} y1={49+i*86} y2={73+i*86} stroke="#e6ebf2"/>):<line x1={x(v)} x2={x(v)} y1={10} y2={height-37} stroke="#e6ebf2"/>}<text x={x(v)} y={height-12} textAnchor="middle" fill="#8793a3" fontSize={11}>{v}</text></g>)}
   {rows.map((r,i)=>{const cy=compact?22+i*86:35+i*61,progress=progressAtFrame(frame,i,reducedMotion),rate=r.rate*progress;return <g key={r.name}>
    <image href={'/assets/logos/'+r.logo+'.svg'} x={compact?14:12} y={cy-18+(compact?0:5)} width={compact?24:28} height={compact?24:28}/>
    <text x={compact?46:52} y={cy-1} fill="#263448" fontSize={compact?15:16} fontWeight={700}>{r.name}</text>
    <text x={compact?46:52} y={cy+19} fill="#7d899b" fontSize={compact?10:9}>{r.detail}</text>
    <rect x={x(0)} y={cy+(compact?29:-13)} width={x(rate)-x(0)} height={22} rx={4} fill={r.color} data-hero-rate={r.rate} data-hero-progress={progress}>
     <title>{r.name+' · '+r.rate.toFixed(5)+' reported tok/s · '+r.detail}</title>
    </rect>
    <text x={x(rate)+9} y={cy+(compact?46:4)} fill="#294166" fontSize={compact?17:19} data-rate-label={r.name}>{rate.toFixed(2)}</text>
   </g>})}
   <text x={width-8} y={height-12} textAnchor="end" fill="#8793a3" fontSize={10}>tok/s</text>
  </svg>
 </AbsoluteFill>;
};
