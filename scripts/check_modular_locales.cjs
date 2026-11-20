/* One new data pack must work in the actual production UI without code edits. */
'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),os=require('node:os'),http=require('node:http'),cp=require('node:child_process'),crypto=require('node:crypto');
const {chromium}=require(process.env.ORCA_PLAYWRIGHT_MODULE || 'playwright');
const root=path.resolve(__dirname,'..'),temp=fs.mkdtempSync(path.join(os.tmpdir(),'gear-added-pack-'));
const output=path.resolve(process.env.ORCA_LOCALE_OUTPUT || path.join(root,'test-output','modular-locales'));
async function main(){
  const project=path.join(temp,'project'),folder=path.join(project,'src','gear_studio','locales'),pagesFolder=path.join(temp,'pages');
  fs.cpSync(path.join(root,'src'),path.join(project,'src'),{recursive:true,filter:x=>!x.includes('__pycache__')});
  // Replace these fixture identities only in the private copy, even if a future
  // contributor already supplied the same language under another filename.
  for(const name of fs.readdirSync(folder).filter(x=>x.endsWith('.json'))){
    const existing=JSON.parse(fs.readFileSync(path.join(folder,name),'utf8'));
    const code=String(existing.code).toLowerCase().replaceAll('_','-');
    if(['nl','nl-nl'].includes(code))fs.unlinkSync(path.join(folder,name));
  }
  const pack={schema_version:1,code:'nl',native_name:'Nederlands',direction:'ltr',order:7,translations:{Randomize:'Willekeurig'}};
  fs.writeFileSync(path.join(folder,'nl.json'),JSON.stringify(pack));
  fs.writeFileSync(path.join(folder,'nl-nl.json'),JSON.stringify({...pack,code:'nl-nl',native_name:'Nederlands (Nederland)',order:8,translations:{Randomize:'Willekeurig NL','ui:btn_random::Randomize':'Willekeurig context'}}));
  for(const code of ['pt','en']){
    const filename=path.join(folder,code+'.json'),existing=JSON.parse(fs.readFileSync(filename,'utf8'));
    Object.assign(existing.translations,{'Randomize':code+' JSON button','Helix Angle (β)':code+' JSON parameter','Toggle Light/Dark Theme':code+' JSON tooltip'});
    fs.writeFileSync(filename,JSON.stringify(existing));
  }
  cp.execFileSync(process.env.ORCA_TEST_PYTHON || 'python',['-B','-W','error',path.join(__dirname,'render_locale_fixtures.py'),pagesFolder],{cwd:project,env:{...process.env,ORCA_LOCALE_SOURCE_ROOT:project}});
  const languageCount = new Set(JSON.parse(fs.readFileSync(path.join(pagesFolder,'pages.json'),'utf8')).map(x=>x.lang)).size;
  const server=http.createServer((req,res)=>{const name=path.basename(new URL(req.url,'http://localhost').pathname);if(name==='favicon.ico'){res.writeHead(204);return res.end()};if(!/^((page|dock)-(light|dark)-(nl|nl-nl|pt|en))\.html$/.test(name)){res.writeHead(404);return res.end()};res.setHeader('content-type','text/html;charset=utf-8');res.end(fs.readFileSync(path.join(pagesFolder,name)))});
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));const base=`http://127.0.0.1:${server.address().port}`;
  let browser;const errors=[],checks=[];
  try{
    browser=await chromium.launch({headless:true,executablePath:process.env.ORCA_CHROMIUM_EXECUTABLE || undefined});
    for(const mode of ['page','dock'])for(const theme of ['light','dark'])for(const lang of ['nl','nl-nl']){
      const context=await browser.newContext({viewport:{width:mode==='dock'?360:1600,height:900}}),page=await context.newPage();
      page.on('pageerror',e=>errors.push(String(e)));page.on('console',m=>{if(m.type()==='error')errors.push(m.text())});
      await page.goto(`${base}/${mode}-${theme}-${lang}.html`);
      assert.equal(await page.locator('#lang-select option').count(),languageCount);
      assert.equal(await page.locator('html').getAttribute('lang'),lang);
      assert.equal(await page.locator('html').getAttribute('dir'),'ltr');
      assert.equal(await page.locator('#lang-select').inputValue(),lang);
      assert.equal(await page.locator('[data-i18n="btn_random"]').first().textContent(),lang==='nl'?'Willekeurig':'Willekeurig context');
      assert.equal(await page.locator('[data-i18n="sec_presets"]').first().textContent(),'Mechanical Presets','missing partial-pack phrase did not fall back to English');
      assert.equal(await page.locator('.preset-name').first().textContent(),'Save','personal preset name changed');
      await page.locator('#lang-select').selectOption(lang==='nl'?'nl-nl':'nl');
      assert.equal(await page.locator('[data-i18n="btn_random"]').first().textContent(),lang==='nl'?'Willekeurig context':'Willekeurig');
      await page.reload();assert.equal(await page.locator('#lang-select').inputValue(),lang==='nl'?'nl-nl':'nl');
      checks.push({mode,theme,lang,result:'PASS'});await context.close();
    }
    for(const mode of ['page','dock'])for(const theme of ['light','dark'])for(const lang of ['pt','en']){
      const context=await browser.newContext({viewport:{width:mode==='dock'?360:1600,height:900}}),page=await context.newPage();
      page.on('pageerror',e=>errors.push(String(e)));page.on('console',m=>{if(m.type()==='error')errors.push(m.text())});
      await page.goto(`${base}/${mode}-${theme}-${lang}.html`);
      assert.equal(await page.locator('[data-i18n="btn_random"]').first().textContent(),lang+' JSON button','existing locale ignored JSON control override');
      assert.equal(await page.locator('[data-spec-label="helix_angle_deg"]').first().textContent(),lang+' JSON parameter','existing locale ignored JSON parameter override');
      assert.equal(await page.locator('#btn-theme').getAttribute('title'),lang+' JSON tooltip','existing locale ignored JSON tooltip override');
      assert.equal(await page.locator('.preset-name').first().textContent(),'Save');
      checks.push({mode,theme,lang,kind:'existing-language JSON-only edit',result:'PASS'});await context.close();
    }
    assert.deepEqual(errors,[]);fs.mkdirSync(output,{recursive:true});
    const report={ok:true,scope:'Real Chromium page/dock/light/dark combinations from two synthetic JSON files added only to a private source copy; plus PT/EN JSON-only edits of controls, parameters and tooltips; dynamic selector, context-key precedence, partial English fallback, personal names and restart persistence.',production_synthetic_packs_committed:false,checks,console_errors:errors,source_hashes:{'studio_ui.py':crypto.createHash('sha256').update(fs.readFileSync(path.join(root,'src','gear_studio','studio_ui.py'))).digest('hex')}};
    fs.writeFileSync(path.join(output,'report.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({ok:true,cases:checks.length}));
  }finally{if(browser)await browser.close();await new Promise(resolve=>server.close(resolve))}
}
main().catch(e=>{console.error(e);process.exitCode=1}).finally(()=>fs.rmSync(temp,{recursive:true,force:true}));
