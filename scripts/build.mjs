import {mkdir,readFile,writeFile,cp,rm,readdir,stat} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
const root=fileURLToPath(new URL('../',import.meta.url)),dist=path.join(root,'dist');
const lessons=JSON.parse(await readFile(path.join(root,'data/lessons.json')));
const terms=JSON.parse(await readFile(path.join(root,'data/glossary.json')));
const sources=JSON.parse(await readFile(path.join(root,'data/sources.json')));
const unique=(items,label)=>{if(new Set(items.map(i=>i.id)).size!==items.length)throw new Error(`Duplicate ${label} IDs`);};
unique(lessons,'lesson');unique(terms,'term');unique(sources,'source');
const sourceIds=new Set(sources.map(s=>s.id)),termIds=new Set(terms.map(t=>t.id)),lessonIds=new Set(lessons.map(l=>l.id));
for(const l of lessons){
  for(const r of l.sourceRefs)if(!sourceIds.has(r.source))throw new Error(`Unknown source ${r.source} in ${l.id}`);
  for(const id of l.terms)if(!termIds.has(id))throw new Error(`Undefined term ${id} in ${l.id}`);
  for(const id of l.related)if(!lessonIds.has(id))throw new Error(`Undefined related reading ${id}`);
  if(l.sections.length<3||!l.exercise?.options?.length||!l.questions.length)throw new Error(`Incomplete lesson ${l.id}`);
}
for(const t of terms)for(const r of t.sourceRefs)if(!sourceIds.has(r.source))throw new Error(`Unknown glossary source ${r.source}`);
await rm(dist,{recursive:true,force:true});await mkdir(dist,{recursive:true});
for(const file of ['index.html','app.js','core.mjs','storage.mjs','experiments.mjs','epub.mjs','styles.css','manifest.webmanifest','data','assets'])await cp(path.join(root,file),path.join(dist,file),{recursive:true});
const walk=async dir=>{const files=[];for(const name of await readdir(dir)){const p=path.join(dir,name);if((await stat(p)).isDirectory())files.push(...await walk(p));else files.push(p);}return files;};
const files=(await walk(dist)).filter(p=>!p.endsWith('.md')).sort();
const hash=createHash('sha256');let bytes=0;for(const file of files){const data=await readFile(file);bytes+=data.length;hash.update(data);}const version=hash.digest('hex').slice(0,16);
const paths=files.map(p=>'./'+path.relative(dist,p).split(path.sep).join('/'));
const serviceWorker=`// Generated from the complete reading pack. Rebuild after source changes.
const CACHE='ludwig-${version}';
const PREFIX='ludwig-';
const BASE=new URL('./',self.location);
const FILES=${JSON.stringify(paths)};
const URLS=FILES.map(p=>new URL(p,BASE).href);
self.addEventListener('install',event=>event.waitUntil((async()=>{const cache=await caches.open(CACHE);await cache.addAll(URLS);})()));
self.addEventListener('activate',event=>event.waitUntil((async()=>{await self.clients.claim();const keys=await caches.keys();await Promise.all(keys.filter(k=>k.startsWith(PREFIX)&&k!==CACHE).map(k=>caches.delete(k)));})()));
self.addEventListener('fetch',event=>{
  const url=new URL(event.request.url);
  if(event.request.method!=='GET'||url.origin!==BASE.origin||!url.pathname.startsWith(BASE.pathname))return;
  if(event.request.mode==='navigate'){event.respondWith((async()=>{const cache=await caches.open(CACHE);return await cache.match(new URL('./index.html',BASE).href)||fetch(event.request);})());return;}
  if(!URLS.includes(url.href))return;
  event.respondWith((async()=>{const cache=await caches.open(CACHE);const saved=await cache.match(event.request);return saved||fetch(event.request);})());
});
self.addEventListener('message',event=>{
 if(event.data?.type==='SKIP_WAITING')self.skipWaiting();
 if(event.data?.type==='OFFLINE_STATUS')event.waitUntil((async()=>{const cache=await caches.open(CACHE);const present=await Promise.all(URLS.map(url=>cache.match(url)));event.ports[0]?.postMessage({ready:present.every(Boolean),count:present.filter(Boolean).length,total:URLS.length,version:CACHE});})());
});
`;
await writeFile(path.join(dist,'sw.js'),serviceWorker);
await writeFile(path.join(dist,'build-info.json'),JSON.stringify({version,readings:lessons.length,terms:terms.length,sources:sources.length,packBytes:bytes},null,2));
console.log(`Built Ludwig ${version}: ${lessons.length} readings, ${terms.length} terms, ${sources.length} sources. Offline pack ${(bytes/1024/1024).toFixed(2)} MB.`);
