/* Actual offline Chromium tests of language switching and unchanged GL geometry. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const http = require('node:http');
const crypto = require('node:crypto');
const cp = require('node:child_process');
const { chromium } = require(process.env.ORCA_PLAYWRIGHT_MODULE || 'playwright');
const root=path.resolve(__dirname,'..');
const output=path.resolve(process.env.ORCA_LOCALE_OUTPUT || path.join(root,'test-output','locales'));
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'gear-locales-'));
const errors=[], records=[];
function gpuHook(){
  window.__glAudit={live:new Map(),uploads:[],deleted:0,errors:[]};
  for(const proto of [window.WebGLRenderingContext?.prototype,window.WebGL2RenderingContext?.prototype]){
    if(!proto || Object.hasOwn(proto,'__gearAuditHook'))continue;
    Object.defineProperty(proto,'__gearAuditHook',{value:true});
    const bind=proto.bindBuffer, data=proto.bufferData, del=proto.deleteBuffer;
    proto.bindBuffer=function(target,buffer){this.__bound ||= new Map();this.__bound.set(target,buffer);return bind.apply(this,arguments)};
    proto.bufferData=function(target,value){
      const buffer=this.__bound?.get(target);
      const bytes=typeof value==='number'?new Uint8Array(value):new Uint8Array(value.buffer,value.byteOffset,value.byteLength);
      let hash=2166136261;for(const byte of bytes){hash^=byte;hash=Math.imul(hash,16777619)}
      const info={bytes:bytes.length,hash:hash>>>0,target};
      window.__glAudit.live.set(buffer,info);window.__glAudit.uploads.push(info);
      return data.apply(this,arguments);
    };
    proto.deleteBuffer=function(buffer){if(buffer){window.__glAudit.live.delete(buffer);window.__glAudit.deleted++}return del.apply(this,arguments)};
  }
}
async function stats(page){return page.evaluate(()=>({live:[...window.__glAudit.live.values()].filter(x=>x.bytes>648),deleted:window.__glAudit.deleted,uploads:window.__glAudit.uploads.filter(x=>x.bytes>648).length,htmlLang:document.documentElement.lang}))}
async function main(){
  fs.mkdirSync(output,{recursive:true});
  cp.execFileSync(process.env.ORCA_TEST_PYTHON || 'python',['-B','-W','error',path.join(__dirname,'render_locale_fixtures.py'),temp],{cwd:root});
  const pages=JSON.parse(fs.readFileSync(path.join(temp,'pages.json'),'utf8'));
  const languageCount = new Set(pages.map(x=>x.lang)).size;
  for(const code of ['ru','cs','zh'])assert(pages.some(item=>item.lang===code),'missing published language '+code);
  const server=http.createServer((req,res)=>{
    const name=path.basename(new URL(req.url,'http://localhost').pathname);
    if(name==='favicon.ico'){res.writeHead(204);return res.end()}
    if(!pages.some(x=>x.file===name)){res.writeHead(404);return res.end()}
    res.setHeader('content-type','text/html; charset=utf-8');res.end(fs.readFileSync(path.join(temp,name)));
  });
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  const base=`http://127.0.0.1:${server.address().port}`;
  let browser;
  try{
    browser=await chromium.launch({headless:true,executablePath:process.env.ORCA_CHROMIUM_EXECUTABLE || undefined});
    let baselineHash;
    for(const item of pages){
      const context=await browser.newContext({viewport:{width:item.mode==='dock'?360:1600,height:900}});
      const page=await context.newPage();
      page.on('pageerror',e=>errors.push(String(e)));page.on('console',m=>{if(m.type()==='error')errors.push(m.text())});
      await page.addInitScript(gpuHook);
      await page.goto(`${base}/${item.file}`);
      await page.waitForFunction(()=>window.__glAudit?.uploads.length>=10);
      assert.equal(await page.locator('html').getAttribute('lang'),item.lang);
      assert.equal(await page.locator('#lang-select').inputValue(),item.lang);
      assert.equal(await page.locator('#lang-select option').count(),languageCount);
      assert.equal(await page.locator('.preset-name').first().textContent(),'Save','user text was translated');
      const initial=await stats(page);
      const hash=crypto.createHash('sha256').update(JSON.stringify(initial.live)).digest('hex');
      baselineHash ||= hash; assert.equal(hash,baselineHash,'changing locale/theme/mode changed geometric buffers');
      const visibleOverflow=await page.locator('.quick-pill,.seg-btn').evaluateAll(nodes=>nodes.filter(x=>x.getBoundingClientRect().width>0 && x.scrollWidth>x.clientWidth+1 && !['hidden','clip'].includes(getComputedStyle(x).overflowX)).map(x=>x.textContent));
      assert.deepEqual(visibleOverflow,[],'uncontained translated buttons');
      if(['ru','cs','zh'].includes(item.lang))await page.screenshot({path:path.join(output,item.lang+'-'+item.mode+'-'+item.theme+'.png')});
      if(item.lang==='it' && item.mode==='page' && item.theme==='light')await page.screenshot({path:path.join(output,'italian-page-light.png')});
      records.push({...item,geometry_hash:hash,large_buffer_bytes:initial.live.reduce((a,x)=>a+x.bytes,0)});
      await context.close();
    }
    const context=await browser.newContext({viewport:{width:1600,height:1000}});
    const page=await context.newPage();page.on('pageerror',e=>errors.push(String(e)));page.on('console',m=>{if(m.type()==='error')errors.push(m.text())});await page.addInitScript(gpuHook);
    await page.goto(`${base}/page-light-en.html`);await page.waitForFunction(()=>window.__glAudit.uploads.length>=10);
    // Capture bridge requests without running exports or native Orca.
    await page.evaluate(()=>{window.__sent=[];window.chrome ||= {};window.chrome.webview={postMessage:msg=>window.__sent.push(typeof msg==='string'?JSON.parse(msg):msg),addEventListener(){}}});
    const before=await stats(page);
    await page.locator('#lang-select').selectOption('it');await page.locator('#lang-select').selectOption('ja');
    await page.evaluate(()=>{
      const reqs=window.__sent.filter(x=>x.type==='ui_preferences');
      window.dispatchEvent(new MessageEvent('message',{data:{type:'ui_preferences',lang:reqs[0].lang,language_request_id:reqs[0].language_request_id,language_revision:1}}));
    });
    assert.equal(await page.locator('html').getAttribute('lang'),'ja','stale preference acknowledgement won');
    await page.evaluate(()=>{
      const req=window.__sent.filter(x=>x.type==='ui_preferences').at(-1);
      window.dispatchEvent(new MessageEvent('message',{data:{type:'ui_preferences',lang:req.lang,language_request_id:req.language_request_id,language_revision:2}}));
    });
    assert.equal(await page.locator('html').getAttribute('lang'),'ja');
    await page.locator('#lang-select').selectOption('fr');
    await page.evaluate(()=>{
      const req=window.__sent.filter(x=>x.type==='ui_preferences').at(-1);
      window.dispatchEvent(new MessageEvent('message',{data:{type:'ui_preferences',lang:'de',language_request_id:'other-dock-view-1',language_revision:4}}));
      window.dispatchEvent(new MessageEvent('message',{data:{type:'ui_preferences',lang:'fr',language_request_id:req.language_request_id,language_revision:3}}));
    });
    assert.equal(await page.locator('html').getAttribute('lang'),'de','newer foreign-view choice was lost while own ACK was pending');
    await page.locator('#lang-select').selectOption('ja');
    await page.evaluate(()=>{
      const req=window.__sent.filter(x=>x.type==='ui_preferences').at(-1);
      window.dispatchEvent(new MessageEvent('message',{data:{type:'ui_preferences',lang:'fr',language_request_id:'other-dock-view-2',language_revision:5}}));
      window.dispatchEvent(new MessageEvent('message',{data:{type:'ui_preferences',lang:'ja',language_request_id:req.language_request_id,language_revision:6}}));
      window.dispatchEvent(new MessageEvent('message',{data:{type:'ui_preferences',lang:'de',language_request_id:'other-dock-view-1',language_revision:4}}));
    });
    assert.equal(await page.locator('html').getAttribute('lang'),'ja','older foreign-view choice overrode newer own ACK');
    assert.equal((await stats(page)).uploads,before.uploads,'language switch rebuilt geometric buffers');
    await page.locator('#inp-gear-name').fill('My custom 日本語');
    await page.locator('#inp-gear-name').dispatchEvent('change');
    await page.locator('[data-action="export_stl"]').first().click();
    const request=await page.evaluate(()=>window.__sent.filter(x=>x.type==='export_file').at(-1));
    assert.equal(request.params.name,'My custom 日本語');assert.equal(request.format,'stl');
    const wireOff=await stats(page);
    await page.locator('#btn-vp-wire').click();const wireOn=await stats(page);
    assert.ok(wireOn.live.reduce((a,x)=>a+x.bytes,0)>wireOff.live.reduce((a,x)=>a+x.bytes,0),'wire buffers missing');
    await page.locator('#btn-vp-wire').click();const wireFreed=await stats(page);
    assert.equal(wireFreed.live.reduce((a,x)=>a+x.bytes,0),wireOff.live.reduce((a,x)=>a+x.bytes,0));
    assert.ok(wireFreed.deleted>wireOff.deleted,'wire buffers not freed');
    await page.locator('[data-vp-view="fit_kit"]').click();const kitOn=await stats(page);
    assert.ok(kitOn.live.length>wireFreed.live.length,'fit kit not uploaded');
    await page.locator('[data-vp-view="meshed"]').click();const kitFreed=await stats(page);
    assert.equal(kitFreed.live.reduce((a,x)=>a+x.bytes,0),wireOff.live.reduce((a,x)=>a+x.bytes,0),'unused kit allocations retained');
    await page.reload();assert.equal(await page.locator('#lang-select').inputValue(),'ja','manual locale not restored');
    await context.close();
    assert.deepEqual(errors,[]);
    const source_hashes={};for(const name of ['studio_ui.py','locale_catalog.py','plugin_main.py'])source_hashes[name]=crypto.createHash('sha256').update(fs.readFileSync(path.join(root,'src','gear_studio',name))).digest('hex');
    const report={ok:true,pages:records,console_errors:errors,geometry_hash:baselineHash,source_hashes,wire_bytes:{off:wireOff.live.reduce((a,x)=>a+x.bytes,0),on:wireOn.live.reduce((a,x)=>a+x.bytes,0),off_again:wireFreed.live.reduce((a,x)=>a+x.bytes,0)},scope:records.length+' isolated Chromium pages, locale persistence/late acknowledgements, preserved user names, bridge export request, exact per-locale GL buffers and lazy-wire lifecycle; no native app or actual export'};
    fs.writeFileSync(path.join(output,'report.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({ok:true,pages:records.length,wire_bytes:report.wire_bytes}));
  } finally {if(browser)await browser.close();await new Promise(resolve=>server.close(resolve));fs.rmSync(temp,{recursive:true,force:true})}
}
main().catch(error=>{fs.mkdirSync(output,{recursive:true});fs.writeFileSync(path.join(output,'failure.txt'),error.stack);console.error(error);process.exitCode=1});
