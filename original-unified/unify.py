from pathlib import Path
from xml.etree import ElementTree as E
from copy import deepcopy
import json
P=Path('/workspace/figma-unified');N='http://www.w3.org/2000/svg';E.register_namespace('',N);E.register_namespace('xlink','http://www.w3.org/1999/xlink')
tree=E.parse(P/'indexed.svg');r=tree.getroot();ids={e.get('id'):e for e in r.iter()};parents={ch:pa for pa in r.iter() for ch in pa}
def remove(n):
 e=ids['edit_'+str(n)];parents[e].remove(e)
def replace(n,el):
 e=ids['edit_'+str(n)];pa=parents[e];i=list(pa).index(e);pa.remove(e);pa.insert(i,el)
def text(x,y,s,size=22,fill='black',bold=False,anchor=None):
 a={'x':str(x),'y':str(y),'fill':fill,'font-family':'Times New Roman, Liberation Serif, serif','font-size':str(size)}
 if bold:a['font-weight']='700'
 if anchor:a['text-anchor']=anchor
 e=E.Element('{'+N+'}text',a);e.text=s;return e
def tx(n,x,y,s,size=22,fill='black',bold=False):replace(n,text(x,y,s,size,fill,bold))
def rect(x,y,w,h,fill,stroke='#797979',rx=5):return E.Element('{'+N+'}rect',{'x':str(x),'y':str(y),'width':str(w),'height':str(h),'rx':str(rx),'fill':fill,'stroke':stroke,'stroke-width':'1'})
def put(e):r.append(e)
def multiline(n,x,y,ss,size=19,step=25,fill='#2A2A2A'):
 g=E.Element('{'+N+'}g')
 for i,s in enumerate(ss):g.append(text(x,y+i*step,s,size,fill))
 replace(n,g)
def button(x,y,w,h,label,size=20,fill='#E7E7E7'):
 put(rect(x,y,w,h,fill));put(text(x+w/2,y+h/2+size*.32,label,size,anchor='middle'))
# HOME: retain original scene, circle, typography, navigation and section positions.
tx(64,79,93,'Cleaning (66 min)',21);tx(65,270,93,'Physical',21)
tx(67,79,134,'Email review (48 min)',20);tx(66,270,134,'Cognitive',21);tx(76,79,176,'Resting (60 min)',21)
tx(68,220,512,'Used: 20 / 100 units',25,'white');ids['edit_68'] if False else None
# Restore centered alignment for the replaced summary.
for e in r.iter():
 if e.tag.endswith('text') and e.text=='Used: 20 / 100 units':e.set('text-anchor','middle')
for n in [29,30,31,32]:ids['edit_'+str(n)].set('height','48')
tx(39,255,805,'View recent days',23);tx(41,49,807,'Adjust budget',23)
button(132,830,176,40,'Log symptoms',21)
# HISTORY: keep two-day panel and symptom check-in in their original locations.
tx(103,521,179,'1 Oct · 48 hours ago',27,bold=True);tx(104,521,342,'2 Oct · Yesterday',27,bold=True)
tx(94,521,216,'Energy used: 130 / 100 units',21);tx(95,521,241,'30 units over your estimate',18,'#8E2828')
tx(98,521,274,'Key activity: Cleaning house (3h)',21);tx(99,521,306,'Symptoms: Mild',21)
tx(96,521,383,'Energy used: 90 / 100 units',21);tx(100,521,425,'Key activity: Rest & light reading',20);tx(101,521,457,'Symptoms: Moderate',21)
tx(89,563,510,'Today · 3 Oct',23);multiline(97,521,575,['Energy used today: 20 / 100 units','Planned activities remaining: 8'],22,31)
for n in [108,109,110,111]:
 e=ids['edit_'+str(n)];e.set('y','679');e.set('height','44')
