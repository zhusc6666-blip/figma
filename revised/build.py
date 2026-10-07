from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from xml.sax.saxutils import escape
from pathlib import Path
import json
P=Path('/workspace/figma-revised'); (P/'screens').mkdir(exist_ok=True)
pdfmetrics.registerFont(TTFont('UI','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('UIBold','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
W,H=390,844
bg='#F4F1E9';card='#FFFFFF';edge='#C6D1C7';white='#203B34';muted='#52665E';mint='#294E43';gold='#E8C99B'
c=canvas.Canvas(str(P/'Revised_Prototype_Preview.pdf'),pagesize=(W,H)); c.setTitle('Still — Energy at your pace | Static UI prototype')
sv=[]; names=[]
def rect(x,y,w,h,col,r=0,stroke=None):
 c.setFillColor(HexColor(col)); c.setStrokeColor(HexColor(stroke or col)); c.roundRect(x,H-y-h,w,h,r,fill=1,stroke=bool(stroke))
 sv.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{col}"'+(f' stroke="{stroke}"' if stroke else '')+'/>')
def text(x,y,s,size=14,col=white,bold=False):
 c.setFillColor(HexColor(col)); c.setFont('UIBold' if bold else 'UI',size); c.drawString(x,H-y-size*.82,s)
 sv.append(f'<text x="{x}" y="{y+size*.82}" font-family="DejaVu Sans" font-size="{size}" font-weight="{700 if bold else 400}" fill="{col}">{escape(s)}</text>')
def lines(x,y,ss,size=14,col=muted,step=22):
 for i,s in enumerate(ss):text(x,y+i*step,s,size,col)
def pill(x,y,w,s,selected=False):
 rect(x,y,w,48,mint if selected else card,14, None if selected else edge);text(x+14,y+17,s,13,bg if selected else white,selected)
def button(y,s,secondary=False):
 rect(24,y,342,54,card if secondary else mint,17,edge if secondary else None);text(42,y+18,s,15,white if secondary else bg,True)
def box(y,h):rect(24,y,342,h,card,20)
def start(name,title,kicker='YOUR DAILY COMPANION',sub=None,nav=False):
 global sv
 sv=[];names.append(name);rect(0,0,W,H,bg)
 text(24,18,'9:41',12,white,True);text(290,18,'LTE  100%',11,muted)
 text(24,65,'pace',24,mint,True);text(308,72,'03 OCT',10,muted)
 text(24,114,kicker,10,mint,True);text(24,139,title,28,white,True)
 if sub:text(24,180,sub,14,muted)
 if nav:
  rect(0,765,390,79,bg);rect(24,765,342,1,edge)
  for x,t in [(31,'Today'),(158,'Plan'),(273,'History')]:text(x,792,t,14,mint if t==nav else muted,t==nav)
  rect(146,831,98,4,muted,2)
def end(name):
 (P/'screens'/f'{len(names):02d}_{name}.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="440" height="956" viewBox="0 0 390 844">'+''.join(sv)+'</svg>')
 c.showPage()
def energy(y,used=35,limit=60):
 box(y,190);text(44,y+20,'TODAY’S ENERGY',11,mint,True);text(44,y+46,str(limit-used),56,white,True);text(134,y+74,'points remaining',16,white)
 rect(44,y+122,302,10,edge,5);rect(44,y+122,302*min(used/limit,1),10,mint,5)
 text(44,y+146,f'Used {used}  /  Daily limit {limit}',14,white);text(44,y+170,'Your estimate · Adjust limit →',11,muted)
def notice(y,a,b):
 rect(24,y,342,76,'#E4EBDF',16);text(42,y+16,a,14,mint,True);text(42,y+43,b,12,white)
def summary(y,used=20,limit=100):
 box(y,192);text(44,y+18,'TODAY’S ENERGY',11,mint,True);text(44,y+43,str(limit-used),52,white,True);text(135,y+71,'units remaining',15,white)
 rect(44,y+115,302,10,'#E4EBDF',5);rect(44,y+115,302*min(used/limit,1),10,mint,5)
 text(44,y+139,f'Used: {used} units · Budget: {limit}',14,white);text(44,y+167,'Adjust daily budget →',13,mint,True)
def row(y,title,sub,action=None):
 box(y,83);text(42,y+16,title,16,white,True);text(42,y+44,sub,12,muted)
 if action:text(42,y+63,action,11,mint,True)
start('home','At your own pace.',sub='Saturday, 3 October 2026',nav='Today');summary(218)
pill(24,429,165,'+ Log activity',True);pill(201,429,165,'+ Symptoms')
text(24,505,'Today’s activities',19,white,True);row(542,'Cleaning house','66 min · 18 units · Recorded');row(637,'Email review','48 min · 2 units · Recorded');text(24,735,'View all activities →',13,mint,True);end('home')
start('history','Activity & symptoms',sub='Compare today with the last two days.',nav='History')
box(222,285);text(42,242,'Date',11,muted,True);text(143,242,'Used / budget',11,muted,True);text(278,242,'Symptoms',11,muted,True)
for y,d,v,sy in [(282,'1 Oct','130 / 100','Mild'),(365,'2 Oct','90 / 100','Moderate'),(448,'3 Oct','20 / 100','Severe')]:
 text(42,y,d,14,white,True);text(143,y,v,14,white,True);text(278,y,sy,12);text(42,y+30,{'1 Oct':'Cleaning house · 3 hours · Over by 30 units','2 Oct':'Rest and light reading','3 Oct':'Latest symptom check-in · 14:15'}[d],11,muted)
notice(528,'Look back 24–72 hours','Today is 48 hours after the 1 Oct record.');lines(24,624,['Compare activity with later symptoms.','This may help you notice patterns;','it does not establish a cause.'],14)
text(24,717,'Review today’s plan →',14,mint,True);end('history')
start('budget','Adjust daily budget',sub='A flexible estimate, not a goal.')
lines(24,223,['Unsure of your limit? Start with a temporary','estimate and revise it from experience.'],12)
box(281,132);text(42,300,'RECENT RECORDS',11,mint,True);text(42,336,'1 Oct  ·  130 / 100 used  ·  Mild',13);text(42,367,'2 Oct  ·  90 / 100 used  ·  Moderate',13);text(42,392,'View activity & symptoms →',12,mint)
text(24,444,'New daily budget · units',15,white,True);box(476,89)
rect(40,493,48,48,'#E4EBDF',12);text(55,505,'−',24,mint);text(169,501,'80',32,white,True);rect(302,493,48,48,'#E4EBDF',12);text(316,505,'+',24,mint)
lines(24,590,['Current: 100 → New estimate: 80 units','25 used today · 55 would remain','It is okay to lower your estimate.'],13)
button(718,'Save budget · Apply today');text(150,798,'Cancel',14,muted);end('budget')
start('log_activity','Log activity',sub='Record your own energy estimate.')
text(24,222,'Activity name',14,white,True);box(247,54);text(42,265,'Cooking',17)
text(24,328,'Energy cost · units',15,white,True)
for y,name,n in [(362,'Physical',4),(433,'Cognitive',1),(504,'Emotional',0)]:
 box(y,59);text(42,y+22,name,15,white,True);rect(219,y+6,46,46,'#E4EBDF',10);text(233,y+16,'−',23,mint);text(280,y+22,str(n),16,white,True);rect(310,y+6,46,46,'#E4EBDF',10);text(324,y+16,'+',23,mint)
text(24,588,'Total cost: 5 units',23,white,True);lines(24,631,['Different kinds of effort can overlap.','Saving adds 5 units to today’s 20 used.'],12);button(718,'Save activity');text(150,798,'Cancel',14,muted);end('log_activity')
start('plan','Your plan can change.',sub='Planned effort is separate from energy used.',nav='Plan')
row(221,'Prepare dinner','18:00 · 30 min · Estimated 12 units');text(24,329,'Adjust this activity',16,white,True)
for y,a,b in [(363,'Scale down','Use a shorter or lighter version →'),(455,'Move to tomorrow','Choose a new time →'),(547,'Stop activity','Remove it from today’s plan →')]:
 box(y,76);text(42,y+15,a,18,white,True);text(42,y+46,b,12,mint)
lines(24,654,['Rest is a valid part of your plan.','There is no need to catch up.'],14);end('plan')
start('activity_details','Today’s activities',sub='3 October 2026',nav='Today')
box(221,269);text(42,242,'Cleaning house',20,white,True);text(42,275,'66 minutes · Recorded',13,muted)
for y,a,n in [(316,'Physical',12),(357,'Cognitive',2),(398,'Emotional',4)]:text(42,y,a,15);text(270,y,f'{n} units',15,white,True)
rect(42,432,306,1,edge);text(42,449,'Total cost: 18 units',18,white,True)
pill(24,510,165,'Edit entry');pill(201,510,165,'Delete entry')
row(580,'Email review','48 minutes · 2 units · Recorded');text(24,687,'Total recorded today: 20 units',15,white,True);text(24,720,'Rest can be recorded without a cost.',12,muted);end('activity_details')
start('symptoms','How are you feeling?',sub='Choose your overall symptoms now.')
for y,a,b,sel in [(225,'None','No symptoms noticed',False),(313,'Mild','Noticeable, but manageable',False),(401,'Moderate','Making daily activities harder',False),(489,'Severe','Making daily activities very difficult',True)]:
 rect(24,y,342,74,mint if sel else card,17);text(42,y+15,('●  ' if sel else '○  ')+a,17,bg if sel else white,True);text(42,y+45,b,12,bg if sel else muted)
lines(24,596,['No note is required.','Now · 14:15 · Change time →'],13);button(718,'Save symptoms');text(150,798,'Cancel',14,muted);end('symptoms')
start('scale_down','A smaller dinner plan',sub='Choose what suits your energy today.')
row(224,'Original: Cook dinner','30 min · Estimated 12 units');text(24,342,'Choose a lighter version',15,white,True)
rect(24,377,342,110,mint,20);text(42,396,'●  Assemble a simple meal',17,bg,True);text(42,433,'10 min · Estimated 4 units',14,bg);text(42,463,'8 fewer planned units',12,bg)
row(505,'○  Choose my own version','Set your own activity and estimate')
lines(24,620,['Only your plan changes.','Log actual effort after the activity.'],14);button(718,'Save smaller plan');text(150,798,'Cancel',14,muted);end('scale_down')
start('defer','Move to another day',sub='Laundry · Estimated 8 units')
text(24,231,'Choose a day',15,white,True);pill(24,265,164,'Tomorrow',True);pill(202,265,164,'Choose date');row(339,'Sunday, 4 October','11:00 · Change time →')
lines(24,464,['This moves out of today’s plan.','Your recorded energy used stays the same.','You can change this again later.'],13)
button(718,'Save · Move to tomorrow');text(150,798,'Cancel',14,muted);end('defer')
start('stop','You can stop here.',sub='Evening walk · Estimated 10 units')
box(235,149);text(42,255,'Remove from today’s plan?',20,white,True);lines(42,298,['No energy cost will be logged.','Your previous records stay unchanged.','You can undo this change.'],13)
lines(24,432,['Rest does not need to be earned.','There is no need to make this up later.'],13);button(650,'Stop activity');button(718,'Keep in my plan',True);end('stop')
start('saved_activity','Activity saved',sub='Cooking · 5 units · Today, 14:10');notice(221,'Today’s energy is updated','20 → 25 used · Budget stays at 100 units');summary(317,25,100);button(690,'Done · Back to today');button(756,'Undo activity',True);end('saved_activity')
start('saved_symptoms','Symptoms saved',sub='Your check-in is complete.');notice(222,'Severe · 3 October, 14:15','You do not need to explain a difficult day.');box(326,127);text(42,346,'Look back gently',18,white,True);lines(42,382,['History shows this alongside earlier','activity and symptom records.'],13);button(618,'View activity & symptoms');button(690,'Done · Back to today');button(756,'Undo check-in',True);end('saved_symptoms')
start('saved_budget','Budget updated',sub='Your estimate can change with your capacity.');notice(222,'Daily estimate changed · 100 → 80','Applies today and to future daily summaries.');summary(317,25,80);lines(24,550,['25 units used · 55 units remaining','Your activity records have not changed.'],14);button(690,'Done · Back to today');button(756,'Undo budget change',True);end('saved_budget')
start('saved_plan','Plan updated',sub='Changes are normal, including doing less.',nav='Plan');notice(221,'Dinner scaled down · 30 → 10 min','Estimated effort reduced from 12 to 4 units.');row(319,'18:00 · Simple meal','10 min · Estimated 4 units');row(416,'Laundry · Moved to tomorrow','Sun 4 Oct · 11:00');row(513,'Evening walk · Stopped','Removed from today’s plan');text(24,625,'Your recorded energy used stays at 25.',13,muted);button(666,'Undo last change',True);end('saved_plan')
c.save();(P/'screen_index.json').write_text(json.dumps(names,indent=2));print('Generated',len(names),'revised screens')
