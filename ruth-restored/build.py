from pathlib import Path
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape
import math,json,base64
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
P=Path('/workspace/figma-ruth');(P/'screens').mkdir(exist_ok=True)
source=ET.parse('/workspace/attachments/c0f425b3-7b23-48f9-937e-7de44533ad4d/1.svg').getroot()
images=[e for e in source.iter() if e.tag.endswith('image')]
photo=images[0].get('{http://www.w3.org/1999/xlink}href');sea=images[1].get('{http://www.w3.org/1999/xlink}href')
pdfmetrics.registerFont(TTFont('R','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'));pdfmetrics.registerFont(TTFont('B','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
W,H=440,956; BG='#102923';CARD='#19362F';SURFACE='#24453C';EDGE='#638371';INK='#F4F1E8';MUTED='#C4D5CA';MINT='#C0DEC5';AMBER='#E6AB70';DARK='#102923'
parts=[];names=[];textmeta=[];allmeta={}
def raw(s):parts.append(s)
def rect(x,y,w,h,fill=CARD,r=16,stroke=None,opacity=1):
 raw(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" fill-opacity="{opacity}"'+(f' stroke="{stroke}"' if stroke else '')+'/>')
def txt(x,y,s,size=16,col=INK,bold=False,anchor=None):
 a=f' text-anchor="{anchor}"' if anchor else ''
 raw(f'<text x="{x}" y="{y+size*.82}" font-family="DejaVu Sans" font-size="{size}" font-weight="{700 if bold else 400}" fill="{col}"{a}>{escape(s)}</text>')
 textmeta.append({'x':x,'y':y,'text':s,'size':size,'bold':bold,'anchor':anchor,'color':col})
def lines(x,y,ss,size=16,col=MUTED,step=25):
 for i,s in enumerate(ss):txt(x,y+i*step,s,size,col)
def line(x,y,x2,y2,col=EDGE,sw=1):raw(f'<path d="M{x} {y} L{x2} {y2}" stroke="{col}" stroke-width="{sw}" fill="none"/>')
def circle(cx,cy,r,col,stroke=None):raw(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}"'+(f' stroke="{stroke}"' if stroke else '')+'/>')
def button(x,y,w,s,primary=True,h=52,size=16):
 rect(x,y,w,h,MINT if primary else SURFACE,14,None if primary else EDGE)
 txt(x+w/2,y+(h-size)/2-1,s,size,DARK if primary else INK,True,'middle')
def card(y,h):rect(24,y,392,h)
def micro(cx,cy,col=DARK):
 raw(f'<rect x="{cx-4}" y="{cy-10}" width="8" height="15" rx="4" fill="none" stroke="{col}" stroke-width="2"/><path d="M{cx-8} {cy-2} v3 a8 8 0 0 0 16 0 v-3 M{cx} {cy+9} v5 M{cx-4} {cy+14} h8" fill="none" stroke="{col}" stroke-width="2" stroke-linecap="round"/>')
def voice():
 rect(24,876,392,60,BG,18,EDGE);rect(32,884,44,44,MINT,14);micro(54,906)
 txt(88,887,'Say or type an activity',16,INK);txt(88,912,'Review before saving',14,MUTED)
 rect(364,884,44,44,MINT,14);line(386,897,386,915,DARK,2);line(377,906,395,906,DARK,2)
 rect(174,944,92,4,MUTED,2)
def start(name,title,sub=None,back=True):
 global parts,textmeta
 parts=[];textmeta=[];names.append(name)
 rect(0,0,W,H,BG,0)
 raw(f'<image x="0" y="0" width="440" height="640" preserveAspectRatio="xMidYMid slice" href="{photo}"/>')
 raw(f'<image x="0" y="640" width="440" height="316" preserveAspectRatio="xMidYMid slice" href="{sea}"/>')
 rect(0,0,W,H,BG,0,opacity=.62)
 rect(16,14,408,116,BG,20,opacity=.92)
 txt(24,24,'9:41',14,INK,True);txt(336,24,'LTE  100%',12,MUTED)
 if back:
  rect(24,64,44,44,SURFACE,12);line(51,78,40,86,MUTED,2);line(40,86,51,94,MUTED,2)
  txt(80,65,title,25,INK,True)
 else:txt(24,64,title,32,INK,True)
 if sub:txt(24,109,sub,14,MUTED)
def finish(name):
 (P/'screens'/f'{len(names):02d}_{name}.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="440" height="956" viewBox="0 0 440 956">'+''.join(parts)+'</svg>')
 allmeta[name]=textmeta.copy()
def water(cx,cy,r,remaining,limit):
 frac=max(0,min(1,remaining/limit));uid='energywater'+str(len(parts));circle(cx,cy,r,SURFACE,EDGE)
 raw(f'<defs><clipPath id="{uid}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath></defs>')
 y=cy+r-2*r*frac;raw(f'<path d="M{cx-r} {y} C{cx-r/2} {y-r*.2} {cx+r/2} {y+r*.2} {cx+r} {y} L{cx+r} {cy+r} L{cx-r} {cy+r} Z" fill="{AMBER}" clip-path="url(#{uid})"/>')
 txt(cx,cy-29,str(remaining),50,DARK if frac>.48 else INK,True,'middle');txt(cx,cy+30,'units remaining',14,DARK if frac>.48 else INK,False,'middle')
def energy(y,used=20,limit=100,label='TODAY’S ENERGY'):
 card(y,228);txt(44,y+19,label,13,MINT,True)
 rem=max(0,limit-used);water(132,y+128,82,rem,limit)
 txt(250,y+67,'Used',14,MUTED);txt(250,y+89,f'{used} units',25,INK,True)
 txt(250,y+128,'Daily budget',14,MUTED);txt(250,y+150,f'{limit} units',25,INK,True)
 if used>limit:txt(230,y+193,f'Over by {used-limit} units',17,AMBER,True)
 else:txt(230,y+193,'Adjust budget →',16,MINT,True)
def timeline(y,selected=3,preview=False,used=20,limit=100):
 card(y,154 if preview else 110);txt(44,y+16,'YOUR TIMELINE',13,MINT,True);txt(324,y+16,'October',13,MUTED)
 line(62,y+44,378,y+44)
 for i in range(1,6):
  x=62+(i-1)*79;circle(x,y+44,6,MINT if i==selected else SURFACE,EDGE)
  if i==selected:rect(x-28,y+55,56,44,MINT,12);txt(x,y+69,str(i)+' Oct',14,DARK,True,'middle')
  else:rect(x-28,y+55,56,44,SURFACE,12,EDGE);txt(x,y+69,str(i)+' Oct',14,MUTED,False,'middle')
 if preview:txt(44,y+130,(f'Today: {used} / {limit} used · Severe symptoms' if selected==3 else '1 Oct: 130 / 100 used · Mild symptoms'),14,INK)
def home(used=20,limit=100,banner=None,past=False):
 start('home_temp','Hi, Ruth.','Saturday, 3 October · Your pace, your choice.',False)
 card(148,178);txt(44,168,'Today’s activities',18,INK,True);txt(310,171,'View all →',14,MINT,True)
 rows=[(211,'Cooking','Mixed effort · 30 min',5),(271,'Cleaning house','Mixed effort · 66 min',18)] if used>=25 else [(211,'Cleaning house','Mixed effort · 66 min',18),(271,'Email review','Cognitive · 48 min',2)]
 for y,title,meta,units in rows:
  txt(44,y,title,16,INK,True);txt(44,y+25,meta,14,MUTED);txt(360,y+7,str(units),22,INK,True,'middle');txt(360,y+34,'units',12,MUTED,False,'middle')
 energy(342,used,limit);button(24,588,188,'Log activity');button(228,588,188,'Log symptoms')
 timeline(656,preview=True,used=used,limit=limit);button(24,820,392,'View today’s plan →',False,44,16)
 voice()
 if banner:
  rect(24,816,392,48,SURFACE,14,EDGE);txt(40,833,banner,14,INK,True);txt(356,833,'Undo',14,MINT,True)
 names.pop()
# Original core page 1: list → energy circle → records → timeline → voice.
home();names.append('Home');finish('Home')
# Original core page 2: history with a useful timeline and an inline quick symptom record.
start('History','Activity & symptoms','Look back gently.');timeline(150,selected=3)
card(278,300);txt(44,295,'Date / activity',14,MUTED,True);txt(228,295,'Energy used',13,MUTED,True);txt(334,295,'Symptoms',13,MUTED)
for y,d,act,cost,sym in [(337,'1 Oct · 48h earlier','Cleaning house (3h)','130 / 100','Mild'),(416,'2 Oct · Yesterday','Rest & light reading','90 / 100','Moderate'),(495,'3 Oct · Today','Cleaning & email','20 / 100','Severe')]:
 txt(44,y,d,16,INK,True);txt(44,y+28,act,14,MUTED);txt(228,y+3,cost,14,INK,True);txt(334,y+3,sym,14,AMBER if sym=='Severe' else INK)
 if d.startswith('1'):txt(228,y+28,'Over by 30',13,AMBER)
 if y<495:line(44,y+62,396,y+62)
lines(24,592,['Symptoms may change 24–72 hours after activity.','Compare these days; this does not prove a cause.'],14,INK,22)
card(648,210);txt(44,666,'How are your symptoms now?',17,INK,True)
for x,y,a,sel in [(44,703,'None',False),(230,703,'Mild',False),(44,759,'Moderate',False),(230,759,'Severe',True)]:button(x,y,166,a,sel,44,15)
button(44,809,352,'Save symptoms',True,48,16);voice();finish('History')
# Original core page 3: budget adjustment remains a modal over Home.
home(25);names.append('Adjust_budget');rect(0,0,W,H,'#061510',0,opacity=.76);rect(24,174,392,650,CARD,24,EDGE)
txt(48,201,'Adjust daily budget',24,INK,True);rect(348,194,44,44,SURFACE,12);line(361,207,379,225,MUTED,2);line(379,207,361,225,MUTED,2)
lines(48,254,['Start with a temporary estimate.','Review your records and revise it over time.'],14,MUTED,23)
txt(48,323,'NEW ESTIMATE · UNITS',13,MINT,True);button(48,352,52,'−',False,56,26);txt(220,351,'80',46,INK,True,'middle');button(340,352,52,'+',False,56,26)
line(62,438,378,438)
for i,n in enumerate([70,80,90,100,110,120,130]):
 x=62+i*316/6;line(x,430,x,445,MINT if n==80 else EDGE,3 if n==80 else 1);txt(x,455,str(n),14,MINT if n==80 else MUTED,n==80,'middle')
rect(48,493,344,130,SURFACE,16);txt(64,510,'RECENT ACTIVITY & SYMPTOMS',12,MINT,True);txt(64,545,'1 Oct · 130 / 100 used · Mild',14,INK);txt(64,576,'2 Oct · 90 / 100 used · Moderate',14,INK);txt(64,603,'Review records →',14,MINT,True)
lines(48,646,['Current budget: 100 → New estimate: 80','25 already used · 55 would remain today','It is okay to lower your estimate.'],14,MUTED,24)
button(48,745,208,'Save · Apply today',True,52,15);button(268,745,124,'Cancel',False);finish('Adjust_budget')
# Original core page 4: activity name, three bars, cost inputs, save, voice.
start('Log_activity','Log activity','Your estimate, in personal energy units.')
card(154,134);txt(44,171,'Activity name',14,MUTED,True);rect(44,204,352,60,SURFACE,14,EDGE);txt(60,225,'Cooking',19,INK,True);txt(296,229,'30 min',15,MUTED)
card(308,440);txt(44,329,'Energy cost by type',18,INK,True);line(56,545,384,545)
for cx,cat,val,h,col in [(94,'Physical',4,135,MINT),(220,'Cognitive',1,34,'#ABC9D4'),(346,'Emotional',0,1,AMBER)]:
 if h>1:rect(cx-21,545-h,42,h,col,7)
 else:line(cx-21,545,cx+21,545,col,2)
 txt(cx,545-h-30,str(val)+' '+('unit' if val==1 else 'units'),14,INK,True,'middle');txt(cx,565,cat,15,MUTED,False,'middle')
 rect(cx-56,605,112,48,SURFACE,12,EDGE);txt(cx-34,619,'−',22,MINT,True,'middle');txt(cx,619,str(val),22,INK,True,'middle');txt(cx+34,619,'+',22,MINT,True,'middle')
txt(44,690,'Total cost: 5 units',24,INK,True)
lines(24,765,['Saving adds 5 to today’s 20 units used.','You can edit or undo the entry.'],14,INK,23)
button(24,812,248,'Save activity');button(284,812,132,'Cancel',False);voice();finish('Log_activity')
# Original core page 5: planned activities with explicit item-level controls.
start('Plan','Today’s plan','Plans can change with your energy.')
card(155,103);txt(44,174,'Prepare dinner',20,INK,True);txt(44,205,'18:00 · Physical · 30 min · Est. 12 units',14,MUTED);txt(44,234,'Selected activity',14,MINT,True)
for y,title,meta in [(274,'Chat with friends','16:00 · Emotional · 18 min · Est. 6 units'),(373,'Laundry','17:00 · Physical · 20 min · Est. 8 units'),(472,'Quiet rest','15:00 · Planned rest · No cost assigned')]:
 card(y,83);txt(44,y+16,title,18,INK,True);txt(44,y+48,meta,14,MUTED)
txt(24,585,'Adjust the selected activity',18,INK,True)
button(24,624,122,'Stop',False,52,16);button(159,624,122,'Defer',False,52,16);button(294,624,122,'Scale down',True,52,14)
rect(24,696,392,136,CARD,18);lines(44,716,['Stopping, moving or doing less is okay.','Planned estimates do not change energy used.','Only logged activity adds to your daily total.'],14,MUTED,30)
voice();finish('Plan')
# Original core page 6: expanded record + coloured bars + edit/delete.
start('Activities','Today’s activities','3 October · Recorded effort, not planned effort.')
card(155,493);txt(44,175,'Cleaning house',21,INK,True);txt(44,208,'66 min · Recorded at 10:00',14,MUTED);txt(375,177,'⌄',24,MINT,True)
for yy in [283,348,413,478]:line(56,yy,384,yy)
for cx,cat,val,h,col in [(94,'Physical',12,182,MINT),(220,'Cognitive',2,30,'#ABC9D4'),(346,'Emotional',4,61,AMBER)]:
 rect(cx-21,478-h,42,h,col,7);txt(cx,478-h-29,str(val)+' units',14,INK,True,'middle');txt(cx,502,cat,15,MUTED,False,'middle')
txt(44,546,'Total cost: 18 units',23,INK,True);button(44,585,168,'Edit',True,44);button(228,585,168,'Delete',False,44)
card(664,80);txt(44,680,'Email review · 48 min',18,INK,True);txt(44,712,'Cognitive · 2 units',14,MUTED);txt(372,684,'⌄',24,MINT,True)
txt(24,765,'Total recorded today: 20 units',17,INK,True);button(24,804,392,'Log another activity');voice();finish('Activities')
# Meaningful additional states: voice capture and review.
start('Voice_listening','Voice input','An optional way to record, without typing.')
card(180,415);txt(220,210,'Listening…',27,INK,True,'middle');circle(220,338,66,SURFACE,EDGE);raw('<g transform="translate(220 336) scale(2.2)">');micro(0,0,MINT);raw('</g>')
lines(52,442,['“I just did 30 minutes of cooking.”','Say what you did, in your own words.'],16,INK,33)
lines(24,634,['Recording starts only when you tap the mic.','You can check or edit the text before saving.'],14,INK,24)
button(24,754,392,'Stop recording & review');button(24,817,392,'Cancel recording',False);rect(24,884,392,44,SURFACE,14);txt(220,899,'0:08 · Recording · Tap Stop to finish',14,INK,False,'middle');rect(174,944,92,4,MUTED,2);finish('Voice_listening')
start('Voice_review','Review voice entry','Nothing is saved until you confirm.')
card(153,154);txt(44,172,'YOU SAID',13,MINT,True);lines(44,205,['“I just did 30 minutes','of cooking.”'],20,INK,30);txt(310,273,'Edit text →',14,MINT,True)
card(328,406);txt(44,348,'Activity',14,MUTED);txt(44,373,'Cooking · 30 min',22,INK,True);txt(44,421,'Choose your energy estimate',16,INK,True)
for y,cat,n in [(458,'Physical',4),(528,'Cognitive',1),(598,'Emotional',0)]:
 txt(44,y+13,cat,16,INK,True);rect(256,y,140,48,SURFACE,12,EDGE);txt(278,y+14,'−',21,MINT,True);txt(325,y+14,str(n),21,INK,True,'middle');txt(371,y+14,'+',21,MINT,True)
txt(44,684,'Total: 5 units',23,INK,True)
txt(24,760,'Only you choose the energy cost.',15,INK);button(24,806,248,'Save activity');button(284,806,132,'Cancel',False);rect(24,884,392,44,SURFACE,14);txt(220,899,'Review this entry before starting another',14,INK,False,'middle');rect(174,944,92,4,MUTED,2);finish('Voice_review')
# UR5 operations make the actual choices visible.
start('Scale_down','A smaller dinner plan','Choose a version that fits your energy.')
card(164,112);txt(44,183,'Original: Prepare dinner',19,INK,True);txt(44,221,'30 min · Estimated 12 units',16,MUTED)
card(300,229);txt(44,320,'Lighter version',16,MUTED);txt(44,353,'Assemble a simple meal',21,INK,True)
for x,w,s in [(44,176,'10 min · 4 units'),(232,164,'Set my own')]:button(x,407,w,s,x==44,56,14)
txt(44,486,'8 fewer planned units',15,MINT,True)
lines(24,575,['Your recorded energy used stays at 25.','Log actual effort after the activity.','There is no need to make up the difference.'],14,INK,29)
button(24,745,392,'Save smaller plan');button(24,808,392,'Cancel',False);voice();finish('Scale_down')
start('Defer','Move to another day','Laundry · 20 min · Estimated 8 units')
card(168,239);txt(44,189,'Choose a day',18,INK,True);button(44,231,168,'Tomorrow',True,52,16);button(228,231,168,'Choose date',False,52,15)
txt(44,312,'Sunday, 4 October',23,INK,True);txt(44,357,'11:00 · Change time →',16,MINT,True)
lines(24,459,['Laundry will leave today’s plan.','Your energy records stay unchanged.','You can adjust it again later.'],16,INK,29)
button(24,745,392,'Save · Move to tomorrow');button(24,808,392,'Cancel',False);voice();finish('Defer')
start('Stop','You can stop here.','Evening walk · Estimated 10 units')
card(178,234);txt(44,200,'Remove from today’s plan?',22,INK,True);lines(44,257,['No energy cost will be logged.','Existing records stay unchanged.','You can undo this change.'],16,MUTED,34)
lines(24,477,['Rest does not need to be earned.','There is no need to catch up later.'],16,INK,31)
button(24,745,392,'Stop this activity');button(24,808,392,'Keep in my plan',False);voice();finish('Stop')
# Save results reuse the existing page layouts rather than inventing new destinations.
home(25,banner='Activity saved · Cooking · 5 units');names.append('Activity_saved');finish('Activity_saved')
# Symptoms save state uses the history layout and same selection styling, with closure + Undo.
start('Symptoms_saved','Check-in saved','Severe · Today, 14:15')
card(162,134);txt(44,185,'Your symptoms are recorded.',20,INK,True);txt(44,224,'You do not need to explain a difficult day.',14,MUTED);txt(44,259,'Undo check-in →',15,MINT,True)
timeline(322,selected=3)
card(452,250);txt(44,474,'Activity and later symptoms',18,INK,True)
for yy,dd,u,sy in [(523,'1 Oct · 48h earlier','130 / 100','Mild'),(584,'2 Oct','90 / 100','Moderate'),(645,'3 Oct','25 / 100','Severe')]:
 txt(44,yy,dd,14,INK);txt(216,yy,u,14,INK,True);txt(334,yy,sy,14,MUTED)
lines(24,734,['Compare records to notice possible patterns.','They do not establish a cause.'],14,INK,24)
button(24,808,392,'Done · Back to today');voice();finish('Symptoms_saved')
home(25,80,banner='Budget saved · 100 → 80 units');names.append('Budget_saved');finish('Budget_saved')
start('Plan_updated','Your plan, adjusted.','Changes are a normal part of pacing.')
for y,a,b,detail in [(165,'Dinner · Scaled down','18:00 · Simple meal','30 → 10 min · Estimated 12 → 4 units'),(307,'Laundry · Deferred','Sun 4 Oct · 11:00','Removed from today’s plan'),(449,'Evening walk · Stopped','Removed from today’s plan','No energy cost was logged')]:
 card(y,125);txt(44,y+18,a,20,INK,True);txt(44,y+57,b,16,MUTED);txt(44,y+91,detail,14,MINT)
lines(24,617,['Energy used remains at 25 units.','Last change: dinner scaled down.'],15,INK,27)
button(24,733,392,'Undo last change',False);button(24,802,392,'Done · Back to plan');voice();finish('Plan_updated')
start('Earlier_day','1 October snapshot','An earlier record from your timeline.')
energy(170,130,100,'1 OCTOBER ENERGY');txt(24,425,'30 units over your recorded estimate.',18,INK,True)
card(478,129);txt(44,498,'Cleaning house · 3 hours',19,INK,True);txt(44,535,'Symptoms that day: Mild',16,MUTED);txt(44,568,'Compare with 3 Oct →',16,MINT,True)
timeline(635,selected=1);txt(24,776,'This is an earlier day, not today’s balance.',14,INK);voice();finish('Earlier_day')
(P/'screen_index.json').write_text(json.dumps(names,indent=2));(P/'text_metrics.json').write_text(json.dumps(allmeta,indent=2))
print('Created',len(names),'screens. Original sunset and ocean assets restored.')
