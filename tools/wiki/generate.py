#!/usr/bin/env python3
"""Generate the GitHub wiki from recipe JSON, registrations and reviewed machine processes."""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import textwrap
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
WIKI = ROOT / 'wiki'
ASSETS = ROOT / 'src/main/resources/assets/novadyne'
DATA = ROOT / 'src/main/resources/data'
JAVA = ROOT / 'src/main/java/com/novadyne'
OUT = WIKI / 'assets/generated'
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
BG, PANEL, TEXT, MUTED, CYAN, GOLD = '#101923', '#1b2a39', '#f0f5fa', '#aabccc', '#56ddce', '#ffd386'
MACHINES = {'macerator':'MaceratorBlockEntity', 'wafer_press':'WaferPressBlockEntity', 'processor':'ProcessorBlockEntity', 'litografia':'LitografiaBlockEntity'}
VANILLA = {'iron_ingot':'Barra de ferro','copper_ingot':'Barra de cobre','gold_ingot':'Barra de ouro','redstone':'Redstone','diamond':'Diamante','emerald':'Esmeralda','netherite_scrap':'Fragmento de netherita','netherite_ingot':'Barra de netherita','water_bucket':'Balde de água','bucket':'Balde vazio','quartz':'Quartzo','clay_ball':'Bola de argila','furnace':'Fornalha','piston':'Pistão','glass':'Vidro','redstone_block':'Bloco de redstone'}
LANG = json.loads((ASSETS/'lang/en_us.json').read_text())
REGISTERED = re.findall(r'registerSimple(?:Item|BlockItem)\("([^\"]+)"', (JAVA/'ModItems.java').read_text())
MATERIALS = [s for s in REGISTERED if s not in MACHINES and not s.startswith('valve_')]
CATALOG = json.loads((ROOT/'tools/wiki/processes.json').read_text())
PROCESSES = CATALOG['processes']
RECIPES = {p.stem:json.loads(p.read_text()) for p in sorted((DATA/'novadyne/recipe').glob('*.json'))}


def name(item):
    if item.startswith('#'): return 'Quartzo (tag c:gems/quartz)'
    ns, key = item.split(':')
    return VANILLA.get(key,key) if ns=='minecraft' else LANG.get('item.novadyne.'+key,LANG.get('block.novadyne.'+key,key))


def link(item, prefix=''):
    label = name(item)
    if item.startswith('novadyne:'):
        return f'[{label}]({prefix}itens/{item.split(":")[1]}.md)'
    return label


def font(size=20,bold=False): return ImageFont.truetype(BOLD if bold else FONT,size)


def icon(item):
    if item.startswith('#'): item='minecraft:quartz'
    ns,key=item.split(':')
    if ns=='novadyne':
        p=ASSETS/('textures/block/'+key+'_front.png' if key in MACHINES else 'textures/item/'+key+'.png')
    else: p=WIKI/'assets/vanilla'/(key+'.png')
    if not p.exists(): raise ValueError('Missing icon: '+item)
    return Image.open(p).convert('RGBA')


def text(draw, xy, value, size=20, color=TEXT, bold=False): draw.text(xy,value,font=font(size,bold),fill=color)


def wrapped(draw, xy, value, width=22, size=18, color=TEXT):
    for i,line in enumerate(textwrap.wrap(value,width)):
        text(draw,(xy[0],xy[1]+i*(size+6)),line,size,color)


