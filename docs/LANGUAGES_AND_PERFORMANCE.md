# Orca Gear Studio 1.4.0 — idiomas e otimização / languages and optimization

## Português

O seletor do cabeçalho oferece Português, English, Español, Italiano, Français, Deutsch e 日本語. Todos os textos são distribuídos com o plugin; não há tradutor online, download de pacotes nem fonte externa. Use o mesmo seletor na aba principal ou no painel lateral. A escolha manual é salva no armazenamento do próprio plugin e enviada às duas interfaces abertas. Identificadores regionais como `it_IT`, `es-ES` e `ja_JP` são aceitos. Um idioma não suportado usa inglês; quando não há nenhuma informação de idioma, o padrão histórico é português. A escolha manual tem prioridade sobre a configuração do host e respostas antigas não substituem uma escolha mais recente.

O catálogo cobre controles, dicas, nomes e descrições dos 12 presets internos, rótulos técnicos, diagnóstico, mensagens de exportação conhecidas e recursos de calibração. Nomes de projetos, presets pessoais, arquivos e caminhos são preservados. Erros técnicos desconhecidos mantêm a mensagem original em vez de ocultar seu conteúdo. As traduções são uma revisão inicial; não foram certificadas por falantes nativos. Os limites numéricos e as unidades dos parâmetros continuam iguais, sem conversão das medidas de fabricação.

### Adicionar outro idioma

Os sete idiomas iniciais estão em `src/gear_studio/locales/*.json`. O seletor, a detecção do idioma do Orca e os instaladores leem esses arquivos automaticamente. Para incluir outro idioma, crie somente um JSON, sem editar Python, JavaScript ou uma lista de códigos. Exemplo de `src/gear_studio/locales/nl.json`:

```json
{
  "schema_version": 1,
  "code": "nl",
  "native_name": "Nederlands",
  "direction": "ltr",
  "order": 100,
  "translations": {
    "Randomize": "Willekeurig",
    "Save": "Opslaan",
    "Exports folder: {path}": "Exportmap: {path}"
  }
}
```

Use textos de origem em inglês como chaves. Um catálogo parcial de um novo idioma funciona: uma chave ausente aparece em inglês. Traduções fornecidas por JSON têm prioridade também em português e inglês; para manter compatibilidade visual, uma frase ausente no catálogo português ainda pode usar o texto português legado. Preserve exatamente as variáveis entre chaves, como `{path}` e `{count}`, e use somente texto, sem HTML. Quando uma frase precisa de tradução diferente conforme o controle, a chave opcional `ui:<data-i18n-key>::<English phrase>` tem prioridade; por exemplo, `ui:btn_random::Randomize`. `native_name` é o nome exibido no seletor, `order` determina a ordem e `direction` aceita `ltr` ou `rtl`. Um arquivo regional pode usar `code: "nl-nl"`; `nl_NL.UTF-8` encontra primeiro esse código exato e depois tenta `nl`.

Execute na raiz do projeto:

```sh
python -B -W error scripts/build_and_install.py --no-install
python -B -W error -m unittest discover -s tests -v
```

O empacotador descobre todos os JSONs, valida textos e variáveis, inclui os arquivos no wheel e embute os mesmos dados compactados nos dois bundles `.py`. Instale uma variante atualizada e reinicie o OrcaSlicer. Os testes adicionam holandês e sua variante regional somente em uma cópia temporária e demonstram o funcionamento na fonte, no bundle, no `_any.py`, no wheel e na interface real; esses catálogos de teste não fazem parte da distribuição.

Opcionalmente, uma instalação standalone também lê JSONs na pasta `locales` ao lado do arquivo `.py`; numa instalação por wheel, a pasta fica dentro de `gear_studio`. Dados locais válidos sobrescrevem somente as frases fornecidas, mantendo as outras frases embutidas. O carregamento ocorre na abertura, portanto reinicie após editar. Pacotes opcionais corrompidos são ignorados sem bloquear o inglês; um pacote inválido no projeto faz a compilação falhar. Para compartilhar permanentemente um idioma, inclua o JSON no repositório e gere novos instaladores.

A opção por manter os idiomas em cada projeto preserva a instalação independente. Não é necessário instalar um plugin auxiliar. O catálogo no wheel e no repositório permanece legível. O bundle `.py` compacta somente duas constantes de dados — HTML/CSS/JavaScript e frases traduzidas — com a biblioteca padrão. Classes Python, ponte Orca e metadados PEP 723 permanecem visíveis; o código Python não é executado a partir de um bloco opaco. Os textos descompactados são iguais aos originais. A tabela de origem é liberada após construir o catálogo.

A malha de arame conserva suas linhas originais, mas seus buffers gráficos só existem enquanto a opção está ligada. Ao desligar, eles são liberados. Sair da visualização do kit também libera seus quatro conjuntos gráficos; voltar reconstrói as mesmas superfícies. Não há redução da resolução, simplificação de dentes ou troca do motor geométrico. Os cinco módulos de schema, matemática, cinemática, geometria e exportação mantêm os bytes da revisão `3c547d4ef71a4c518addb8e480fa26c6649e1153`.

