const DB_NAME='ludwig-local';
let connection;
export async function openDatabase() {
  if(connection)return connection;
  connection=await new Promise((resolve,reject)=>{
    const req=indexedDB.open(DB_NAME,1);
    req.onupgradeneeded=()=>{const db=req.result;db.createObjectStore('notes',{keyPath:'id'});db.createObjectStore('preferences');db.createObjectStore('files',{keyPath:'id'});};
    req.onsuccess=()=>resolve(req.result);
    req.onerror=()=>reject(req.error);
    req.onblocked=()=>reject(new Error('Close other Ludwig tabs, then reload.'));
  });
  connection.onversionchange=()=>{connection.close();connection=null;};
  return connection;
}
async function transaction(store,mode,action) {
  const db=await openDatabase();
  return new Promise((resolve,reject)=>{
    const tx=db.transaction(store,mode);let result;
    try {const req=action(tx.objectStore(store));if(req)req.onsuccess=()=>{result=req.result;};} catch(e){tx.abort();reject(e);return;}
    tx.oncomplete=()=>resolve(result);tx.onerror=()=>reject(tx.error);tx.onabort=()=>reject(tx.error??new Error('Storage was interrupted.'));
  });
}
export const getNotes=()=>transaction('notes','readonly',s=>s.getAll());
export const putNote=note=>transaction('notes','readwrite',s=>s.put(note));
export const deleteNote=id=>transaction('notes','readwrite',s=>s.delete(id));
export const getPreferences=async()=>await transaction('preferences','readonly',s=>s.get('settings'))??{};
export const putPreferences=p=>transaction('preferences','readwrite',s=>s.put(p,'settings'));
export const getFile=id=>transaction('files','readonly',s=>s.get(id));
export const putFile=file=>transaction('files','readwrite',s=>s.put(file));
export const deleteFile=id=>transaction('files','readwrite',s=>s.delete(id));
export const getFileKeys=()=>transaction('files','readonly',s=>s.getAllKeys());
export async function importBackupAtomic(notes,preferences) {
  const db=await openDatabase();
  return new Promise((resolve,reject)=>{const tx=db.transaction(['notes','preferences'],'readwrite');for(const n of notes)tx.objectStore('notes').put(n);tx.objectStore('preferences').put(preferences,'settings');tx.oncomplete=resolve;tx.onerror=()=>reject(tx.error);tx.onabort=()=>reject(tx.error??new Error('Import failed.'));});
}
