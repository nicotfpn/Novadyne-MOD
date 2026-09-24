#!/usr/bin/env python3
"""Generate the GitHub wiki from recipe JSON, registrations and reviewed machine processes."""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
from functools import lru_cache
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
BG, PANEL, TEXT, MUTED, CYAN, GOLD = '#1b1e19', '#272b26', '#eeeadd', '#a9ad9c', '#bdcca8', '#d8b789'
MACHINES = {'macerator':'MaceratorBlockEntity', 'wafer_press':'WaferPressBlockEntity', 'processor':'ProcessorBlockEntity', 'litografia':'LitografiaBlockEntity'}
TEST_BLOCKS = {'test_power_hub'}
UTILITY_BLOCKS = {'water_sink', 'fluid_pipe', 'energy_cable', 'fuel_generator', 'basic_solar_generator', 'advanced_solar_generator'}
VANILLA = {'iron_ingot':'Barra de ferro','copper_ingot':'Barra de cobre','gold_ingot':'Barra de ouro','redstone':'Redstone','diamond':'Diamante','emerald':'Esmeralda','netherite_scrap':'Fragmento de netherita','netherite_ingot':'Barra de netherita','water_bucket':'Balde de água','bucket':'Balde vazio','quartz':'Quartzo','clay_ball':'Bola de argila','furnace':'Fornalha','piston':'Pistão','glass':'Vidro','redstone_block':'Bloco de redstone'}
LANG = json.loads((ASSETS/'lang/en_us.json').read_text())
REGISTERED = re.findall(r'registerSimple(?:Item|BlockItem)\("([^\"]+)"', (JAVA/'ModItems.java').read_text())
MATERIALS = [s for s in REGISTERED if s not in MACHINES and s not in TEST_BLOCKS and s not in UTILITY_BLOCKS and not s.startswith('valve_')]
CATALOG = json.loads((ROOT/'tools/wiki/processes.json').read_text())
PROCESSES = CATALOG['processes']
RECIPES = {p.stem:json.loads(p.read_text()) for p in sorted((DATA/'novadyne/recipe').glob('*.json'))}


def name(item):
    if item.startswith('#'): return 'Quartzo'
    ns, key = item.split(':')
    return VANILLA.get(key,key) if ns=='minecraft' else LANG.get('item.novadyne.'+key,LANG.get('block.novadyne.'+key,key))


def link(item, prefix=''):
    label = name(item)
    if item.startswith('novadyne:'):
        return f'[{label}]({prefix}itens/{item.split(":")[1]}.md)'
    return label


def font(size=20,bold=False): return ImageFont.truetype(BOLD if bold else FONT,size)


def cube(front, side, top):
    """Project the three visible texture faces into an isometric inventory icon."""
    result=Image.new('RGBA',(192,200))
    faces=[(top,[(96,8),(180,52),(96,96),(12,52)],1.0),
           (front,[(12,52),(96,96),(96,188),(12,144)],0.94),
           (side,[(96,96),(180,52),(180,144),(96,188)],0.70)]
    for texture,points,shade in faces:
        tex=texture.convert('RGBA');layer=Image.new('RGBA',result.size);draw=ImageDraw.Draw(layer)
        a,b,_,c=points
        def point(u,v):return (a[0]+(b[0]-a[0])*u+(c[0]-a[0])*v,a[1]+(b[1]-a[1])*u+(c[1]-a[1])*v)
        for y in range(tex.height):
            for x in range(tex.width):
                r,g,bv,alpha=tex.getpixel((x,y))
                if not alpha:continue
                corners=[point(x/tex.width,y/tex.height),point((x+1)/tex.width,y/tex.height),point((x+1)/tex.width,(y+1)/tex.height),point(x/tex.width,(y+1)/tex.height)]
                draw.polygon(corners,fill=(round(r*shade),round(g*shade),round(bv*shade),alpha))
        result=Image.alpha_composite(result,layer)
    return result


