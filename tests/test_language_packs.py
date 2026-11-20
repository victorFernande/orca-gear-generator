"""A future language is one data file, not a Python/JavaScript feature edit."""
from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from gear_studio.language_packs import load_language_packs, validate_language_pack, resolve_language
from gear_studio.locale_catalog import LANGUAGE_PACKS, SUPPORTED_LANGUAGES


def synthetic(code="nl", name="Nederlands"):
    return {"schema_version":1,"code":code,"native_name":name,"direction":"ltr","order":7,
            "translations":{"Randomize":"Willekeurig", "Save":"Opslaan"}}


def write_pack(folder, name, pack):
    path=folder/name
    path.write_text(json.dumps(pack,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    return path


class LanguagePackTests(unittest.TestCase):
    def test_metadata_is_discovered_and_regional_precedence_is_dynamic(self):
        with tempfile.TemporaryDirectory() as td:
            folder=Path(td)
            write_pack(folder,'nl.json',synthetic())
            write_pack(folder,'regional.json',synthetic('nl-NL','Nederlands (Nederland)'))
            packs, errors=load_language_packs(folder,embedded={},strict=True)
            self.assertFalse(errors)
            self.assertIn('nl',packs)
            self.assertEqual(resolve_language('NL_nl.UTF-8',packs),'nl-nl')
            self.assertEqual(resolve_language('nl_BE',packs),'nl')
            self.assertEqual(resolve_language('zz_ZZ',packs),'en')
            self.assertEqual(packs['nl']['translations'].get('Missing label','Missing label'),'Missing label')
            self.assertEqual(tuple(LANGUAGE_PACKS), SUPPORTED_LANGUAGES)

    def test_bad_optional_data_does_not_disable_english_but_strict_build_rejects(self):
        malformed=[
            '{broken',
            '{"schema_version":1,"schema_version":1,"code":"nl","native_name":"Nederlands","translations":{}}',
            json.dumps({**synthetic(),"schema_version":True}),
            json.dumps({**synthetic(),"code":True}),
            json.dumps({**synthetic(),"native_name":"<script>bad</script>"}),
            json.dumps({**synthetic(),"native_name":"bad\nname"}),
            json.dumps({**synthetic(),"translations":{"Files {count}":"Bestanden"}}),
            json.dumps({**synthetic(),"translations":{"Save":"<img src=x>"}}),
            json.dumps({**synthetic(),"translations":{"":"leeg"}}),
        ]
        for content in malformed:
            with self.subTest(content=content),tempfile.TemporaryDirectory() as td:
                folder=Path(td);(folder/'bad.json').write_text(content,encoding='utf-8')
                packs,errors=load_language_packs(folder,embedded={})
                self.assertIn('en',packs);self.assertTrue(errors)
                with self.assertRaises(ValueError):load_language_packs(folder,embedded={},strict=True)
        with tempfile.TemporaryDirectory() as td:
            folder=Path(td);write_pack(folder,'one.json',synthetic());write_pack(folder,'two.json',synthetic())
            with self.assertRaises(ValueError):load_language_packs(folder,embedded={},strict=True)
        with self.assertRaises(ValueError):
            load_language_packs(Path('missing-test-locale-folder'),embedded={'one':synthetic(),'two':synthetic()},strict=True)

    def test_sidecar_overrides_only_requested_phrases_and_preserves_placeholders(self):
        with tempfile.TemporaryDirectory() as td:
            folder=Path(td)
            embedded={'nl':{**synthetic(), 'translations':{'Randomize':'Oud','Save':'Opslaan'}}}
            write_pack(folder,'nl.json',{**synthetic(),'translations':{'Randomize':'Nieuw'}})
            packs,_=load_language_packs(folder,embedded=embedded,strict=True)
            self.assertEqual(packs['nl']['translations'],{'Randomize':'Nieuw','Save':'Opslaan'})
            valid=validate_language_pack({**synthetic(),'translations':{'Files {count}: {path}':'Bestanden {count}: {path}'}})
            self.assertIn('{path}',valid['translations']['Files {count}: {path}'])

    def test_added_json_is_packaged_and_recognized_by_source_both_bundles_and_wheel(self):
        with tempfile.TemporaryDirectory() as td:
            project=Path(td)/'project';project.mkdir()
            shutil.copytree(ROOT/'src',project/'src',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
            (project/'scripts').mkdir()
            shutil.copyfile(ROOT/'scripts/build_and_install.py',project/'scripts/build_and_install.py')
            for name in ('pyproject.toml','README.md','LICENSE'):shutil.copyfile(ROOT/name,project/name)
            packs=project/'src/gear_studio/locales'
            for existing in packs.glob('*.json'):
                code=json.loads(existing.read_text(encoding='utf-8')).get('code','').lower().replace('_','-')
                if code in {'nl','nl-nl'}:existing.unlink()
            write_pack(packs,'nl.json',synthetic())
            write_pack(packs,'nl-nl.json',synthetic('nl-nl','Nederlands (Nederland)'))
            env={k:v for k,v in os.environ.items() if k!='PYTHONPATH'}
            def invoke(code,*args):
                result=subprocess.run([sys.executable,'-B','-W','error','-c',code,*map(str,args)],cwd=project,env=env,check=True,capture_output=True,text=True)
                return json.loads(result.stdout.strip().splitlines()[-1])
            inspect='''import json,sys
sys.path.insert(0,sys.argv[1])
from gear_studio.locale_catalog import SUPPORTED_LANGUAGES, normalize_language, TRANSLATION_CATALOG
from gear_studio.plugin_main import _detect_language
from gear_studio.studio_ui import get_studio_html
print(json.dumps({'codes':list(SUPPORTED_LANGUAGES),'resolved':normalize_language('nl_NL.UTF-8'),'host':_detect_language({'language':'nl_NL'}),'translated':TRANSLATION_CATALOG['nl']['Randomize'],'page':get_studio_html('page',{'lang':'nl'}),'dock':get_studio_html('dock',{'lang':'nl-nl'})}))
'''
            source=invoke(inspect,project/'src')
            self.assertEqual(source['resolved'],'nl-nl');self.assertEqual(source['host'],'nl-nl')
            self.assertIn('nl',source['codes']);self.assertEqual(source['translated'],'Willekeurig')
            self.assertIn('Nederlands',source['page']);self.assertIn('lang="nl-nl"',source['dock'])
            subprocess.run([sys.executable,'-B','-W','error',str(project/'scripts/build_and_install.py'),'--no-install'],cwd=project,env=env,check=True,capture_output=True,text=True)
            bundle_inspect='''import importlib.util,json,sys
s=importlib.util.spec_from_file_location('gear_extra_locale',sys.argv[1]);m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)
print(json.dumps({'codes':list(m.SUPPORTED_LANGUAGES),'resolved':m.normalize_language('nl_NL.UTF-8'),'translated':m.TRANSLATION_CATALOG['nl']['Randomize'],'html':m.get_studio_html('dock',{'lang':'nl-nl'})}))
'''
            for filename in ('orca_gear_generator.py','orca_gear_generator_any.py'):
                result=invoke(bundle_inspect,project/'dist'/filename)
                self.assertIn('nl',result['codes']);self.assertEqual(result['resolved'],'nl-nl')
                self.assertEqual(result['translated'],'Willekeurig');self.assertIn('lang="nl-nl"',result['html'])
            wheel=next((project/'dist').glob('*.whl'));extract=project/'wheel-extracted'
            with zipfile.ZipFile(wheel) as archive:
                self.assertIn('gear_studio/locales/nl.json',archive.namelist())
                self.assertIn('gear_studio/locales/nl-nl.json',archive.namelist())
                archive.extractall(extract)
            result=invoke(inspect,extract)
            self.assertEqual(result['resolved'],'nl-nl');self.assertIn('nl',result['codes'])
            # Adding data next to an existing standalone file also works on restart.
            sidecar=project/'dist/locales';sidecar.mkdir()
            write_pack(sidecar,'pl.json',synthetic('pl','Polski'))
            result=invoke(bundle_inspect,project/'dist/orca_gear_generator.py')
            self.assertIn('pl',result['codes'])
            # A malformed source pack stops both release builders, not just runtime discovery.
            (packs/'broken.json').write_text('{',encoding='utf-8')
            spec=importlib.util.spec_from_file_location('gear_invalid_pack_build',project/'scripts/build_and_install.py')
            builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)
            with self.assertRaises(ValueError):builder.build_bundle()
            with self.assertRaises(ValueError):builder.build_wheel()


if __name__=='__main__':unittest.main()
