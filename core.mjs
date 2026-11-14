export const NAV = [
  ['home','Home','home'],['readings','Readings','book'],['explore','Experiments','spark'],['daily','Today','sun'],['glossary','Key words','type'],['sources','Sources','library'],['notebook','Notes','pen']
];
export function localDate(date = new Date()) {
  return `${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}-${String(date.getDate()).padStart(2,'0')}`;
}
export function dailyIndex(length, date = localDate()) {
  if (!length) return 0;
  const [y,m,d] = date.split('-').map(Number);
  return ((Math.floor(Date.UTC(y,m-1,d)/86400000) % length) + length) % length;
}
export function escapeHtml(value = '') { return String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }
export function normalize(text) { return String(text ?? '').normalize('NFKD').replace(/[\u0300-\u036f]/g,'').toLowerCase(); }
export function matchQuery(query, ...values) { return normalize(query).trim().split(/\s+/).every(word=>normalize(values.flat(Infinity).join(' ')).includes(word)); }
export function makeId() { return globalThis.crypto?.randomUUID?.() ?? `n-${Date.now()}-${Math.random().toString(36).slice(2)}`; }
export function validateBackup(data) {
  if (!data || data.app !== 'ludwig' || data.version !== 1 || !Array.isArray(data.notes) || !data.preferences || typeof data.preferences !== 'object' || Array.isArray(data.preferences)) throw new Error('This is not a Ludwig backup.');
  if(data.notes.length>10000) throw new Error('This backup contains too many notes.');
  for (const n of data.notes) {
    if (!n || typeof n.id !== 'string' || !n.id || n.id.length > 200 || typeof n.title !== 'string' || typeof n.body !== 'string' || n.title.length>1000 || n.body.length>1000000 || typeof n.updated !== 'string' || Number.isNaN(Date.parse(n.updated)) || (n.lesson!=null && typeof n.lesson !== 'string') || (n.section!=null && typeof n.section !== 'string')) throw new Error('A note in this backup is invalid. No notes were imported.');
  }
  const p=data.preferences;
  const clean={};
  if (['light','dark','system'].includes(p.theme)) clean.theme=p.theme;
  if (['normal','large','larger'].includes(p.font)) clean.font=p.font;
  for(const key of ['completed','bookmarks','seen']) if(Array.isArray(p[key])) clean[key]=[...new Set(p[key].filter(x=>typeof x==='string'&&x.length<200))];
  if(typeof p.lastLesson==='string'&&p.lastLesson.length<200) clean.lastLesson=p.lastLesson;
  return {notes:data.notes.map(n=>({id:n.id,title:n.title,body:n.body,updated:n.updated,created:typeof n.created==='string'?n.created:n.updated,lesson:n.lesson??null,section:n.section??null})),preferences:clean};
}
export function mergeNotes(current, incoming) {
  const map=new Map(current.map(n=>[n.id,n]));
  for(const n of incoming) { const old=map.get(n.id);if(!old||Date.parse(n.updated)>Date.parse(old.updated))map.set(n.id,n); }
  return [...map.values()];
}
export function noteMarkdown(note) {return `# ${note.title||'Untitled thought'}\n\n${note.body}\n\n---\nUpdated: ${note.updated}\n${note.lesson?`Reading: ${note.lesson}${note.section?' · '+note.section:''}\n`:''}`;}