def slot(im,x,y,item=None,count=1,size=80):
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((x,y,x+size,y+size),radius=9,fill='#0d151e',outline='#40576a',width=2)
    if item:
        pic=icon(item); factor=(size-18)/max(pic.size)
        pic=pic.resize((round(pic.width*factor),round(pic.height*factor)),Image.Resampling.NEAREST)
        im.paste(pic,(x+(size-pic.width)//2,y+(size-pic.height)//2),pic)
        if count>1:
            d.rectangle((x+size-29,y+size-26,x+size-4,y+size-4),fill=BG)
            text(d,(x+size-27,y+size-28),str(count),19,GOLD,True)


def arrow(d,x,y,w=110):
    d.line((x,y,x+w-16,y),fill=CYAN,width=6)
    d.polygon([(x+w-18,y-13),(x+w,y),(x+w-18,y+13)],fill=CYAN)


def canvas(title,sub,height=440):
    im=Image.new('RGB',(1200,height),BG); d=ImageDraw.Draw(im)
    d.rectangle((0,0,8,height),fill=CYAN)
    text(d,(34,22),'NOVADYNE  /  GUIA DE PRODUÇÃO',15,CYAN,True)
    text(d,(34,52),title,30,TEXT,True)
    text(d,(34,97),sub,17,MUTED)
    return im,d


def render_recipe(key,r):
    typ=r['type'].split(':')[1]
    labels={'crafting_shaped':'BANCADA · posição dos ingredientes importa','crafting_shapeless':'BANCADA · sem posição fixa; a grade é apenas um exemplo','smelting':'FORNALHA · combustível necessário','blasting':'ALTO-FORNO · combustível necessário'}
    im,d=canvas(name(r['result']['id']),labels[typ],480)
    if typ.startswith('crafting'):
        if typ=='crafting_shaped':
            cells=[r['key'].get(c) for row in r['pattern'] for c in row.ljust(3)]
        else: cells=r['ingredients']
        cells=cells+[None]*(9-len(cells))
        for i,item in enumerate(cells):slot(im,42+(i%3)*88,148+(i//3)*88,item)
        arrow(d,350,274,135)
        text(d,(541,151),'RESULTADO',17,CYAN,True)
        slot(im,551,190,r['result']['id'],r['result'].get('count',1),128)
        wrapped(d,(714,202),name(r['result']['id']),29,25)
        text(d,(714,288),str(r['result'].get('count',1))+' unidade(s)',20,GOLD)
    else:
        slot(im,90,189,r['ingredient'],size=100)
        wrapped(d,(45,310),name(r['ingredient']),29)
        arrow(d,275,241,150)
        text(d,(469,200),'CALOR',22,GOLD,True)
        text(d,(451,245),f'{r["cookingtime"]/20:g} s · {r["experience"]} XP',19,MUTED)
        arrow(d,666,241,150)
        slot(im,906,189,r['result']['id'],size=100)
        wrapped(d,(846,310),name(r['result']['id']),29)
    text(d,(35,447),'Quantidades e ingredientes completos na tabela abaixo da imagem.',16,MUTED)
    im.save(OUT/(key+'.png'))


def stats(machine):
    src=(JAVA/'common/blockentity'/(MACHINES[machine]+'.java')).read_text()
    def get(k):return int(re.search(r'\b'+k+r'\s*=\s*([\d_]+)',src).group(1).replace('_',''))
    return {k:get(k) for k in ['MAX_ENERGY','ENERGY_PER_TICK','MAX_PROGRESS']}


def render_process(p):
    s=stats(p['machine'])
    im,d=canvas(p['title'],f'{name("novadyne:"+p["machine"])} · {s["MAX_PROGRESS"]/20:g} s · {s["ENERGY_PER_TICK"]} FE/t · {s["MAX_PROGRESS"]*s["ENERGY_PER_TICK"]:,} FE por ciclo'.replace(',','.'),450)
    text(d,(38,143),'ENTRADAS',16,CYAN,True)
    for i,item in enumerate(p['inputs']):
        x=35+i*130;slot(im,x,180,item)
        wrapped(d,(x,272),name(item),16,16)
        if i<len(p['inputs'])-1:text(d,(x+92,209),'+',25,MUTED)
    arrow(d,434,221,79)
    slot(im,546,171,'novadyne:'+p['machine'],size=100)
    text(d,(538,291),'PROCESSO',16,MUTED)
    arrow(d,681,221,79)
    text(d,(797,143),'SAÍDAS POSSÍVEIS' if p.get('random') else 'SAÍDAS',16,CYAN,True)
    for i,item in enumerate(p['outputs']):
        x=797+i*190;slot(im,x,180,item)
        wrapped(d,(x,272),name(item),22,16)
        if p.get('labels'):text(d,(x,345),p['labels'][i],16,GOLD)
        if i<len(p['outputs'])-1:text(d,(x+109,208),'OU' if p.get('random') else '+',20,GOLD,True)
    text(d,(35,412),p['short_note'],16,MUTED)
    im.save(OUT/(p['id']+'.png'))


def nav(prefix=''):
    return f'[Início]({prefix}README.md) · [Receitas]({prefix}receitas.md) · [Máquinas]({prefix}maquinas.md) · [Materiais]({prefix}materiais.md) · [Valves]({prefix}valves.md) · [Progressão]({prefix}progressao.md) · [Como testar]({prefix}testar.md)\n\n---\n\n'


def write(path,body):
    p=WIKI/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(body.rstrip()+'\n',encoding='utf-8')


def ingredient_list(r):
    if 'pattern' in r:return [r['key'][c] for row in r['pattern'] for c in row if c!=' ']
    return r.get('ingredients',[r.get('ingredient')])


def ingredients_table(items,prefix=''):
    return '| Quantidade | Ingrediente |\n| ---: | --- |\n'+''.join(f'| {n} | {link(item,prefix)} |\n' for item,n in Counter(items).items())


def recipe_section(key,r,prefix=''):
    img=f'{prefix}assets/generated/{key}.png'
    typ=r['type'].split(':')[1]
    s=f'### {name(r["result"]["id"])} — {key}\n\n![Grade ou processo para {name(r["result"]["id"])}]({img})\n\n'
    s+=ingredients_table(ingredient_list(r),prefix)+f'\n**Resultado:** {r["result"].get("count",1)} × {link(r["result"]["id"],prefix)}.\n\n'
    if typ=='crafting_shapeless':s+='**Sem posição fixa:** basta colocar esses ingredientes na bancada, em qualquer ordem.\n\n'
    if typ in ['smelting','blasting']:s+='A tag `c:gems/quartz` contém quartzo vanilla neste mod e pode receber outros itens por datapacks. O combustível não está incluído no ingrediente.\n\n'
    if 'minecraft:water_bucket' in ingredient_list(r):s+='O balde de água tem o balde vazio como restante de crafting vanilla.\n\n'
    s+=f'[Ver JSON da receita]({prefix}../src/main/resources/data/novadyne/recipe/{key}.json)\n\n'
    return s


def process_section(p,prefix=''):
    s=f'### {p["title"]}\n\n![{p["title"]}: entradas e saídas]({prefix}assets/generated/{p["id"]}.png)\n\n'
    s+=ingredients_table(p['inputs'],prefix)
    s+='\n**'+('Resultado sorteado (um por ciclo)' if p.get('random') else 'Resultado')+':** '+(' **ou** ' if p.get('random') else ' + ').join('1 × '+link(i,prefix) for i in p['outputs'])+'.\n\n'+p['note']+'\n\n'
    s+=f'[Ver lógica da máquina]({prefix}../src/main/java/com/novadyne/common/blockentity/{MACHINES[p["machine"]]}.java)\n\n'
    return s


def build():
    OUT.mkdir(parents=True,exist_ok=True)
    for f in OUT.glob('*.png'):f.unlink()
    for key,r in RECIPES.items():render_recipe(key,r)
    for p in PROCESSES:render_process(p)
    for key in REGISTERED:
        icon('novadyne:'+key).resize((96,96),Image.Resampling.NEAREST).save(OUT/('icon_'+key+'.png'))
    # A source-texture header; no additional brand art or runtime assets.
    im,d=canvas('Da matéria-prima ao wafer gravado','WIKI VISUAL  /  Minecraft 26.1.2 · NeoForge 26.1.2.76',280)
    for i,key in enumerate(MACHINES):
        x=40+i*294;slot(im,x,153,'novadyne:'+key,size=80)
        wrapped(d,(x+98,170),name('novadyne:'+key),16,19)
    im.save(OUT/'header.png')
    intro=nav()+'![NovaDyne — linha de produção](assets/generated/header.png)\n\n# NovaDyne · Wiki visual\n\nGuia do conteúdo **implementado** no mod: 4 máquinas, 9 materiais e 7 valves. Nomes em inglês iguais aos exibidos no jogo; explicações em português.\n\n'
    intro+='## Encontre o que precisa\n\n| Guia | O que você encontra |\n| --- | --- |\n| [Todas as receitas](receitas.md) | Grades 3×3, ingredientes, quantidades e resultado |\n| [Máquinas](maquinas.md) | Consumo, duração, slots e processos |\n| [Materiais](materiais.md) | Como obter cada material e onde usar |\n| [Valves](valves.md) | Crafts dos 7 tiers e chance de sucesso |\n| [Progressão](progressao.md) | Ordem para montar sua linha industrial |\n| [Como testar](testar.md) | Instalar o JAR, comandos e testes rápidos |\n\n'
    intro+='## Antes de começar\n\n- As máquinas precisam de energia FE externa. O NovaDyne ainda não possui gerador próprio.\n- Minere as quatro máquinas com **picareta de pedra ou superior**.\n- Engraving e reciclagem aleatória exigem output vazio; retire o resultado antes do próximo ciclo.\n- Capacitores e transistor têm PNGs, mas **não são itens registrados nem funcionais**. Plasma Cannon, veículos e automação de itens também não estão disponíveis.\n\n[Repositório e download do JAR](../README.md) · [Fontes das imagens vanilla](assets/vanilla/SOURCES.md) · [Manutenção da wiki](manutencao.md)\n'
    write('README.md',intro)
    write('receitas.md',nav()+'# Todas as receitas\n\nAs grades usam os PNGs reais do mod e texturas vanilla. Ícones de máquinas e blocos mostram uma face da textura; não são capturas 3D do jogo.\n\n## Bancada e fornos\n\n'+''.join(recipe_section(k,r) for k,r in RECIPES.items())+'## Processamento nas máquinas\n\n'+''.join(process_section(p) for p in PROCESSES))
    for key in REGISTERED:
        item='novadyne:'+key
        s=nav('../')+f'# {name(item)}\n\n![{name(item)}](../assets/generated/icon_{key}.png)\n\n`{item}`\n\n'
        if key in MACHINES:
            st=stats(key);s+='## Operação\n\n| Propriedade | Valor |\n| --- | --- |\n'+f'| Capacidade | {st["MAX_ENERGY"]:,} FE |\n| Consumo | {st["ENERGY_PER_TICK"]} FE/t |\n| Duração | {st["MAX_PROGRESS"]} ticks / {st["MAX_PROGRESS"]/20:g} s |\n| Energia por ciclo | {st["ENERGY_PER_TICK"]*st["MAX_PROGRESS"]:,} FE |\n'.replace(',','.')+'\nTempos consideram 20 ticks por segundo. A extração externa de energia é bloqueada. Sem energia suficiente para o próximo tick, o progresso é zerado.\n\n'+CATALOG['machines'][key]+'\n\n'
        elif key.startswith('valve_'):
            tier=int(key[-1]);s+=f'**Upgrade da Lithography.** Tier {tier}: {(0.70+(tier-1)*0.25/6)*100:.2f}% de sucesso e {(0.30-(tier-1)*0.25/6)*100:.2f}% de falha na gravação. A valve não é consumida.\n\n'.replace('.00%','%')
        else:s+=CATALOG['materials'][key]+'\n\n'
        sources=[(k,r) for k,r in RECIPES.items() if r['result']['id']==item]
        processes=[p for p in PROCESSES if item in p['outputs']]
        s+='## Como obter\n\n'
        s+=''.join(recipe_section(k,r,'../') for k,r in sources)
        s+=''.join(process_section(p,'../') for p in processes)
        if not sources and not processes:s+='Sem receita de obtenção implementada.\n\n'
        s+='## Onde usar\n\n'
        uses=[f'- Craft de {link(r["result"]["id"],"../")}.' for r in RECIPES.values() if item in ingredient_list(r)]
        uses += [f'- {p["title"]}, em {link("novadyne:"+p["machine"],"../")}.' for p in PROCESSES if item in p['inputs']]
        if key.startswith('valve_'):uses+=['- Slot de valve da [Lithography](litografia.md); melhora a chance de sucesso.']
        s+='\n'.join(uses) if uses else 'Sem consumo em outra receita implementada no momento.'
        if key in MACHINES:s+='\n\n## Processos\n\n'+''.join(process_section(p,'../') for p in PROCESSES if p['machine']==key)
        s+=f'\n\n## Teste em criativo\n\n```mcfunction\n/give @s {item}\n```\n'
        write('itens/'+key+'.md',s)
    def index(keys):
        return '| Ícone | Item | ID |\n| --- | --- | --- |\n'+''.join(f'| <img src="assets/generated/icon_{k}.png" width="48" alt="{name("novadyne:"+k)}"> | {link("novadyne:"+k)} | `{k}` |\n' for k in keys)
    write('materiais.md',nav()+'# Materiais\n\nClique no nome para ver obtenção, craft e usos.\n\n'+index(MATERIALS))
    write('maquinas.md',nav()+'# Máquinas\n\n'+index(MACHINES)+'\n## Regras comuns\n\n- Use energia externa FE ou, em testes com comandos, preencha o campo `energy`. Não há geração própria.\n- Picareta de pedra ou superior permite recuperar o bloco. Ao quebrar, o inventário é derrubado; energia e progresso não são preservados no item da máquina.\n- Output incompatível/cheio bloqueia o processamento. Não há transporte automático de itens implementado.\n- As valves têm efeito na Lithography. Os slots presentes nas outras máquinas ainda não aplicam bônus.\n')
    valve=nav()+'# Valves · tiers e chance de sucesso\n\nColoque uma valve no slot dedicado da Lithography. Ela permanece no slot após o processo. As porcentagens abaixo são do **engraving**; a limpeza com água não usa RNG.\n\n| Valve | Sucesso | Falha |\n| --- | ---: | ---: |\n| Sem valve | 70% | 30% |\n'
    for tier in range(1,8):valve+=f'| {link("novadyne:valve_tier_"+str(tier))} | {(0.70+(tier-1)*0.25/6)*100:.2f}% | {(0.30-(tier-1)*0.25/6)*100:.2f}% |\n'
    valve+='\nChance por tentativa, não uma garantia em lotes pequenos. Os sete crafts são sem posição fixa.\n\n'+index(['valve_tier_'+str(i) for i in range(1,8)])
    write('valves.md',valve)
    write('progressao.md',nav()+'''# Progressão industrial

1. **Prepare energia externa.** As máquinas consomem FE e este mod ainda não tem gerador. Para testes em criativo, use o comando do [guia de testes](testar.md).
2. **Faça o [Macerator](itens/macerator.md).** Processe argila para obter Ceramic Powder.
3. **Faça a [Wafer Press](itens/wafer_press.md).** O craft consome um Macerator; construa outro para manter as duas máquinas. A prensa transforma Ceramic Powder em Base Wafer, cobre em Copper Layer e Pure Silicon em Silicon Wafer.
4. **Faça o [Processor](itens/processor.md).** O craft consome uma Wafer Press. Construa outra para manter a produção dos componentes. Junte Silicon Wafer, Copper Layer e Base Wafer nos três slots, nessa ordem, para produzir Stacked Electronic Circuit.
5. **Faça a [Lithography](itens/litografia.md).** O craft consome um Processor e um circuito; conserve materiais para reconstruir a linha. Grave o circuito: sai Dirty Silicon Wafer ou Failed Silicon Wafer.
6. **Finalize ou recicle.** Limpe o wafer sujo com um balde de água. Recicle o wafer com falha no Macerator: 50% Copper Layer, 50% Base Wafer.

Pure Silicon vem da fundição de quartzo. O wafer gravado é o final da cadeia implementada: ainda não tem aplicação posterior no mod.

## Fluxos de materiais

```mermaid
flowchart TD
    Q["Quartzo + calor"] --> S["Pure Silicon"]
    S --> W["Wafer Press: Silicon Wafer"]
    C["Cobre"] --> L["Wafer Press: Copper Layer"]
    A["Argila"] --> P["Macerator: Ceramic Powder"]
    P --> B["Wafer Press: Base Wafer"]
    W --> R["Processor: Stacked Electronic Circuit"]
    L --> R
    B --> R
    R --> E["Lithography: gravação"]
    E --> D["Dirty Silicon Wafer"]
    E --> F["Failed Silicon Wafer"]
    D --> T["Água + limpeza: Etched Silicon Wafer"]
    F --> X["Macerator: Copper Layer OU Base Wafer"]
```
''')
    write('testar.md',nav()+'''# Instalar e testar

## Baixar o mod

1. Abra [Actions → Build](https://github.com/nicotfpn/Novadyne-MOD/actions/workflows/build.yml).
2. Escolha uma execução da `main` com marca verde. Em **Artifacts**, baixe `novadyne-jar` (é preciso estar conectado ao GitHub).
3. Extraia o ZIP e coloque o `.jar` em `mods` de uma instalação **Minecraft 26.1.2 + NeoForge 26.1.2.76**, com Java 25.
4. Use um mundo novo em criativo e habilite comandos. Para isolar problemas, comece com NovaDyne apenas.

## Teste rápido do Macerator

```mcfunction
/give @s novadyne:macerator
/give @s minecraft:clay_ball 8
```

Coloque a máquina e anote as coordenadas. Substitua X, Y e Z pelos números do bloco:

```mcfunction
/data merge block X Y Z {energy:10000L}
```

Abra a GUI e coloque argila no input. Cada unidade leva 120 ticks (6 s a 20 TPS) e produz 1 Ceramic Powder. O comando é uma facilidade de teste; não adiciona um gerador ao survival.

## Teste da limpeza

```mcfunction
/give @s novadyne:litografia
/give @s novadyne:part_electronic_dirty_silicon_wafer
/give @s minecraft:water_bucket
```

Abasteça energia pelo mesmo comando. Coloque wafer no slot de entrada e água no slot do balde. Após 120 ticks, espere 1 Etched Silicon Wafer no output e 1 balde vazio no slot do balde.

## Diagnóstico

| Sintoma | O que conferir |
| --- | --- |
| Não processa | Energia suficiente, input correto e output livre |
| Engraving ou reciclagem parou | Retire todo o conteúdo do output; ambos os resultados precisam poder caber |
| Limpeza parou | Retire o balde vazio e coloque outro balde de água |
| Não dropou ao minerar | Use picareta de pedra ou superior |
| PNG existe mas `/give` falha | Capacitores/transistor ainda não são itens registrados |
| Build verde | Compilação e GameTests passaram; isso não certifica aparência, GUI ou desempenho em todo PC |

## Trabalhar em um computador fraco

Faça o build e os testes pelo GitHub Actions. O servidor de GameTests verifica alguns cenários de registro, energia e processamento sem renderizar o cliente no seu PC. O teste visual ainda exige abrir o Minecraft; com 4 GB de RAM, feche outros programas e tente uma instalação mínima com pouca distância de renderização. Não há garantia de desempenho nesse hardware.
''')
    write('manutencao.md',nav()+'''# Como manter esta wiki

A wiki é um conjunto de páginas Markdown neste repositório, acessível pelo GitHub sem publicar um site. O índice é `wiki/README.md`.

## Atualizar

```bash
python -m pip install -r tools/wiki/requirements.txt
python tools/wiki/generate.py
python tools/wiki/generate.py --check
```

Use Linux com as fontes DejaVu Sans (`fonts-dejavu-core`). O gerador lê as receitas JSON, os itens registrados, nomes, texturas e constantes das máquinas. Processos especiais em Java têm uma descrição revisada em `tools/wiki/processes.json`; ao mudar essas classes, revise esse catálogo e atualize seus hashes de origem.

O workflow **Wiki** confere fontes, páginas, imagens e links em cada mudança relevante. Se ele ficar vermelho após mudar uma receita, regenere a wiki e inclua os arquivos atualizados no commit. `--check` não altera arquivos e não acessa a rede.

Imagens de craft e processo são diagramas gerados a partir de dados. Ícones de blocos mostram uma face, sem simular uma captura 3D. Texturas vanilla e suas fontes estão em [créditos](assets/vanilla/SOURCES.md).
''')
    snapshot={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs()}
    (WIKI/'sources.json').write_text(json.dumps(snapshot,indent=2,ensure_ascii=False)+'\n')


def inputs():
    files=[ROOT/'tools/wiki/generate.py',ROOT/'tools/wiki/processes.json',ROOT/'tools/wiki/requirements.txt',JAVA/'ModItems.java',JAVA/'common/blockentity/AbstractMachineBlockEntity.java',ROOT/'gradle.properties']
    files+=list((DATA/'novadyne/recipe').glob('*.json'))+list((JAVA/'common/blockentity').glob('*BlockEntity.java'))
    files+=list((ASSETS/'lang').glob('*.json'))+list((ASSETS/'textures').rglob('*.png'))+list((WIKI/'assets/vanilla').glob('*'))
    return sorted(set(files))


def check():
    old=json.loads((WIKI/'sources.json').read_text())
    now={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs()}
    if old!=now:raise ValueError('Wiki desatualizada. Revise processes.json e execute python tools/wiki/generate.py')
    for key,sha in CATALOG['source_sha256'].items():
        actual=hashlib.sha256((JAVA/'common/blockentity'/(key+'.java')).read_bytes()).hexdigest()
        if actual!=sha:raise ValueError('Revisar processos descritos de '+key+' antes de atualizar a wiki')
    for p in WIKI.rglob('*.md'):
        body=p.read_text()
        targets=re.findall(r'\]\(([^)]+)\)|src="([^"]+)"',body)
        for pair in targets:
            target=next(v for v in pair if v)
            if target.startswith(('https:','http:','#')):continue
            target=target.split('#')[0]
            if not (p.parent/target).exists():raise ValueError(f'Link quebrado: {p}: {target}')
    for key in REGISTERED:
        assert (WIKI/'itens'/(key+'.md')).is_file(),key
    for key in RECIPES:
        assert (OUT/(key+'.png')).is_file(),key
    for p in PROCESSES:
        assert (OUT/(p['id']+'.png')).is_file(),p['id']
    for p in OUT.glob('*.png'):
        with Image.open(p) as im:im.verify()
    print(f'Wiki OK: {len(REGISTERED)} itens, {len(RECIPES)} crafts/fornos, {len(PROCESSES)} processos; links e PNGs válidos.')


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');args=ap.parse_args()
    if not args.check:build()
    check()