def pipe_icon():
    """Isometric view of the three visible axes of the six-way pipe junction."""
    texture=Image.open(ASSETS/'textures/block/fluid_pipe.png').convert('RGBA')
    dark=texture.getpixel((8,2));copper=texture.getpixel((8,5));water=texture.getpixel((8,8))
    im=Image.new('RGBA',(192,200));d=ImageDraw.Draw(im)
    center=(96,100)
    arms=((18,53),(174,53),(96,184))
    for end in arms:
        d.line((center,end),fill=dark,width=32)
        d.line((center,end),fill=copper,width=24)
        d.line((center,end),fill=water,width=9)
        # A darker collar and a bright water-facing end cap make each connection clear.
        d.ellipse((end[0]-16,end[1]-16,end[0]+16,end[1]+16),fill=dark)
        d.ellipse((end[0]-12,end[1]-12,end[0]+12,end[1]+12),fill=copper)
        d.ellipse((end[0]-5,end[1]-5,end[0]+5,end[1]+5),fill=water)
    d.polygon(((76,88),(96,77),(116,88),(116,111),(96,124),(76,111)),fill=dark)
    d.polygon(((82,89),(96,82),(110,89),(110,107),(96,116),(82,107)),fill=copper)
    d.polygon(((88,90),(96,86),(104,90),(104,101),(96,106),(88,101)),fill=water)
    d.line(((88,90),(96,86),(104,90)),fill='#d9f4ef',width=3)
    return im


@lru_cache(maxsize=None)
def icon(item):
    if item.startswith('#'):item='minecraft:quartz'
    ns,key=item.split(':')
    def load(path):return Image.open(path).convert('RGBA')
    if ns=='novadyne' and key in UTILITY_BLOCKS:
        if key=='water_sink':
            side=load(ASSETS/'textures/block/water_sink_side.png')
            return cube(side,side,load(ASSETS/'textures/block/water_sink_top.png'))
        if key=='fuel_generator':
            return cube(load(ASSETS/'textures/block/fuel_generator_front.png'),
                        load(ASSETS/'textures/block/fuel_generator_side.png'),
                        load(ASSETS/'textures/block/fuel_generator_top.png'))
        if key.endswith('solar_generator'):
            if key.startswith('advanced'):
                side=load(ASSETS/'textures/block/advanced_solar_side.png')
                return cube(side,side,load(ASSETS/'textures/block/advanced_solar_top.png'))
            panel=Image.new('RGBA',(16,16),'#1c2639');draw=ImageDraw.Draw(panel)
            for px in (2,6,10):
                for py in (2,7):draw.rectangle((px,py,px+3,py+4),fill='#376998')
            frame=load(ASSETS/'textures/block/machine_side.png')
            return cube(frame,frame,panel)
        # Show the actual pixel texture from the mod, not an outdated six-way junction drawing.
        return load(ASSETS/f'textures/block/{key}.png').resize((192,192),Image.Resampling.NEAREST)
    if ns=='novadyne' and (key in MACHINES or key in TEST_BLOCKS):
        textures=json.loads((ASSETS/'models/block'/(key+'.json')).read_text())['textures']
        def face(k):return load(ASSETS/'textures'/(textures[k].split(':')[1]+'.png'))
        if key in TEST_BLOCKS:
            return cube(face('side'),face('side'),load(WIKI/'assets/vanilla/redstone_block.png'))
        return cube(face('front'),face('side'),face('top'))
    if ns=='minecraft' and key in {'furnace','blast_furnace','piston','glass','redstone_block'}:
        def vanilla(k):return load(WIKI/'assets/vanilla'/(k+'.png'))
        if key=='furnace':return cube(vanilla('furnace'),vanilla('furnace_side'),vanilla('furnace_top'))
        if key=='blast_furnace':return cube(vanilla('blast_furnace_front'),vanilla('blast_furnace_side'),vanilla('blast_furnace_top'))
        if key=='piston':return cube(vanilla('piston_side'),vanilla('piston_side'),vanilla('piston'))
        return cube(vanilla(key),vanilla(key),vanilla(key))
    p=ASSETS/'textures/item'/(key+'.png') if ns=='novadyne' else WIKI/'assets/vanilla'/(key+'.png')
    if not p.exists():raise ValueError('Missing icon: '+item)
    return load(p)


