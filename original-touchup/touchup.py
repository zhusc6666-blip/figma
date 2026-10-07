from pathlib import Path
from xml.etree import ElementTree as E
from copy import deepcopy
import json
P=Path('/workspace/figma-touchup');N='http://www.w3.org/2000/svg';E.register_namespace('',N);E.register_namespace('xlink','http://www.w3.org/1999/xlink')
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
# Save original-sized combined canvas, retaining unchanged original background images and graphic elements.
E.indent(tree,space=' ');tree.write(P/'Original_Layout_Touched_Up.svg',encoding='utf-8',xml_declaration=True)
# Split by viewport, retaining exact positions and all original definitions.
(P/'screens').mkdir(exist_ok=True)
frames=[('01_Home',0,0),('02_History',480,0),('03_Adjust_budget',960,0),('04_Log_activity',0,1048),('05_Plan',480,1048),('06_Activities',960,1048)]
for name,x,y in frames:
 root=deepcopy(r);root.set('width','440');root.set('height','956');root.set('viewBox',f'{x} {y} 440 956');root.set('overflow','hidden')
 E.ElementTree(root).write(P/'screens'/f'{name}.svg',encoding='utf-8',xml_declaration=True)
print('Original six layouts preserved; local edits applied.')