# Larger consistent options; selected Severe still has a darker border and its text label.
tx(114,540,706,'None',18);tx(115,632,706,'Mild',18);tx(116,710,706,'Moderate',17);tx(117,810,706,'Severe',18)
multiline(112,523,821,['Compare activity with symptoms 24–72h later.','A pattern does not prove a cause.'],18,24)
tx(105,597,896,'Review today’s plan',23)
# BUDGET MODAL: retain original grey modal and scale, repair unclear selected value.
tx(202,1002,213,'Adjust daily energy budget',26);tx(213,1040,310,'Daily budget: 100 units',25)
# Keep original slider but give the current selected tick a clear outline.
ids['edit_200'].set('stroke','#333333');ids['edit_200'].set('stroke-width','2')
tx(203,1169,410,'100',24,bold=True)
# Original old outlined 80% was part of this text element; replacement removes that overlap.
multiline(216,1019,473,['Start with a temporary estimate; revise it.','Recent records to help you decide:','1 Oct: 130 / 100 used · Mild symptoms','2 Oct: 90 / 100 used · Moderate symptoms','It is okay to lower your budget.'],19,25)
for n in [217,218]:ids['edit_'+str(n)].set('height','44');ids['edit_'+str(n)].set('y','612')
ids['edit_217'].set('fill','#E7E7E7');ids['edit_218'].set('fill','#B9B9B9');tx(219,1072,641,'Save',22);tx(220,1229,641,'Cancel',22,'#292929')
# LOG: retain panel and the three original bars; show a real completed entry instead of empty placeholder.
tx(310,43,1235,'Cooking (12 min)',25,'#373737');tx(312,42,1322,'Estimated energy cost (units)',23)
for n in [324,325,326]:remove(n)
# Keep baseline and chart area, shorten the unused plot space locally without moving form fields.
ids['edit_328'].set('transform',f'translate(0 {1558*(1-132/7)}) scale(1 {132/7})')
ids['edit_329'].set('transform',f'translate(0 {1558*(1-33/7)}) scale(1 {33/7})')
ids['edit_330'].set('transform',f'translate(0 {1558*(1-1/7)}) scale(1 {1/7})')
put(text(105,1413,'4 units',18));put(text(203,1512,'1 unit',18));put(text(298,1544,'0 units',18))
# Larger original numeric controls in the same row.
for n in [298,299,300]:ids['edit_'+str(n)].set('y','1600');ids['edit_'+str(n)].set('height','44')
tx(313,121,1628,'4',22);tx(314,217,1628,'1',22);tx(315,313,1628,'0',22)
for n in [316,318,320]:e=ids['edit_'+str(n)];e.set('transform','translate(0 4)')
tx(323,134,1685,'Total cost: 5 units',24)
for n in [297,301]:ids['edit_'+str(n)].set('height','44')
tx(311,122,1744,'Save',22);tx(322,278,1744,'Cancel',22,'#292929')
# PLAN: retain list, selected blue rows and checkboxes; correct typo and make selected actions explicit.
for n,x,y in [(353,563,1320),(365,563,1464),(373,563,1608),(381,563,1751)]:tx(n,x,y,'Chat with friends (18 min)',23)
tx(351,564,1247,'Cooking (12 min)',24);tx(364,564,1391,'Working (72 min)',24);tx(372,564,1536,'Rest (90 min)',24);tx(380,564,1678,'Cooking (12 min)',24)
tx(352,790,1180,'Select',22)
remove(383)
ids['edit_366'].set('fill','#A29191')
ids['edit_368'].set('fill','#DADADA')
# Remove unlabeled red X only, retain its location as a clear text action.
for n in [384,385,386]:remove(n)
put(text(520,1183,'Select activities to adjust',20))
# Three equally clear actions at the original bottom action position.
for n in [354,355,356]:remove(n)
button(515,1816,111,48,'Stop',21);button(635,1816,111,48,'Shorten',21);button(755,1816,130,48,'Tomorrow',20)
put(text(522,1890,'Plans can change. There is no need to catch up.',18))
# ACTIVITY DETAILS: retain chart and expanded accordion; fix total, units and date.
tx(245,1043,1173,'3 Oct 2026',23,'white');tx(258,997,1232,'Cleaning house (66 min)',24)
tx(267,1071,1550,'Total cost: 18 units',24);tx(282,1256,1428,'4 units',18)
for n in [237,238]:ids['edit_'+str(n)].set('height','44')
tx(268,1087,1600,'Edit',22);tx(269,1240,1600,'Delete',22)
tx(261,1000,1659,'Email review (48 min)',24);tx(260,1000,1733,'Resting (60 min)',24);tx(263,997,1800,'Cooking (12 min)',24)
# Actual total is written next to the record summary without hiding the list.
tx(265,1064,1882,'Log another activity',25)

# SECOND PASS: unify the original layout, remove noise, and style components consistently.
BG='#EEE9E5';CARD='#FAF7F3';SUB='#E5DFDC';INK='#302C32';ACCENT='#655366';BORDER='#BEB2BA';SELECT='#D7E1E7'
current_parents={ch:pa for pa in r.iter() for ch in pa}
def existing(n):
 for e in r.iter():
  if e.get('id')=='edit_'+str(n):return e
 return None