O relatório [de equivalência](validation/1.4.0-geometry-equivalence.json) compara efetivamente os 12 pares em resolução alta e quatro peças de calibração: 28 peças e 112 hashes de vértices, triângulos, normais e ângulos de overhang, além de dimensões e volumes iguais. Os testes de navegador verificam 28 combinações de idioma, tema e aba/painel, persistência, resposta antiga, pedido de exportação, conservação de nomes pessoais e liberação de buffers. Pedir uma exportação no navegador isolado não prova importação na mesa; os testes Python existentes verificam os arquivos STL/3MF e a ponte simulada.

As medições em [1.4.0-localization-performance.json](validation/1.4.0-localization-performance.json) registram os bytes reais dos pacotes, sete processos Python novos antes e depois, e alocações solicitadas ao WebGL. O wheel pode crescer por incluir cinco idiomas novos mesmo quando o bundle encolhe. Comparações de importação incluem NumPy e não limpam o cache do sistema operacional; pequenas diferenças não comprovam ganho universal de abertura. Não medimos FPS sustentado, memória física total da GPU nem abertura no Orca nativo. 60 FPS e dez minutos para imprimir o kit são metas, dependentes da máquina, da peça e do fatiamento. Esta atualização não instala nada no OrcaSlicer nem publica uma nova assinatura Cloud.

## English

The header selector contains seven fully offline languages: Portuguese, English, Spanish, Italian, French, German and Japanese. It is available in the main tab and dock. A manual choice is saved in the plugin's own storage and synchronized to open views. Regional locale identifiers are normalized. Unsupported languages fall back to English; genuinely absent language information keeps the historical Portuguese default. A saved choice overrides the host, and stale acknowledgements cannot replace the latest selection.

Controls, technical labels, tooltips, all 12 built-in preset names/descriptions, diagnostics and known action messages are translated. User project/preset names, numbers, filenames and paths stay intact. Unknown technical errors preserve their original text. These are initial translations without native-speaker certification. Numeric parameter semantics and manufacturing units are unchanged.

Every project includes its own catalog; there is no dependency on a sibling plugin or runtime network. The wheel keeps readable Python modules and catalogs. The standalone bundle compresses only authored UI/translation data with standard-library codecs; Python classes, bridge code and PEP 723 metadata remain readable. The decoded data is identical to the original. The temporary translation source table is released after catalog construction.

### Adding a future language

Add one `src/gear_studio/locales/<code>.json` file with the schema shown above. No Python/JavaScript locale allowlist needs editing. Metadata drives the selector, native name, ordering and text direction. Translation keys are English source phrases; missing phrases in a new partial language fall back to English. Supplied JSON takes precedence in Portuguese and English too; legacy Portuguese text is retained only when a PT key is absent, preserving visual compatibility. Preserve placeholders exactly and provide plain text. Optional context keys such as `ui:btn_random::Randomize` take precedence for a specific UI control. Exact regional locales are tried before their base language.

Run the no-install builder and tests, distribute one new bundle or wheel, and restart OrcaSlicer. All JSON packs are automatically included in source/wheel packages and compressed as data in both standalone bundles. Optional `locales` files next to a standalone bundle, or inside a wheel's `gear_studio` directory, are read at startup and merge only their supplied phrases. Invalid optional packs cannot disable the English fallback; strict builds reject malformed or duplicate catalogs and mismatched placeholders. Tests add synthetic Dutch and a regional variant only to temporary copies, verifying source, both standalone variants, extracted wheel and actual page/dock UI behavior without committing test languages.

Exact original wire lines are uploaded only while wireframe is enabled and freed when disabled. Four kit GPU parts are released when leaving that view and recreated identically on return. No geometry simplification, tooth resolution reduction or manufacturing-engine change is used. High-resolution comparison covers all 12 preset pairs and four calibration parts, 28 parts and 112 typed-array hashes. The five manufacturing/schema/export source files are byte-identical to baseline `3c547d4ef71a4c518addb8e480fa26c6649e1153`.

The browser test covers 28 locale/theme/page/dock combinations, preference persistence, stale acknowledgements, an export bridge request, preservation of user names and GPU buffer cleanup. Python tests cover actual STL/3MF files and simulated bridges. Browser export requests do not demonstrate native Plater import. Measurements record actual package bytes, seven fresh Python imports before/after including NumPy, and requested WebGL bytes. They are not guarantees of native startup time, total GPU memory or sustained FPS; the OS cache was not cleared. The wheel may grow with the five new languages even while the bundle shrinks. Native Orca/macOS/Linux sessions and physical printing/fit remain outside this verification. This update does not install into OrcaSlicer or publish a Cloud release.
