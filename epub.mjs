// Minimal, offline EPUB 2/3 text reader. Imports never execute scripts or fetch book resources.
async function unzip(buffer) {
  const view=new DataView(buffer),bytes=new Uint8Array(buffer),entries=new Map();let end=-1;
  for(let i=bytes.length-22;i>=Math.max(0,bytes.length-65557);i--)if(view.getUint32(i,true)===0x06054b50){end=i;break;}
  if(end<0)throw new Error('This EPUB has no readable ZIP directory.');
  const count=view.getUint16(end+10,true);let p=view.getUint32(end+16,true),total=0;
  if(count>5000)throw new Error('This EPUB has too many entries.');
  for(let i=0;i<count;i++){
    if(view.getUint32(p,true)!==0x02014b50)throw new Error('This EPUB directory is damaged.');
    const flags=view.getUint16(p+8,true),method=view.getUint16(p+10,true),compressed=view.getUint32(p+20,true),size=view.getUint32(p+24,true),nl=view.getUint16(p+28,true),el=view.getUint16(p+30,true),cl=view.getUint16(p+32,true),offset=view.getUint32(p+42,true);
    const name=new TextDecoder().decode(bytes.slice(p+46,p+46+nl));p+=46+nl+el+cl;
    if(size>20000000||(total+=size)>100000000)throw new Error('This book is too large for the text reader.');
    if(flags&1)throw new Error('Encrypted EPUBs cannot be opened here.');
    entries.set(name,async()=>{
      if(view.getUint32(offset,true)!==0x04034b50)throw new Error('Damaged EPUB entry.');
      const start=offset+30+view.getUint16(offset+26,true)+view.getUint16(offset+28,true),chunk=bytes.slice(start,start+compressed);
      if(method===0)return new TextDecoder().decode(chunk);
      if(method!==8)throw new Error('Unsupported EPUB compression.');
      const stream=new Blob([chunk]).stream().pipeThrough(new DecompressionStream('deflate-raw'));
      const expanded=await new Response(stream).arrayBuffer();if(expanded.byteLength>20000000)throw new Error('This chapter is too large.');
      return new TextDecoder().decode(expanded);
    });
  }
  return entries;
}
const xml=text=>new DOMParser().parseFromString(text,'application/xml');
const nodes=(doc,name)=>[...doc.getElementsByTagNameNS('*',name)];
function resolvePath(base,path){const parts=(base+'/'+path.split('#')[0]).split('/');const out=[];for(const part of parts){if(part==='..')out.pop();else if(part&&part!=='.')out.push(part);}return decodeURIComponent(out.join('/'));}
export async function readEpub(file) {
  const zip=await unzip(await file.arrayBuffer());
  if(zip.has('META-INF/encryption.xml'))throw new Error('This EPUB declares encrypted resources. Open it with your usual reader.');
  const container=zip.get('META-INF/container.xml');if(!container)throw new Error('This is not a valid EPUB.');
  const opfPath=nodes(xml(await container()),'rootfile')[0]?.getAttribute('full-path');
  const opfEntry=zip.get(opfPath);if(!opfEntry)throw new Error('The EPUB package is missing.');
  const opf=xml(await opfEntry()),base=opfPath.split('/').slice(0,-1).join('/');
  const manifest=new Map(nodes(opf,'item').map(n=>[n.getAttribute('id'),n.getAttribute('href')]));
  const chapters=[];
  for(const ref of nodes(opf,'itemref')){
    if(ref.getAttribute('linear')==='no')continue;
    const href=manifest.get(ref.getAttribute('idref'));if(!href)continue;
    const entry=zip.get(resolvePath(base,href));if(!entry)continue;
    const doc=new DOMParser().parseFromString(await entry(),'text/html');
    doc.querySelectorAll('script,style,iframe,object,embed,link,meta,form,svg,math,img,video,audio,source').forEach(n=>n.remove());
    const safe=document.createElement('div');
    const allowed=new Set(['P','DIV','SECTION','ARTICLE','H1','H2','H3','H4','BLOCKQUOTE','EM','I','STRONG','B','SMALL','SUP','SUB','BR','UL','OL','LI','TABLE','THEAD','TBODY','TR','TH','TD','SPAN','HR','DL','DT','DD']);
    const copy=(from,to)=>{for(const child of from.childNodes){if(child.nodeType===3)to.append(document.createTextNode(child.textContent));else if(child.nodeType===1){const el=document.createElement(allowed.has(child.tagName)?child.tagName.toLowerCase():'span');copy(child,el);to.append(el);}}};
    copy(doc.body,safe);
    if(!safe.textContent.trim())continue;
    chapters.push({title:doc.querySelector('h1,h2,h3')?.textContent?.trim()||`Section ${chapters.length+1}`,html:safe.innerHTML});
  }
  if(!chapters.length)throw new Error('No readable chapters found. Open this EPUB with your usual reader.');
  return {title:nodes(opf,'title')[0]?.textContent||file.name,chapters};
}