def drop(n):
 e=existing(n)
 if e is not None:
  pa=next((p for p in r.iter() if e in list(p)),None)
  if pa is not None:pa.remove(e)
def attrs(n,**kw):
 e=existing(n)
 if e is not None:
  for k,v in kw.items():e.set(k.replace('_','-'),str(v))
def change_text(old,new=None,**kw):
 for e in r.iter():
  if e.tag.endswith('text') and e.text==old:
   if new is not None:e.text=new
   for k,v in kw.items():e.set(k.replace('_','-'),str(v))
def addtxt(x,y,s,size=20,fill=INK,bold=False):put(text(x,y,s,size,fill,bold))
def primary(x,y,w,h,label,size=22):
 put(rect(x,y,w,h,ACCENT,ACCENT,8));put(text(x+w/2,y+h/2+size*.32,label,size,'white',anchor='middle'))
def secondary(x,y,w,h,label,size=22):
 put(rect(x,y,w,h,CARD,BORDER,8));put(text(x+w/2,y+h/2+size*.32,label,size,INK,anchor='middle'))
# Recolor plain foreground shapes while keeping the original graphics and serif text.
for e in r.iter():
 if e.get('fill')=='black':e.set('fill',INK)
 if e.get('fill')=='#7F0002':e.set('fill','#856A7D')
 if e.get('fill')=='#003399':e.set('fill','#728A9C')
 if e.get('fill')=='#045700':e.set('fill','#A29575')
 if e.tag.endswith('text') and e.get('fill') not in ['white','#8E2828']:e.set('fill',INK)
# Remove all photographic layers and dark photo overlays; retain circle and existing cards.
for n in [4,5,10,11,83,85,124,125,130,131]:drop(n)
for n in [3,82,123]:attrs(n,fill=BG)
for n in [224,285,334]:attrs(n,fill=BG,fill_opacity=1)
attrs(1,fill='#D9D2D7')
# Remove the unlabelled side toolbar, voice fields and decorative date ruler.
for n in [12,13,14,15,16,17,18,70,71,132,133,134,135,136,137,138,192,193]:drop(n)
for n in [19,20,21,23,24,25,45,139,140,141,143,144,145,162,225,226,227,228,229,230,231,286,287,288,289,290,291,292,335,336,337,338,339,340,341]:drop(n)
for n in [308,309,254,255]:drop(n)
# Flat cards and restrained selection colors, with shared opacity, border and radius.
for n in [26,35,146,153,86,90,91,92,198,232,234,235,293,295,296,342]:attrs(n,fill=CARD,fill_opacity=1,rx=12)
for n in [36,37,38,154,155,156,233,236,239,240,343,346,357,366,367,374,375]:attrs(n,fill=SUB,fill_opacity=1,rx=8)
for n in [358]:attrs(n,fill=SELECT,fill_opacity=1,rx=8)
for n in [90,92,234,235,296]:attrs(n,fill='#E9E3E0',fill_opacity=1)
for n in [27,28,147,148]:drop(n)
# Extend the existing task-list card into the area freed by the old toolbar.
for n in [26]:attrs(n,x=24,width=392)
for n in [35,36,37,38]:attrs(n,x=32,width=376)
for old in ['Physical','Cognitive']:
 for e in list(r.iter()):
  if e.tag.endswith('text') and e.text==old and float(e.get('y','0'))<150:e.set('x','292')
drop(63);addtxt(292,62,'Type',23)
for n in [42,43,44]:drop(n)
secondary(258,191,142,36,'View all tasks',18)
# Keep the original orange water circle; use a quiet outline rather than a red border.
for n in [6,126]:attrs(n,fill=CARD,fill_opacity=1)
for n in [9,129]:attrs(n,stroke=BORDER)
for n in [8,128]:attrs(n,stroke='#B47D52')
# HOME: use one consistent pair of primary recording buttons in the original action area.
for n in [33,34,40]:drop(n)
for e in list(r):
 if e.tag.endswith('rect') and e.get('x')=='132' and e.get('y')=='830':r.remove(e)
 elif e.tag.endswith('text') and e.text=='Log symptoms':r.remove(e)
primary(24,545,186,56,'Log activity',24);primary(230,545,186,56,'Log symptoms',24)
change_text('Used: 20 / 100 units',fill=INK)
# Replace the ambiguous decorative timeline with one clean review card, retaining its location.
for k,b in list(B.items()) if False else []:pass
# The indexed original bounds identify only the decorative Home date-ruler elements.
for line in (P/'bounds.csv').read_text().splitlines():
 try:
  k,x,y,w,h=line.split(',');x,y,w,h=map(float,(x,y,w,h))
  if k.startswith('edit_') and 0<=x<440 and y>=674 and y+h<=751:drop(int(k[5:]))
 except ValueError:pass
