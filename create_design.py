from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from xml.sax.saxutils import escape
from pathlib import Path
import json
P=Path('/workspace/figma-deliverables'); (P/'screens').mkdir(exist_ok=True)
pdfmetrics.registerFont(TTFont('UI','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('UIBold','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
W,H=390,844
bg='#102723';card='#1C3731';edge='#37554D';white='#F5F2E9';muted='#BCCFC6';mint='#C1DEC5';gold='#E8C99B'
c=canvas.Canvas(str(P/'Still_Prototype_Preview.pdf'),pagesize=(W,H)); c.setTitle('Still — Energy at your pace | Static UI prototype')
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
 text(24,65,'still',24,mint,True);text(308,72,'07 OCT',10,muted)
 text(24,114,kicker,10,mint,True);text(24,139,title,28,white,True)
 if sub:text(24,180,sub,14,muted)
 if nav:
  rect(0,765,390,79,bg);rect(24,765,342,1,edge)
  for x,t in [(31,'Today'),(158,'Plan'),(273,'History')]:text(x,792,t,14,mint if t==nav else muted,t==nav)
  rect(146,831,98,4,muted,2)
def end(name):
 (P/'screens'/f'{len(names):02d}_{name}.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="390" height="844" viewBox="0 0 390 844">'+''.join(sv)+'</svg>')
 c.showPage()
def energy(y,used=35,limit=60):
 box(y,190);text(44,y+20,'TODAY’S ENERGY',11,mint,True);text(44,y+46,str(limit-used),56,white,True);text(134,y+74,'points remaining',16,white)
 rect(44,y+122,302,10,edge,5);rect(44,y+122,302*min(used/limit,1),10,mint,5)
 text(44,y+146,f'Used {used}  /  Daily limit {limit}',14,white);text(44,y+170,'Your estimate · Adjust limit →',11,muted)
def notice(y,a,b):
 rect(24,y,342,76,'#28473D',16);text(42,y+16,a,14,mint,True);text(42,y+43,b,12,white)
start('today','Space for today.',sub='Wednesday, 7 October',nav='Today');energy(216)
pill(24,424,165,'+ Log activity',True);pill(201,424,165,'+ Symptoms')
text(24,501,'Next in your plan',19,white,True);box(537,102);text(44,555,'Prepare dinner',17,white,True);text(44,583,'18:00 · Physical · Estimated 12 pts',12,muted);text(44,611,'Adjust activity →',14,mint,True)
lines(24,661,['Rest is part of your plan.','You can do less whenever you need.'],14);end('today')
start('log_activity','Log an activity',sub='One short entry. Your own estimate.')
text(24,225,'Activity',14,white,True);box(252,56);text(42,270,'Work call',17)
text(24,333,'What kind of effort?',14,white,True);pill(24,363,106,'Physical');pill(138,363,119,'Cognitive',True);pill(265,363,101,'Emotional')
text(24,437,'Energy used · points',14,white,True);box(468,83);text(47,487,'−',28,mint);text(171,486,'10',32,white,True);text(318,487,'+',28,mint)
lines(24,577,['Points are personal estimates.','10 points uses 10 of your daily 60.','You can edit the entry later.'],14)
text(24,668,'Now · 14:10     Change time →',13,muted);button(718,'Save activity');text(151,798,'Cancel',14,muted);end('log_activity')
start('activity_saved','Activity saved',sub='Your energy summary is up to date.');notice(220,'Work call · Cognitive · 10 points','Saved today at 14:10');energy(319,45)
box(532,86);text(42,550,'35 → 45 points used',17,white,True);text(42,580,'Your daily limit stays at 60 points.',13,muted)
button(690,'Done · Back to today');button(756,'Undo activity',True);end('activity_saved')
start('symptoms','How are you feeling?',sub='Choose your overall symptoms now.')
for y,a,b,sel in [(231,'Mild','Noticeable, but manageable',False),(324,'Moderate','Making daily activities harder',True),(417,'Severe','Making daily activities very difficult',False)]:
 rect(24,y,342,78,mint if sel else card,18,edge if not sel else None);text(43,y+16,('●  ' if sel else '○  ')+a,17,bg if sel else white,True);text(43,y+46,b,12,bg if sel else muted)
text(24,523,'Optional note',14,white,True);box(550,81);text(42,570,'Brain fog after the call',14);text(42,602,'A few words are enough.',12,muted)
text(24,657,'Now · 14:15     Change time →',13,muted);button(718,'Save symptoms');text(151,798,'Cancel',14,muted);end('symptoms')
start('symptoms_saved','Check-in saved',sub='You do not need to explain a difficult day.');notice(228,'Moderate · Today, 14:15','Brain fog after the call');box(327,145);text(44,347,'Your latest check-in',17,white,True);lines(44,382,['Today’s symptoms are recorded.','History keeps activity and symptoms','together, including earlier days.'],14)
button(618,'View activity & symptoms');button(690,'Done · Back to today');button(756,'Undo check-in',True);end('symptoms_saved')
start('history','Look back gently.',sub='Activity and symptoms, side by side.',nav='History');pill(24,218,106,'This week',True);pill(142,218,116,'Last week')
box(290,238);text(42,308,'Date',12,muted,True);text(145,308,'Energy used',12,muted,True);text(267,308,'Symptoms',12,muted,True)
for y,d,n,s in [(349,'Mon 5','55 / 60','Mild'),(407,'Tue 6','30 / 60','Moderate'),(465,'Wed 7','45 / 60','Moderate')]:
 rect(42,y-12,306,1,edge);text(42,y,d,14);text(145,y,n,14,white,True);text(267,y,s,12)
rect(24,548,342,173,'#28473D',20);text(42,568,'A possible delayed pattern',16,mint,True);lines(42,605,['Symptoms can change 24–72 hours','after activity. Compare today with','Monday, two days earlier.'],13);text(42,684,'Compare these days →',14,mint,True);end('history')
start('comparison','Two days apart',sub='Monday 5 Oct → Wednesday 7 Oct')
box(229,157);text(43,247,'MONDAY · 5 OCT',11,mint,True);text(43,278,'55 / 60 points used',23,white,True);text(43,319,'Walk 20 · Work 25 · Stressful call 10',12,muted);text(43,349,'Symptoms: Mild',15)
box(402,130);text(43,420,'WEDNESDAY · 7 OCT',11,mint,True);text(43,450,'45 / 60 points used',23,white,True);text(43,492,'Symptoms: Moderate · 14:15',14)
lines(24,564,['Different symptoms, two days later.','This is a prompt to notice patterns,','not proof that one activity caused them.'],14)
text(24,656,'Self-management support, not diagnosis.',12,muted);button(718,'Back to history');end('comparison')
start('adjust_plan','Make room for rest.',sub='Prepare dinner · 18:00 · 12 points')
for y,a,b in [(230,'Scale down','Choose a shorter or lighter version →'),(337,'Defer','Choose another time or day →'),(444,'Stop','Remove this activity from today →')]:
 box(y,88);text(42,y+17,a,20,white,True);text(42,y+55,b,12,mint)
lines(24,573,['Your plan can change with your energy.','Stopping or doing less is a valid choice.','Planned points are estimates; only','logged activity changes energy used.'],14)
button(746,'Keep current plan',True);end('adjust_plan')
start('scale_down','A smaller version',sub='Change today’s dinner plan.')
box(230,104);text(42,248,'Original plan',12,muted);text(42,277,'Cook dinner · 30 min · 12 pts',17,white,True)
text(24,365,'Choose a lighter version',15,white,True);rect(24,397,342,112,mint,20);text(42,417,'●  Assemble a simple meal',17,bg,True);text(42,452,'10 minutes · Estimated 4 points',14,bg);text(42,482,'8 fewer planned points',12,bg)
box(526,69);text(42,550,'○  Choose my own version',15)
lines(24,626,['Energy used stays at 45 points.','Log actual effort after the activity.'],14);button(718,'Save smaller plan');text(151,798,'Cancel',14,muted);end('scale_down')
start('plan_updated','Your plan, adjusted.',sub='Wednesday, 7 October',nav='Plan');notice(220,'Dinner plan scaled down','30 → 10 min · Estimated 12 → 4 pts')
box(314,83);text(42,330,'18:00 · Assemble a simple meal',15,white,True);text(42,362,'Physical · Estimated 4 points',13,muted)
box(413,83);text(42,429,'Laundry · Deferred',15,white,True);text(42,461,'Moved to Thu 8 Oct, 11:00',13,muted)
box(512,83);text(42,528,'Evening walk · Stopped',15,white,True);text(42,560,'Removed from today’s plan',13,muted)
text(24,619,'There is no need to catch up.',15,mint);button(659,'Undo last change',True);text(24,733,'Each change offers its own undo.',11,muted);end('plan_updated')
start('energy_limit','Find your own limit.',sub='A flexible estimate, not a target.')
lines(24,222,['Not sure where to start? Use a temporary','estimate and revise it from experience.'],13)
box(285,140);text(42,303,'RECENT RECORDS',11,mint,True);text(42,339,'5 Oct    55 / 60 used    Mild',13);text(42,370,'6 Oct    30 / 60 used    Moderate',13);text(42,401,'Review activity & symptoms →',12,mint)
text(24,452,'Daily limit · points',14,white,True);box(483,82);text(47,501,'−',28,mint);text(169,500,'50',32,white,True);text(318,501,'+',28,mint)
lines(24,592,['Current estimate: 60 → New estimate: 50','45 already used · 5 would remain today','Change this as your circumstances change.'],12)
text(24,680,'Your limit can go down as well as up.',11,muted);button(718,'Save limit · Apply today');text(151,798,'Cancel',14,muted);end('energy_limit')
start('limit_saved','Limit updated',sub='You can revise it whenever you need.');notice(220,'Daily estimate changed · 60 → 50','Applies today and to future daily summaries');energy(319,45,50)
lines(24,550,['45 points used · 5 remaining','Your activity records have not changed.','A lower limit is an adjustment,','not a setback.'],14)
button(690,'Done · Back to today');button(756,'Undo limit change',True);end('limit_saved')
start('defer_activity','Another time is okay.',sub='Laundry · Estimated 8 points')
text(24,231,'Move this activity to',15,white,True);pill(24,265,164,'Tomorrow',True);pill(202,265,164,'Choose date')
box(338,109);text(42,357,'Thursday, 8 October',20,white,True);text(42,400,'11:00     Change time →',16,mint)
lines(24,484,['The activity leaves today’s plan.','No energy points are logged or used.','You can change this again later.'],14)
button(718,'Save · Move to tomorrow');text(151,798,'Cancel',14,muted);end('defer_activity')
start('stop_activity','You can stop here.',sub='Evening walk · Estimated 10 points')
box(235,164);text(42,255,'Remove from today’s plan?',20,white,True);lines(42,299,['This does not add energy used.','Your existing records stay unchanged.','You can undo this change.'],14)
lines(24,439,['Rest does not need to be earned.','There is no need to make this up later.'],14)
button(650,'Stop this activity');button(718,'Keep in my plan',True);end('stop_activity')
c.save();(P/'screen_index.json').write_text(json.dumps(names,indent=2))
print('Created',len(names),'SVG screens and PDF')