def text(draw, xy, value, size=20, color=TEXT, bold=False):draw.text(xy,value,font=font(size,bold),fill=color)


def wrapped(draw, xy, value, width=22, size=18, color=TEXT):
    for i,line in enumerate(textwrap.wrap(value,width)):
        text(draw,(xy[0],xy[1]+i*(size+6)),line,size,color)


def centered(draw,cx,y,value,width=180,size=18,color=TEXT,bold=False):
    lines=[];line='';f=font(size,bold)
    for word in value.split():
        test=(line+' '+word).strip()
        if line and draw.textlength(test,font=f)>width:lines.append(line);line=word
        else:line=test
    if line:lines.append(line)
    for i,line in enumerate(lines):
        x=cx-draw.textlength(line,font=f)/2
        text(draw,(x,y+i*(size+5)),line,size,color,bold)


def slot(im,x,y,item=None,count=1,size=80):
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((x,y+2,x+size,y+size+2),radius=7,fill='#111410')
    d.rounded_rectangle((x,y,x+size,y+size),radius=7,fill='#272b26',outline='#444a40',width=1)
    if item:
        pic=icon(item);factor=(size-14)/max(pic.size)
        pic=pic.resize((round(pic.width*factor),round(pic.height*factor)),Image.Resampling.NEAREST)
        im.paste(pic,(x+(size-pic.width)//2,y+(size-pic.height)//2),pic)
        if count>1:
            d.rounded_rectangle((x+size-30,y+size-27,x+size-3,y+size-3),radius=3,fill=BG)
            text(d,(x+size-27,y+size-28),str(count),18,GOLD,True)


def arrow(d,x,y,w=110):
    d.line((x,y,x+w-3,y),fill=CYAN,width=3)
    d.line((x+w-13,y-9,x+w,y,x+w-13,y+9),fill=CYAN,width=3)


def canvas(title,sub,height=440):
    im=Image.new('RGB',(1200,height),BG);d=ImageDraw.Draw(im)
    text(d,(40,22),'NOVADYNE',14,CYAN,True)
    text(d,(1040,22),'GUIA DE JOGO',12,MUTED)
    text(d,(40,54),title,31,TEXT,True)
    text(d,(40,101),sub,17,MUTED)
    d.line((40,135,1160,135),fill='#373d33',width=1)
    return im,d


def render_recipe(key,r):
    typ=r['type'].split(':')[1]
    labels={'crafting_shaped':'Na bancada · siga a posição dos ingredientes','crafting_shapeless':'Na bancada · os ingredientes podem ficar em qualquer posição','smelting':'Na fornalha · adicione combustível','blasting':'No alto-forno · adicione combustível'}
    im,d=canvas(name(r['result']['id']),labels[typ],490)
    if typ.startswith('crafting'):
        cells=[r['key'].get(c) for row in r['pattern'] for c in row.ljust(3)] if typ=='crafting_shaped' else r['ingredients']
        cells=cells+[None]*(9-len(cells))
        for i,item in enumerate(cells):slot(im,199+(i%3)*86,161+(i//3)*86,item,size=78)
        arrow(d,526,286,160)
        slot(im,804,222,r['result']['id'],r['result'].get('count',1),128)
        centered(d,868,367,name(r['result']['id']),360,21,bold=True)
        count=r['result'].get('count',1)
        centered(d,868,405,f'{count} '+('unidade' if count==1 else 'unidades'),240,17,GOLD)
        centered(d,324,429,'Grade 3 × 3' if typ=='crafting_shaped' else 'Uma forma de organizar',290,15,MUTED)
    else:
        cx=[260,600,940]
        slot(im,cx[0]-50,208,r['ingredient'],size=100)
        centered(d,cx[0],333,name(r['ingredient']),250,18)
        arrow(d,385,258,88)
        slot(im,cx[1]-50,208,'minecraft:furnace' if typ=='smelting' else 'minecraft:blast_furnace',size=100)
        centered(d,cx[1],333,'Fornalha' if typ=='smelting' else 'Alto-forno',250,21,bold=True)
        centered(d,cx[1],371,f'{r["cookingtime"]/20:g} s · {r["experience"]} XP',200,16,GOLD)
        arrow(d,726,258,88)
        slot(im,cx[2]-50,208,r['result']['id'],size=100)
        centered(d,cx[2],333,name(r['result']['id']),250,18)
    im.save(OUT/(key+'.png'))


def stats(machine):
    src=(JAVA/'common/blockentity'/(MACHINES[machine]+'.java')).read_text()
    def get(k):return int(re.search(r'\b'+k+r'\s*=\s*([\d_]+)',src).group(1).replace('_',''))
    return {k:get(k) for k in ['MAX_ENERGY','ENERGY_PER_TICK','MAX_PROGRESS']}


def render_process(p):
    s=stats(p['machine']);machine=name('novadyne:'+p['machine'])
    im,d=canvas(p['title'],f'{s["MAX_PROGRESS"]/20:g} segundos · {s["ENERGY_PER_TICK"]} FE/t · {s["MAX_PROGRESS"]*s["ENERGY_PER_TICK"]:,} FE por operação'.replace(',','.'),475)
    centered(d,230,156,'Ingredientes',370,15,MUTED)
    centered(d,957,156,'Um dos dois resultados' if p.get('random') else 'Resultado',370,15,MUTED)
    for i,item in enumerate(p['inputs']):
        cx=230+(i-(len(p['inputs'])-1)/2)*130
        slot(im,int(cx-42),208,item,size=84)
        centered(d,cx,310,name(item),310 if len(p['inputs'])==1 else 119,16)
        if i<len(p['inputs'])-1:centered(d,cx+65,234,'+',25,21,MUTED)
    arrow(d,442,250,71)
    slot(im,540,190,'novadyne:'+p['machine'],size=120)
    centered(d,600,329,machine,210,22,CYAN,True)
    arrow(d,686,250,71)
    for i,item in enumerate(p['outputs']):
        cx=957+(i-(len(p['outputs'])-1)/2)*200
        slot(im,int(cx-42),208,item,size=84)
        centered(d,cx,310,name(item),180,16)
        if p.get('labels'):centered(d,cx,374,p['labels'][i],186,16,GOLD)
        if i<len(p['outputs'])-1:centered(d,cx+100,234,'ou' if p.get('random') else '+',42,19,MUTED)
    d.line((40,421,1160,421),fill='#373d33',width=1)
    text(d,(40,438),p['short_note'],16,MUTED)
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
    method={'smelting':' · fornalha','blasting':' · alto-forno'}.get(typ,'')
    s=f'### {name(r["result"]["id"])}{method}\n\n![Grade ou processo para {name(r["result"]["id"])}]({img})\n\n'
    s+=ingredients_table(ingredient_list(r),prefix)+f'\n**Resultado:** {r["result"].get("count",1)} × {link(r["result"]["id"],prefix)}.\n\n'
    if typ=='crafting_shapeless':s+='**Sem posição fixa:** basta colocar esses ingredientes na bancada, em qualquer ordem.\n\n'
    if typ in ['smelting','blasting']:s+='A tag `c:gems/quartz` contém quartzo vanilla neste mod e pode receber outros itens por datapacks. O combustível não está incluído no ingrediente.\n\n'
    if 'minecraft:water_bucket' in ingredient_list(r):s+='O balde vazio retorna após o craft.\n\n'
    s+=f'<details>\n<summary>Ver no código</summary>\n\n[Receita JSON]({prefix}../src/main/resources/data/novadyne/recipe/{key}.json)\n\n</details>\n\n'
    return s


def process_section(p,prefix=''):
    s=f'### {p["title"]}\n\n![{p["title"]}: entradas e saídas]({prefix}assets/generated/{p["id"]}.png)\n\n'
    s+=ingredients_table(p['inputs'],prefix)
    s+='\n**'+('Resultados possíveis' if p.get('random') else 'Resultado')+':** '+(' **ou** ' if p.get('random') else ' + ').join('1 × '+link(i,prefix) for i in p['outputs'])+'.\n\n'+p['note']+'\n\n'
    s+=f'<details>\n<summary>Ver no código</summary>\n\n[Lógica da máquina]({prefix}../src/main/java/com/novadyne/common/blockentity/{MACHINES[p["machine"]]}.java)\n\n</details>\n\n'
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
    intro=nav()+'![As quatro máquinas do NovaDyne](assets/generated/header.png)\n\n# NovaDyne\n\nUma linha industrial que transforma argila, quartzo e cobre em circuitos e wafers. Esta wiki reúne as receitas, os processos e o caminho para montar cada máquina no survival.\n\n'
    intro+='## A linha de produção\n\n| 01 · Macerator | 02 · Wafer Press | 03 · Processor | 04 · Lithography |\n| :---: | :---: | :---: | :---: |\n| [<img src="assets/generated/icon_macerator.png" width="88" alt="Macerator">](itens/macerator.md) | [<img src="assets/generated/icon_wafer_press.png" width="88" alt="Wafer Press">](itens/wafer_press.md) | [<img src="assets/generated/icon_processor.png" width="88" alt="Processor">](itens/processor.md) | [<img src="assets/generated/icon_litografia.png" width="88" alt="Lithography">](itens/litografia.md) |\n| Moe argila e recicla wafers com falha | Prensa silício, cobre e cerâmica | Monta o circuito eletrônico | Grava e limpa o wafer |\n\n**Primeira vez por aqui?** Siga a [progressão industrial](progressao.md) para montar a linha. Para consultar um craft específico, abra [todas as receitas](receitas.md).\n\n'
    intro+='## Energia para a fábrica\n\nComece com o [Fuel Generator](itens/fuel_generator.md): coloque combustível no slot e ligue uma máquina diretamente ou com [Energy Cables](itens/energy_cable.md). Depois, faça o [Basic Solar Generator](itens/basic_solar_generator.md) e avance para o [Advanced Solar Generator](itens/advanced_solar_generator.md), que funciona à noite com 25% da geração diurna.\n\n'
    intro+='## Explore\n\n| Guia | Conteúdo |\n| --- | --- |\n| [Receitas](receitas.md) | Crafts, fundição e processos ilustrados |\n| [Máquinas](maquinas.md) | Slots, energia e tempo de operação |\n| [Materiais](materiais.md) | Obtenção e usos de cada componente |\n| [Valves](valves.md) | Tiers e chances da Lithography |\n| [Instalação e testes](testar.md) | Download do JAR e primeiros passos no jogo |\n\n'
    intro+='> **Para recuperar os blocos:** use uma picareta.\n\n---\n\n[Repositório](../README.md) · [Créditos das texturas vanilla](assets/vanilla/SOURCES.md) · [Contribuir com a wiki](manutencao.md)\n'
    write('README.md',intro)
    write('receitas.md',nav()+'# Receitas e processos\n\nAs imagens mostram a disposição dos ingredientes e o resultado de cada operação. Na bancada, siga a grade quando houver posição fixa; nas máquinas, confira as entradas e deixe espaço na saída.\n\n## Bancada e fornos\n\n'+''.join(recipe_section(k,r) for k,r in RECIPES.items())+'## Nas máquinas\n\n'+''.join(process_section(p) for p in PROCESSES))
    for key in REGISTERED:
        item='novadyne:'+key
        s=nav('../')+f'# {name(item)}\n\n![{name(item)}](../assets/generated/icon_{key}.png)\n\n`{item}`\n\n'
        if key in MACHINES:
            st=stats(key);s+='## Operação\n\n| Propriedade | Valor |\n| --- | --- |\n'+f'| Capacidade | {st["MAX_ENERGY"]:,} FE |\n| Consumo | {st["ENERGY_PER_TICK"]} FE/t |\n| Duração | {st["MAX_PROGRESS"]} ticks / {st["MAX_PROGRESS"]/20:g} s |\n| Energia por ciclo | {st["ENERGY_PER_TICK"]*st["MAX_PROGRESS"]:,} FE |\n'.replace(',','.')+'\nTempos consideram 20 ticks por segundo. Recebe energia, mas não fornece energia a outros blocos. Se faltar energia durante o trabalho, o progresso volta a zero.\n\n'+CATALOG['machines'][key]+'\n\n'
        elif key in TEST_BLOCKS:
            s+='**Bloco de teste em criativo.** Fornece até 1.000 FE por tick para cada máquina NovaDyne dentro de um quadrado 5 × 5, no mesmo nível do bloco. É uma fonte infinita para testar as GUIs e os processos; não possui receita de craft.\n\n'
        elif key in UTILITY_BLOCKS:
            info={
                'water_sink':'**Fonte infinita de água.** Fornece água aos blocos vizinhos e por uma rede de até 128 cabos de fluido em chunks carregados. Não consome energia.',
                'fluid_pipe':'**Tubo de água.** Water Sink → Fluid Pipe → Lithography. O núcleo aparece isolado; os braços aparecem apenas ao lado de outros pipes ou de blocos com capability de fluido na face adjacente. Suporta curvas e até 128 pipes por sink.',
                'energy_cable':'**Cabo de energia.** Fuel Generator ou gerador solar → Energy Cable → Macerator ou outra máquina com capability de energia. Os braços apontam apenas para outros cabos e blocos com capability de energia. Cada gerador percorre até 128 cabos carregados e transfere até sua taxa de geração por tick, com transações.',
                'fuel_generator':'**Gerador a combustível.** Aceita madeira, carvão, balde de lava e outros combustíveis válidos da fornalha. Gera 80 FE/t enquanto queima; pausa ao encher o buffer de 40.000 FE. Recipientes vazios vão para o slot de saída.',
                'basic_solar_generator':'**Gerador solar básico.** Céu aberto: 40 FE/t durante o dia e 0 FE/t à noite. Buffer de 40.000 FE.',
                'advanced_solar_generator':'**Gerador solar avançado.** Céu aberto: 100 FE/t durante o dia e 25 FE/t à noite. Buffer de 40.000 FE.'
            }
            s+=info[key]+'\n\n'
        elif key.startswith('valve_'):
            tier=int(key[-1]);s+=f'**Upgrade da Lithography.** Tier {tier}: {(0.70+(tier-1)*0.25/6)*100:.2f}% de sucesso e {(0.30-(tier-1)*0.25/6)*100:.2f}% de falha na gravação. A valve não é consumida.\n\n'.replace('.00%','%')
        else:s+=CATALOG['materials'][key]+'\n\n'
        sources=[(k,r) for k,r in RECIPES.items() if r['result']['id']==item]
        processes=[p for p in PROCESSES if item in p['outputs']]
        s+='## Como obter\n\n'
        s+=''.join(recipe_section(k,r,'../') for k,r in sources)
        s+=''.join(process_section(p,'../') for p in processes)
        if not sources and not processes:s+='Disponível no inventário criativo ou com `/give @s novadyne:test_power_hub`.\n\n' if key in TEST_BLOCKS else 'Sem receita de obtenção implementada.\n\n'
        s+='## Onde usar\n\n'
        uses=[f'- Craft de {link(r["result"]["id"],"../")}.' for r in RECIPES.values() if item in ingredient_list(r)]
        uses += [f'- {p["title"]}, em {link("novadyne:"+p["machine"],"../")}.' for p in PROCESSES if item in p['inputs']]
        if key.startswith('valve_'):uses+=['- Slot de valve da [Lithography](litografia.md); melhora a chance de sucesso.']
        s+='\n'.join(uses) if uses else ('Coloque-o no centro das máquinas que deseja alimentar.' if key in TEST_BLOCKS else 'Por enquanto, não entra em nenhuma outra receita.')
        if key in MACHINES:s+='\n\n## O que dá para fazer\n\n'+''.join(process_section(p,'../') for p in PROCESSES if p['machine']==key)
        s+=f'\n\n<details>\n<summary>Pegar este item em criativo</summary>\n\n```mcfunction\n/give @s {item}\n```\n\n</details>\n'
        write('itens/'+key+'.md',s)
    def index(keys):
        return '| | Item |\n| --- | --- |\n'+''.join(f'| <img src="assets/generated/icon_{k}.png" width="48" alt="{name("novadyne:"+k)}"> | {link("novadyne:"+k)} |\n' for k in keys)
    write('materiais.md',nav()+'# Materiais\n\nClique no nome para ver obtenção, craft e usos.\n\n'+index(MATERIALS))
    write('maquinas.md',nav()+'# Máquinas\n\nDo primeiro material ao wafer gravado, cada máquina prepara a próxima etapa. Abra uma página para ver o craft, os slots e os processos disponíveis.\n\n'+index(MACHINES)+'\n## Energia para testar\n\n'+index(TEST_BLOCKS)+'\nO [Test Power Hub](itens/test_power_hub.md) alimenta as máquinas em um quadrado 5 × 5 no mesmo nível. Está disponível no criativo e facilita os [testes no jogo](testar.md).\n\n## Regras comuns\n\n- Todas recebem energia FE externa. Para testar em criativo, use o Test Power Hub.\n- Use picareta de pedra ou superior para recuperar os blocos. Os itens do inventário caem ao quebrá-los.\n- O processamento aguarda quando a saída está cheia ou contém outro item.\n- As valves alteram a chance de sucesso na Lithography. Nas demais máquinas, o slot de valve não oferece bônus.\n')
    valve=nav()+'# Valves · tiers e chance de sucesso\n\nColoque uma valve no slot dedicado da Lithography. Ela permanece no slot após o processo. As porcentagens abaixo são do **engraving**; a limpeza com água não usa RNG.\n\n| Valve | Sucesso | Falha |\n| --- | ---: | ---: |\n| Sem valve | 70% | 30% |\n'
    for tier in range(1,8):valve+=f'| {link("novadyne:valve_tier_"+str(tier))} | {(0.70+(tier-1)*0.25/6)*100:.2f}% | {(0.30-(tier-1)*0.25/6)*100:.2f}% |\n'
    valve+='\nChance por tentativa, não uma garantia em lotes pequenos. Os sete crafts são sem posição fixa.\n\n'+index(['valve_tier_'+str(i) for i in range(1,8)])
    write('valves.md',valve)
    write('progressao.md',nav()+'''# Progressão industrial

1. **Prepare energia.** Construa o [Fuel Generator](itens/fuel_generator.md) para usar combustível de fornalha ou faça um [gerador solar](itens/basic_solar_generator.md). Coloque o gerador encostado na máquina. Para testes em criativo, use o comando do [guia de testes](testar.md).
2. **Faça o [Macerator](itens/macerator.md).** Processe argila para obter Ceramic Powder.
3. **Faça a [Wafer Press](itens/wafer_press.md).** O craft consome um Macerator; construa outro para manter as duas máquinas. A prensa transforma Ceramic Powder em Base Wafer, cobre em Copper Layer e Pure Silicon em Silicon Wafer.
4. **Faça o [Processor](itens/processor.md).** O craft consome uma Wafer Press. Construa outra para manter a produção dos componentes. Junte Silicon Wafer, Copper Layer e Base Wafer nos três slots, nessa ordem, para produzir Stacked Electronic Circuit.
5. **Faça a [Lithography](itens/litografia.md).** O craft consome um Processor e um circuito; conserve materiais para reconstruir a linha. Grave o circuito: sai Dirty Silicon Wafer ou Failed Silicon Wafer.
6. **Finalize ou recicle.** Limpe o wafer sujo com um balde de água ou com água do Water Sink transportada por cabos de fluido. Recicle o wafer com falha no Macerator: 50% Copper Layer, 50% Base Wafer.

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
/give @s novadyne:test_power_hub
/give @s novadyne:macerator
/give @s minecraft:clay_ball 8
```

Coloque o Test Power Hub e o Macerator no mesmo nível, até dois blocos de distância nos eixos norte/sul e leste/oeste. O bloco fornece energia a cada máquina NovaDyne no quadrado 5 × 5 centrado nele. Abra a GUI do Macerator e coloque argila no input. Cada unidade leva 120 ticks (6 s a 20 TPS) e produz 1 Ceramic Powder.

## Teste da limpeza

```mcfunction
/give @s novadyne:litografia
/give @s novadyne:part_electronic_dirty_silicon_wafer
/give @s minecraft:water_bucket
```

Coloque a Lithography no mesmo quadrado 5 × 5 do Test Power Hub. Insira o wafer no slot de entrada e a água no slot do balde. Após 120 ticks, espere 1 Etched Silicon Wafer no output e 1 balde vazio no slot do balde.

## Teste dos geradores

```mcfunction
/give @s novadyne:fuel_generator
/give @s novadyne:energy_cable 8
/give @s minecraft:oak_planks 16
/give @s novadyne:basic_solar_generator
/give @s novadyne:advanced_solar_generator
```

Ligue o Fuel Generator à máquina com até 128 Energy Cables, abra a GUI e coloque tábuas no slot de combustível. Ele gera 80 FE/t e transfere até 80 FE/t para a rede. O slot da direita guarda recipientes vazios (por exemplo, um balde após queimar lava); se estiver ocupado, a máquina aguarda antes de consumir o combustível. Quando o armazenamento de energia enche, a queima pausa.

Coloque os solares sob céu aberto: o básico gera 40 FE/t de dia e 0 à noite; o avançado, 100 FE/t de dia e 25 FE/t à noite. Clique com o botão direito para ver a energia guardada. Conecte a máquina diretamente ou por Energy Cables.

## Teste da água encanada

```mcfunction
/give @s novadyne:water_sink
/give @s novadyne:fluid_pipe 8
/give @s novadyne:part_electronic_dirty_silicon_wafer
```

Coloque o Water Sink, uma linha contínua de cabos de fluido e a Lithography nas extremidades. O cabo encosta no sink e na máquina; curvas e subidas também funcionam. O tanque da Lithography recebe água em até 16 ticks (4.000 mB) e mostra seu volume na GUI. Com energia FE e saída livre, cada wafer consome 1.000 mB. O balde continua sendo uma alternativa; se houver água suficiente no tanque, ele não é consumido.

## Diagnóstico

| Sintoma | O que conferir |
| --- | --- |
| Não processa | Energia suficiente, input correto e output livre |
| Engraving ou reciclagem parou | Retire todo o conteúdo do output; ambos os resultados precisam poder caber |
| Limpeza parou | Confira o balde de água ou o tanque (mínimo de 1.000 mB); confirme cabos conectados e saída livre |
| Não dropou ao minerar | Use picareta de pedra ou superior |
| JAR não aparece em Artifacts | Confirme que a execução do workflow terminou com marca verde e que a conta está conectada ao GitHub |
| Build verde, mas há erro visual | Os testes automatizados verificam o código e alguns processos; registre o erro visto no cliente |

## Sobre os testes automatizados

O [workflow de build](https://github.com/nicotfpn/Novadyne-MOD/actions/workflows/build.yml) compila o mod e executa testes de registro, energia e processamento em um servidor Minecraft. Aparência, interface e interação com outros mods precisam de verificação dentro do jogo.
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

Imagens de craft e processo são diagramas gerados a partir de dados. Blocos e máquinas são desenhados em perspectiva a partir das texturas de suas faces; não são capturas do cliente Minecraft. Texturas vanilla e suas fontes estão em [créditos](assets/vanilla/SOURCES.md).
''')
    snapshot={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs()}
    (WIKI/'sources.json').write_text(json.dumps(snapshot,indent=2,ensure_ascii=False)+'\n')


def inputs():
    files=[ROOT/'tools/wiki/generate.py',ROOT/'tools/wiki/processes.json',ROOT/'tools/wiki/requirements.txt',JAVA/'ModItems.java',JAVA/'common/blockentity/AbstractMachineBlockEntity.java',ROOT/'gradle.properties']
    files+=list((DATA/'novadyne/recipe').glob('*.json'))+list((JAVA/'common/blockentity').glob('*BlockEntity.java'))
    files+=list((ASSETS/'models/block').glob('*.json'))
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