attrs(22,x=24,y=673,width=392,height=171,fill=CARD,fill_opacity=1,rx=12)
for n in [29,30,31,32,39,41]:drop(n)
addtxt(40,706,'Today · 3 Oct 2026',24,bold=True);addtxt(40,743,'Review records or revise your estimate.',19)
secondary(40,770,172,48,'Adjust budget',22);secondary(228,770,172,48,'View recent days',21)
addtxt(24,640,'Rest is part of your plan.',22)
# HISTORY: shared page header, card fills, buttons and large clearly selected symptom chips.
attrs(84,fill=INK);attrs(88,fill=INK)
for n in [86]:attrs(n,stroke=BORDER)
for n in [93,106]:attrs(n,fill=ACCENT,stroke=ACCENT,rx=8)
change_text('Review today’s plan',fill='white');attrs(107,fill='white')
for n in [108,109,110]:attrs(n,fill=CARD,stroke=BORDER,rx=8)
attrs(111,fill=ACCENT,stroke=ACCENT,rx=8)
change_text('Severe',fill='white')
# BUDGET MODAL: same panel and slider, with clearly selected value and matching action styles.
attrs(198,x=984,width=392,stroke=BORDER,rx=12);replace(201,rect(984,162,392,77,'#E1D7DF','#E1D7DF',12));change_text('Adjust daily energy budget',x=1004,y=213,font_size=24,fill=INK);attrs(199,fill=SUB,rx=8);attrs(200,fill=ACCENT,stroke=ACCENT)
change_text('100',fill='white')
for n in [217,218,219,220]:drop(n)
primary(1008,610,164,48,'Save',23);secondary(1188,610,164,48,'Cancel',23)
attrs(204,x=1327,y=178,width=40,height=40,fill=CARD,rx=8);attrs(205,x=1327,y=178,width=40,height=40,stroke=BORDER,rx=8)
# LOG: keep the original input + three-column graph; align values, bars and controls to shared centers.
attrs(304,fill=INK);attrs(305,fill=INK);attrs(294,fill=CARD,rx=8)
for n in [295]:drop(n)
for n in [297,301,311,322]:drop(n)
primary(42,1715,148,48,'Save',23);secondary(249,1715,148,48,'Cancel',23)
# Keep plotted heights and move the outer columns slightly to give each +/- a 44-wide target.
attrs(328,transform=f'translate(-29 {1558*(1-132/7)}) scale(1 {132/7})')
attrs(330,transform=f'translate(30 {1558*(1-1/7)}) scale(1 {1/7})')
for n in [298,299,300,313,314,315,316,317,318,319,320,321,331,332,333]:drop(n)
for e in list(r):
 if e.tag.endswith('text') and e.text in ['4 units','1 unit','0 units'] and float(e.get('y','0'))>1300 and float(e.get('x','0'))<440:r.remove(e)
for cx,cat,val,top in [(94,'Physical',4,1426),(220,'Cognitive',1,1525),(346,'Emotional',0,1557)]:
 put(text(cx,top-12,f'{val} '+('unit' if val==1 else 'units'),18,INK,anchor='middle'))
 put(text(cx,1590,cat,19,INK,anchor='middle'))
 x=cx-56;put(rect(x,1602,112,44,CARD,BORDER,8))
 put(text(x+22,1632,'−',23,INK,anchor='middle'));put(text(cx,1632,str(val),23,INK,anchor='middle'));put(text(x+90,1632,'+',23,INK,anchor='middle'))
# PLAN: delete repeated placeholder rows; retain the original list and selection mechanism.
attrs(361,fill=INK)
for n in [367,370,371,374,376,377,375,378,379]:drop(n)
for old in ['Chat with friends (18 min)','Cooking (12 min)']:
 for e in list(r.iter()):
  if e.tag.endswith('text') and e.text==old and float(e.get('x','0'))>480 and float(e.get('x','0'))<920 and float(e.get('y','0'))>=1600:
   pa=next((p for p in r.iter() if e in list(p)),None)
   if pa is not None:pa.remove(e)
change_text('Chat with friends (18 min)',**{})
for e in r.iter():
 if e.tag.endswith('text') and e.text=='Chat with friends (18 min)' and e.get('y')=='1320':e.text='Read messages (10 min)'
attrs(344,fill=CARD,rx=8);attrs(345,stroke=BORDER,rx=8)
put(rect(516,1584,366,176,CARD,BORDER,8));addtxt(530,1614,'Selected: Chat with friends',23,bold=True)
addtxt(530,1645,'Original: 18 min · Emotional · 6 units',19)
addtxt(530,1677,'Shorten to: 9 min · 3 units',22)
addtxt(530,1710,'Defer to: Tomorrow, 4 Oct',22)
addtxt(530,1741,'Stop removes it from today’s plan.',19)
# Rebuild the existing three actions as one shared component style.
for e in list(r):
 if e.tag.endswith('rect') and e.get('y')=='1816':r.remove(e)
 elif e.tag.endswith('text') and e.text in ['Stop','Shorten','Tomorrow']:r.remove(e)
primary(516,1816,112,48,'Stop',22);primary(643,1816,112,48,'Shorten',22);primary(770,1816,112,48,'Defer',22)
# DETAILS: retain original accordion and chart; apply identical actions, labels and palette.
attrs(244,fill=INK);change_text('3 Oct 2026',fill=INK)
for n in [237,238,268,269]:drop(n)
primary(1019,1569,148,48,'Edit',23);secondary(1207,1569,148,48,'Delete',23)
attrs(241,fill=ACCENT,rx=8);change_text('Log another activity',fill='white')
# Shared back/close treatments. No sidebar or microphone bars are retained.
for n in [118,119,242,243,302,303,387,388]:attrs(n,fill=CARD,stroke=BORDER,rx=8)
# Remove covered old Home button labels so their ends cannot protrude beyond new button edges.
for e in list(r.iter()):
 if e.tag.endswith('text') and ((e.text=='View recent days' and e.get('x')=='255') or (e.text=='Adjust budget' and e.get('x')=='49')):
  pa=next((p for p in r.iter() if e in list(p)),None)
  if pa is not None:pa.remove(e)
attrs(241,fill_opacity=1)
attrs(294,stroke=BORDER)
# Match the dimmed Home context to the same column formatting and card style.
attrs(146,x=984,width=392);attrs(153,x=992,width=376)
for n in [154,155,156]:attrs(n,x=992,width=376)
tx(182,992,93,'Cleaning house (66 min)',21,INK)
tx(183,1252,93,'Physical',21,INK)
tx(185,992,134,'Email review (48 min)',21,INK)
tx(184,1252,134,'Cognitive',21,INK)
tx(181,1252,62,'Type',23,INK)
# Chart labels use the same serif family as all other text.
tx(280,1060,1328,'12 units',18,INK);tx(281,1157,1452,'2 units',18,INK)
tx(279,1241,1516,'Emotional',18,INK);tx(283,1145,1516,'Cognitive',18,INK);tx(284,1058,1516,'Physical',18,INK)

# Gridlines and frame outlines use the shared border color.
for n in [272,273,274,275,327]:attrs(n,stroke=BORDER,stroke_opacity=1)
for n in [80,223]:attrs(n,stroke=BG)
# The original dark modal overlay remains, with lower opacity for readable context.
attrs(197,fill='#302C32',fill_opacity='0.35')

# Save unified styling on the same six original page structures.
# Remove unused photo and gradient definitions after removing those decorative layers.
import re
refs=set()
for child in r:
 if not child.tag.endswith('defs'):
  for node in child.iter():
   for val in node.attrib.values():refs.update(re.findall(r'url\(#([^)]*)\)',val))
for child in r:
 if child.tag.endswith('defs'):
  for node in list(child):
   if node.get('id') not in refs:child.remove(node)
E.indent(tree,space=' ');tree.write(P/'Unified_Original_Layout.svg',encoding='utf-8',xml_declaration=True)
# Split by viewport, retaining exact positions and all original definitions.
(P/'screens').mkdir(exist_ok=True)
frames=[('01_Home',0,0),('02_History',480,0),('03_Adjust_budget',960,0),('04_Log_activity',0,1048),('05_Plan',480,1048),('06_Activities',960,1048)]
for name,x,y in frames:
 root=deepcopy(r);root.set('width','440');root.set('height','956');root.set('viewBox',f'{x} {y} 440 956');root.set('overflow','hidden')
 E.ElementTree(root).write(P/'screens'/f'{name}.svg',encoding='utf-8',xml_declaration=True)
print('Unified original six layouts; noise removed and component styles aligned.')
