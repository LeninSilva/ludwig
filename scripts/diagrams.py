"""Generates assets/diagrams/<lesson-id>.svg. Run: python3 scripts/diagrams.py
Each diagram uses CSS classes styled by styles.css so it follows light/dark themes."""
import os, html
OUT = os.path.join(os.path.dirname(__file__), '..', 'assets', 'diagrams')
os.makedirs(OUT, exist_ok=True)

class D:
    def __init__(s, id, h=200, w=360):
        s.id, s.w, s.h, s.el = id, w, h, []
    def add(s, x): s.el.append(x); return s
    def t(s, x, y, txt, c='t', a='middle'):
        lines = txt.split('\n')
        for i, ln in enumerate(lines):
            s.add(f'<text x="{x}" y="{y + i*15}" class="{c}" text-anchor="{a}">{html.escape(ln)}</text>')
        return s
    def box(s, x, y, w, h, txt='', c='b', tc='t', r=8):
        s.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" class="{c}"/>')
        if txt:
            n = len(txt.split('\n'))
            s.t(x + w/2, y + h/2 - (n-1)*7.5 + 4.5, txt, tc)
        return s
    def arrow(s, x1, y1, x2, y2, c='k', dash=False):
        d = ' stroke-dasharray="4 4"' if dash else ''
        s.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{c}"{d} marker-end="url(#{s.id}-ar)"/>')
        return s
    def line(s, x1, y1, x2, y2, c='k', dash=False):
        d = ' stroke-dasharray="4 4"' if dash else ''
        return s.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{c}"{d}/>')
    def circ(s, cx, cy, r, c='k'): return s.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" class="{c}"/>')
    def path(s, d, c='k'): return s.add(f'<path d="{d}" class="{c}"/>')
    def svg(s, title):
        defs = f'<defs><marker id="{s.id}-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 10 5 0 10z" class="mk"/></marker></defs>'
        return (f'<svg class="dg" viewBox="0 0 {s.w} {s.h}" role="img" aria-label="{html.escape(title)}" xmlns="http://www.w3.org/2000/svg">'
                f'<title>{html.escape(title)}</title>{defs}' + ''.join(s.el) + '</svg>\n')

def save(d, title):
    open(os.path.join(OUT, d.id + '.svg'), 'w').write(d.svg(title))

# 1 begin
d = D('begin', 190)
d.path('M40 70c20-30 40 30 60 0s-30-40-40-10 50 30 30 40-60-10-40-30', 'c')
d.t(70, 120, 'A puzzling\nquestion', 'tc')
d.arrow(118, 70, 148, 70); d.box(150, 45, 112, 50, 'Look at how\nwords are used')
d.arrow(264, 70, 290, 70)
d.line(295, 55, 345, 55, 'p'); d.line(295, 70, 345, 70, 'p'); d.line(295, 85, 345, 85, 'p')
d.t(320, 120, 'A clear\nview', 'tp')
d.t(180, 170, 'Not new facts. A better look at familiar ones.', 's')
save(d, 'From a tangled question, through looking at use, to a clear view')

# 2 picture
d = D('picture', 210)
d.t(90, 22, 'MODEL', 'lab'); d.t(270, 22, 'REALITY', 'lab')
d.box(20, 35, 140, 100, '', 'bc'); d.circ(65, 70, 9, 'fc'); d.circ(115, 100, 9, 'fp')
d.t(65, 92, 'button 1', 's'); d.t(115, 122, 'button 2', 's')
d.box(200, 35, 140, 100, '', 'b')
d.path('M240 62h22v14h-22z', 'fc'); d.path('M290 92h22v14h-22z', 'fp')
d.line(270, 40, 270, 130, 'k', True); d.line(205, 85, 335, 85, 'k', True)
d.t(251, 88+0, '', 's')
d.arrow(74, 70, 238, 69, 'p', True); d.arrow(124, 100, 288, 99, 'p', True)
d.t(180, 160, 'Each part stands for a thing.', 't')
d.t(180, 180, 'The arrangement says how things are,', 's')
d.t(180, 195, 'so the model can be true or false.', 's')
save(d, 'Two buttons on a table arranged like two cars at a junction: a model that can be true or false')

# 3 facts
d = D('facts', 190)
d.t(90, 22, 'THINGS', 'lab'); d.t(270, 22, 'A FACT', 'lab')
d.box(20, 35, 140, 95, '', 'b')
d.path('M45 95h40v20h-40z', 'fp'); d.t(65, 140, '', 's')
d.circ(120, 70, 13, 'fc'); d.path('M100 60l12-20 12 20z', 'k')
d.t(90, 148, 'book, cup, lamp…', 's')
d.box(200, 35, 140, 95, '', 'b')
d.path('M240 100h60v20h-60z', 'fp'); d.circ(270, 86, 13, 'fc')
d.t(270, 148, 'the cup is ON the book', 's')
d.arrow(162, 82, 196, 82)
d.t(180, 176, 'The world is how things stand, not a list of things.', 't')
save(d, 'A list of things versus a fact: things arranged in a particular way')

# 4 logic
d = D('logic', 210)
d.t(180, 20, 'Does the sentence tell you about the weather?', 'lab')
d.t(90, 48, '“It is raining.”', 't'); d.t(270, 48, '“It is raining', 't'); d.t(270, 63, 'or it is not.”', 't')
for x0, marks in [(30, ['✓', '✗']), (210, ['✓', '✓'])]:
    d.box(x0, 78, 55, 55, '', 'b'); d.box(x0+65, 78, 55, 55, '', 'bc')
    d.path(f'M{x0+15} 100h25M{x0+12} 108l-4 10M{x0+24} 108l-4 10M{x0+36} 108l-4 10', 'p')
    d.circ(x0+92, 100, 9, 'c')
    d.t(x0+27, 150, 'rain: ' + marks[0], 't'); d.t(x0+92, 150, 'sun: ' + marks[1], 't')
d.t(90, 180, 'Rules some weather out', 'tp'); d.t(90, 195, '→ gives information', 's')
d.t(270, 180, 'True whatever happens', 'tc'); d.t(270, 195, '→ shows logic, says nothing', 's')
save(d, 'A factual sentence is true in some cases; a logical truth is true in every case and says nothing about the weather')

# 5 limits
d = D('limits', 210)
d.circ(120, 105, 75, 'b')
d.t(120, 100, 'What can be', 'tp'); d.t(120, 116, 'said (facts)', 'tp')
d.t(120, 200, 'The edge is shown, not said', 's')
d.path('M262 190 300 30M292 190 330 30', 'k')
for i in range(6):
    y = 175 - i*27; x = 265 + (190-y)*38/160
    d.line(x, y, x+30, y)
d.t(300, 18, 'climb, then let go', 'tc')
d.arrow(205, 105, 255, 105, 'k', True)
save(d, 'A circle of what can be said, its edge only shown; and a ladder to climb up and then throw away')

# 6 ethics
d = D('ethics', 200)
d.t(90, 22, 'RELATIVE VALUE', 'lab'); d.t(270, 22, 'ABSOLUTE VALUE', 'lab')
d.box(20, 35, 140, 100, '', 'b')
d.line(35, 110, 145, 110, 'p')
for i in range(12): d.line(35+i*10, 110, 35+i*10, 104 if i % 5 else 98, 'p')
d.t(90, 70, '“a good runner”', 't'); d.t(90, 128, 'measurable: 11 seconds', 's')
d.box(200, 35, 140, 100, '', 'bc')
d.t(270, 70, '“a good life”', 't'); d.t(270, 98, '?', 'big'); d.t(270, 128, 'no ruler fits', 's')
d.t(180, 160, 'Good FOR something: a fact you can check.', 'tp')
d.t(180, 178, 'Good, full stop: not one more fact in the world.', 'tc')
save(d, 'Relative value can be measured; absolute value is not another measurable fact')

# 7 builders
d = D('builders', 200)
d.circ(60, 75, 14, 'k'); d.path('M60 89v40M60 100l-18 15M60 100l18 15M60 129l-14 30M60 129l14 30', 'k')
d.box(85, 25, 70, 32, '“Slab!”', 'bc', 'tc', 14)
d.circ(290, 75, 14, 'k'); d.path('M290 89v40M290 129l-14 30M290 129l14 30M290 100l-25-5M290 100l25-5', 'k')
d.box(250, 82, 80, 16, '', 'fp', r=2)
d.arrow(160, 110, 245, 110, 'p'); d.t(202, 102, 'acts', 's')
d.t(290, 52, 'brings the slab', 's')
d.t(180, 185, 'Word + action together = a language-game', 't')
save(d, 'Builder A calls Slab! and builder B brings a slab: words and actions woven together')

# 8 meaning-use
d = D('meaning-use', 210)
d.box(130, 85, 100, 40, '“Check!”', 'bc', 'tc')
for (x, y, lab, sub) in [(10, 20, 'Chess', 'a warning move'), (240, 20, 'Restaurant', 'the bill, please'), (10, 160, 'Doctor', 'examine this'), (240, 160, 'To-do list', 'it is done')]:
    d.box(x, y, 110, 36, lab + '\n' + sub, 'b')
d.arrow(150, 85, 100, 58); d.arrow(210, 85, 260, 58); d.arrow(150, 125, 100, 158); d.arrow(210, 125, 260, 158)
save(d, 'One word, Check!, doing different jobs in chess, a restaurant, a clinic and a to-do list')

# 9 family
d = D('family', 210)
for (x, lab, feats) in [(50, 'Chess', 'compete\nrules\nskill'), (130, 'Solitaire', 'rules\nskill\nfun'), (210, 'Catch', 'skill\nfun'), (290, 'Make-\nbelieve', 'fun')]:
    d.circ(x, 85, 50, 'b')
    d.t(x, 60, lab, 'tp'); d.t(x, 92 if '\n' not in lab else 100, feats, 's')
d.path('M10 165c80-20 120 20 170 0s100-20 170 0', 'c'); d.path('M10 172c80-20 120 20 170 0s100-20 170 0', 'c')
d.t(180, 200, 'No thread runs the whole length. The rope holds.', 't')
save(d, 'Games overlap like family members: neighbours share features, but no single feature runs through all')

# 10 life
d = D('life', 200)
d.box(80, 20, 200, 40, '“Good morning”  “3 apples”', 'bc', 'tc', 16)
d.t(195, 82, 'words…', 's', 'start')
d.box(20, 95, 320, 60, '', 'b')
d.t(180, 118, 'greeting · trading · counting · caring', 'tp')
d.t(180, 138, 'eating · playing · mourning · promising', 'tp')
d.arrow(180, 62, 180, 92)
d.t(180, 182, '…rest on shared ways of living.', 't')
save(d, 'Words rest on a ground of shared human activities')

# 11 going-on
d = D('going-on', 200)
d.t(180, 22, 'Rule given: “add 2”', 'lab')
xs = [30, 80, 130, 180]
for x, n in zip(xs, ['996', '998', '1000', '']):
    if n: d.box(x-20, 50, 40, 30, n, 'b')
for x in xs[:2]: d.arrow(x+20, 65, x+30, 65)
d.arrow(200, 65, 255, 40, 'p'); d.arrow(200, 65, 255, 100, 'c')
d.box(260, 25, 70, 30, '1002', 'b', 'tp'); d.box(260, 85, 70, 30, '1004', 'bc', 'tc')
d.t(295, 70, 'teacher', 's'); d.t(295, 130, 'pupil', 's')
d.t(180, 160, 'The formula alone does not stop the pupil.', 't')
d.t(180, 178, 'Shared training and practice fix what “correct” is.', 's')
save(d, 'After 1000 the teacher expects 1002 but the pupil writes 1004: the rule needs a practice')

# 12 interpretation
d = D('interpretation', 200)
d.path('M50 160V40M50 50h60l15 12-15 12H50', 'k'); d.t(80, 66, 'rule', 's')
d.t(160, 40, '→ interpretation → interpretation → …', 'tc', 'start')
d.line(160, 33, 345, 47, 'c')
d.t(160, 60, 'never reaches an action', 's', 'start')
d.arrow(60, 120, 150, 120, 'p'); d.box(155, 100, 170, 40, 'Follow it: walk the path', 'b', 'tp')
d.t(240, 160, 'Understanding shows in what we do.', 't')
d.t(180, 188, '“Explanations come to an end somewhere.”', 's')
save(d, 'Interpreting a signpost with another interpretation never ends; following it in practice does')

# 13 private
d = D('private', 210)
d.t(90, 22, 'PUBLIC WORD', 'lab'); d.t(270, 22, 'PRIVATE SIGN', 'lab')
d.box(20, 35, 140, 110, '', 'b'); d.t(90, 65, '“pain”', 'tp')
d.t(90, 88, 'others see: wince,', 's'); d.t(90, 102, 'injury, comforting', 's')
d.t(90, 128, 'can be corrected ✓', 't')
d.box(200, 35, 140, 110, '', 'bc')
for i in range(5):
    d.box(212+i*25, 55, 20, 20, 'S' if i in (0, 2, 3) else '', 'b', 'tc', 3)
d.t(270, 100, 'same as last time?', 's'); d.t(270, 128, 'nothing to check ✗', 't')
d.t(180, 172, 'If only my impression decides, “right” and', 't')
d.t(180, 188, '“seems right” collapse into one.', 't')
save(d, 'A public word can be corrected by others; a purely private sign has no check')

# 14 beetle
d = D('beetle', 200)
for i, x in enumerate([50, 140, 230, 320]):
    d.box(x-30, 60, 60, 50, '?', 'b', 'big')
    d.circ(x, 135, 9, 'k'); d.line(x, 144, x, 165)
    d.box(x-28, 20, 56, 24, '“beetle”', 'bc', 's', 10)
d.t(180, 192, 'No one sees inside another box. The word still works.', 't')
save(d, 'Everyone has a box with a beetle that only they can see; the word beetle is still used')

# 15 criteria
d = D('criteria', 200)
d.t(90, 22, 'CRITERION', 'lab'); d.t(270, 22, 'EVIDENCE', 'lab')
d.box(20, 35, 140, 95, '', 'b')
for x in range(45, 140, 20): d.line(x, 50, x-6, 70, 'p'); d.line(x+8, 80, x+2, 100, 'p')
d.t(90, 120, 'rain falling', 's')
d.box(200, 35, 140, 95, '', 'bc'); d.path('M215 105h110', 'k'); d.path('M235 102c10-6 25-6 35 0M280 102c10-6 25-6 35 0', 'p')
d.t(270, 120, 'wet streets, puddles', 's')
d.t(90, 150, 'what COUNTS as rain', 'tp'); d.t(270, 150, 'what makes rain LIKELY', 'tc')
d.t(180, 182, 'Sprinklers can wet the street. Evidence can mislead.', 's')
save(d, 'A criterion is what counts as rain; evidence such as wet streets only makes rain likely')

# 16 aspects
d = D('aspects', 200)
def cube(ox, oy, hl):
    d.path(f'M{ox} {oy+30}h60v60h-60z', 'k'); d.path(f'M{ox+30} {oy}h60v60h-60z', 'k')
    for a, b in [((ox, oy+30), (ox+30, oy)), ((ox+60, oy+30), (ox+90, oy)), ((ox, oy+90), (ox+30, oy+60)), ((ox+60, oy+90), (ox+90, oy+60))]:
        d.line(*a, *b)
    d.path(hl, 'fpa')
cube(30, 30, 'M30 60h60v60h-60z'); cube(220, 30, 'M250 30h60v60h-60z')
d.t(75, 145, 'front face low', 's'); d.t(265, 145, 'front face high', 's')
d.t(180, 80, '⇄', 'big')
d.t(180, 175, 'Same lines. Nothing changed but how you see them.', 't')
save(d, 'One wire cube seen two ways: the drawing stays the same while the aspect flips')

# 17 hinges
d = D('hinges', 200)
d.path('M70 25v150', 'k'); d.box(75, 25, 160, 150, '', 'b', r=3)
d.box(62, 45, 16, 26, '', 'fc', r=3); d.box(62, 130, 16, 26, '', 'fc', r=3)
d.t(155, 95, 'questions,', 'tp'); d.t(155, 112, 'checking, doubts', 'tp')
d.circ(215, 100, 5, 'k')
d.t(250, 50, '“I have hands.”', 's', 'start'); d.t(250, 140, '“The earth is old.”', 's', 'start')
d.arrow(248, 46, 82, 58, 'c', True); d.arrow(248, 136, 82, 143, 'c', True)
d.t(180, 194, 'The door moves only because the hinges stay put.', 't')
save(d, 'A door of questions turning on hinges of certainties that are not themselves questioned')

# 18 doubt
d = D('doubt', 200)
d.t(90, 22, 'WORKING DOUBT', 'lab'); d.t(270, 22, 'IDLE DOUBT', 'lab')
d.box(20, 35, 140, 110, '', 'b'); d.t(90, 65, '“Did I lock\nthe door?”', 'tp')
d.box(200, 35, 140, 110, '', 'bc'); d.t(270, 65, '“Do I really\nhave hands?”', 'tc')
d.t(90, 115, 'go and check ✓', 't'); d.t(90, 132, 'clear way to settle it', 's')
d.t(270, 115, 'check with… what? ✗', 't'); d.t(270, 132, 'nothing is surer', 's')
d.t(180, 178, 'A real doubt needs a reason and a way to check.', 't')
save(d, 'A working doubt can be checked; an idle doubt has no test that could settle it')

# 19 colour
d = D('colour', 200)
d.box(140, 20, 80, 50, '', 'fc'); d.t(180, 90, 'a colour puzzle', 's')
d.arrow(150, 72, 80, 115, 'p'); d.arrow(210, 72, 280, 115, 'c')
d.box(10, 118, 150, 50, 'Why does it look\nlighter here?', 'b', 'tp')
d.box(200, 118, 150, 50, 'Could there be a\ntransparent white?', 'bc', 'tc')
d.t(85, 186, 'ask physics: light, eyes', 's'); d.t(275, 186, 'ask how we use colour words', 's')
save(d, 'A colour puzzle can be a question for science or a question about our concepts')

# 20 will
d = D('will', 200)
d.t(90, 22, 'A REGULARITY', 'lab'); d.t(270, 22, 'A COMPULSION', 'lab')
d.box(20, 35, 140, 100, '', 'b')
for i in range(6): d.circ(40+i*22, 85 - (i % 2)*12, 5, 'fp')
d.t(90, 122, 'what tends to happen', 's')
d.box(200, 35, 140, 100, '', 'bc')
d.circ(240, 75, 9, 'k'); d.line(240, 84, 240, 115); d.circ(300, 75, 9, 'k'); d.line(300, 84, 300, 115)
d.arrow(250, 95, 288, 95, 'c'); d.t(270, 122, 'someone forces you', 's')
d.t(180, 162, 'Being predictable is not the same as being pushed.', 't')
save(d, 'A law describing regularities is different from a force compelling an action')

# 21 grammar
d = D('grammar', 200)
for r in range(4):
    for c in range(4):
        d.box(30+c*30, 30+r*30, 30, 30, '', 'b' if (r+c) % 2 == 0 else 'bc', r=0)
d.t(75, 82, '♔', 'big')
for (dx, dy) in [(-30, 0), (30, 0), (0, -30), (0, 30), (30, 30)]: d.arrow(75+dx*0.45, 75+dy*0.45, 75+dx*0.95, 75+dy*0.95, 'p')
d.t(240, 60, 'What makes this', 't'); d.t(240, 76, 'the king?', 't')
d.t(240, 104, 'Not its shape:', 's'); d.t(240, 118, 'the rules for moving it.', 's')
d.t(180, 172, 'A word’s grammar = the rules for using it.', 't')
save(d, 'A chess king is defined by how it may move, as a word is by the rules for its use')

# 22 ritual
d = D('ritual', 200)
d.box(140, 30, 80, 70, '', 'b', r=4); d.circ(180, 57, 12, 'p'); d.path('M160 95c5-20 35-20 40 0', 'p')
d.t(180, 118, 'kissing a photo of', 's'); d.t(180, 132, 'someone you love', 's')
d.box(5, 35, 125, 60, '“This will\nreach her.”\n(bad science)', 'bc', 'tc'); d.line(10, 40, 125, 90, 'c')
d.box(230, 35, 125, 60, '“I love her.”\n(expression)', 'b', 'tp')
d.t(180, 172, 'Ask what an act means in a life,', 't'); d.t(180, 188, 'not only whether it “works”.', 't')
save(d, 'Kissing a photo is not a failed prediction but an expression of love')

# 23 psychology
d = D('psychology', 200)
d.box(130, 20, 100, 36, 'experience', 'b', 'tp')
d.box(20, 130, 120, 36, 'expression\n(wince, words)', 'bc', 'tc')
d.box(220, 130, 120, 36, 'circumstances\n(a burn, a fall)', 'b')
d.line(160, 58, 90, 128); d.line(200, 58, 270, 128); d.line(142, 148, 218, 148)
d.t(180, 112, 'learned together', 's')
d.t(180, 190, 'Peacocke asks: does this triangle explain everything?', 's')
save(d, 'Experience, its expression and its circumstances are tied together in how we learn feeling words')

# 24 method
d = D('method', 210)
d.path('M120 190h120v-90c0-30-35-35-35-60V20h-50v20c0 25-35 30-35 60z', 'k')
d.path('M163 120c-6-6-6-14 0-14s6 8 0 14zm0 0c6-6 14-6 14 0s-8 6-14 0z', 'fp')
d.path('M155 115c-8 0-10-10-2-10', 'k')
d.arrow(180, 110, 180, 10, 'c', True)
d.t(255, 70, 'the way out', 'tc', 'start')
d.t(255, 86, 'was always open', 's', 'start')
d.t(20, 140, 'stuck', 't', 'start'); d.t(20, 156, 'buzzing', 's', 'start')
save(d, 'A fly trapped in a bottle whose neck is open: philosophy shows the way out')

# 25 reading-lab
d = D('reading-lab', 230)
steps = [('1', 'Locate it', 'which edition, which §'), ('2', 'Hear the voices', 'who speaks? who objects?'), ('3', 'Find the target', 'which picture is questioned?'), ('4', 'Keep the hedges', '“for a large class of cases”'), ('5', 'Argue back', 'your own view, with reasons')]
for i, (n, a, b) in enumerate(steps):
    y = 10 + i*44
    d.circ(30, y+18, 15, 'fc'); d.t(30, y+23, n, 'tw')
    d.t(58, y+16, a, 'tp', 'start'); d.t(58, y+31, b, 's', 'start')
    if i < 4: d.line(30, y+34, 30, y+47)
save(d, 'Five steps to read a remark closely')

# 26 daily-life
d = D('daily-life', 220)
pts = [(180, 35, 'Notice a word\ndoing too much'), (300, 110, 'Look at how\nit is used here'), (180, 185, 'Compare\ncases'), (60, 110, 'Decide, stay open\nto correction')]
for (x, y, lab) in pts: d.box(x-62, y-20, 124, 40, lab, 'b')
d.arrow(240, 45, 290, 88); d.arrow(290, 132, 240, 175); d.arrow(120, 175, 70, 132); d.arrow(70, 88, 120, 45)
d.t(180, 115, 'a daily habit', 'tc')
save(d, 'A daily cycle: notice a word, look at its use, compare cases, decide while staying open')
print('wrote', len(os.listdir(OUT)), 'diagrams')

# ---------- Section diagrams (one per section), from scripts/sections.py ----------
import sys, textwrap
sys.path.insert(0, os.path.dirname(__file__))
from sections import S as SECTIONS
SOUT = os.path.join(OUT, 'sections'); os.makedirs(SOUT, exist_ok=True)
def wrap(txt, chars): return '\n'.join(textwrap.wrap(txt, chars, break_long_words=False)) or txt
def tbox(d, x, y, w, h, txt, cls='b', tcls='t', chars=None, r=8):
    d.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" class="{cls}"/>')
    lines = wrap(txt, chars or max(8, int(w/6.6))).split('\n')
    y0 = y + h/2 - (len(lines)-1)*7.5 + 4.5
    d.t(x+w/2, y0, '\n'.join(lines), tcls)
def lines_of(txt, chars): return len(wrap(txt, chars).split('\n'))
def render(sid, spec):
    kind = spec[0]
    if kind == 'vs':
        _, ha, ta, hb, tb, note = spec
        n = max(lines_of(ta, 21), lines_of(tb, 21)); bh = 30 + n*15
        d = D(sid, 28 + bh + 16 + lines_of(note, 52)*15 + 6)
        d.t(90, 18, ha.upper(), 'lab'); d.t(270, 18, hb.upper(), 'lab')
        tbox(d, 15, 28, 150, bh, ta, 'b', 'tp', 21); tbox(d, 195, 28, 150, bh, tb, 'bc', 'tc', 21)
        d.t(180, 28 + bh/2 + 4, 'vs', 's')
        nl = wrap(note, 52); d.t(180, 28 + bh + 24, nl, 's')
        return d
    if kind == 'flow':
        _, steps, note = spec
        k = len(steps); gap = 14; w = (330 - gap*(k-1)) / k; ch = max(6, int(w/(6.0 if k >= 4 else 7.2)))
        n = max(lines_of(s, ch) for s in steps); bh = 26 + n*15
        d = D(sid, 20 + bh + 50)
        for i, s in enumerate(steps):
            x = 15 + i*(w+gap); tbox(d, x, 15, w, bh, s, 'b' if i < k-1 else 'bc', ('t' if i < k-1 else 'tc') + (' sm' if k >= 4 else ''), ch)
            if i < k-1: d.arrow(x+w+1, 15+bh/2, x+w+gap-1, 15+bh/2)
        d.t(180, 15 + bh + 26, wrap(note, 52), 's')
        return d
    if kind == 'hub':
        _, center, spokes, note = spec
        k = len(spokes); cols = 2 if k <= 4 else 3; rows = (k + cols - 1)//cols
        w = (330 - (cols-1)*12)/cols; ch = max(8, int(w/7.2))
        bh = 18 + max(lines_of(s, ch) for s in spokes)*15
        top = 18 + 16 + lines_of(center, 40)*15
        d = D(sid, top + 22 + rows*(bh+12) + 34)
        tbox(d, 70, 10, 220, top-6, center, 'bc', 'tc', 36, 16)
        for i, s in enumerate(spokes[:cols]):
            x = 15 + i*(w+12); d.line(180, top+4, x+w/2, top+22, 'k', True)
        if rows > 1: d.add(f'<rect x="8" y="{top+16}" width="344" height="{rows*(bh+12)}" rx="12" class="grp"/>')
        for i, s in enumerate(spokes):
            r, c = divmod(i, cols); x = 15 + c*(w+12); y = top + 22 + r*(bh+12)
            tbox(d, x, y, w, bh, s, 'b', 't', ch)
        d.t(180, top + 22 + rows*(bh+12) + 16, wrap(note, 52), 's')
        return d
    if kind == 'stack':
        _, layers, note = spec
        bh = 34; d = D(sid, 14 + len(layers)*(bh+8) + 40)
        for i, s in enumerate(layers):
            inset = (len(layers)-1-i)*14
            tbox(d, 15+inset, 12+i*(bh+8), 330-2*inset, bh, s, 'b' if i < len(layers)-1 else 'bc', 'tp' if i < len(layers)-1 else 'tc', 48)
        d.t(180, 12 + len(layers)*(bh+8) + 18, wrap(note, 52), 's')
        return d
    if kind == 'branch':
        _, root, a, b, note = spec
        n = max(lines_of(a, 21), lines_of(b, 21)); bh = 24 + n*15
        rh = 24 + lines_of(root, 40)*15
        d = D(sid, 12 + rh + 34 + bh + 46)
        tbox(d, 60, 10, 240, rh, root, 'bc', 'tc', 38)
        y = 10 + rh + 34
        d.arrow(150, 12+rh, 90, y-2, 'p'); d.arrow(210, 12+rh, 270, y-2, 'c')
        tbox(d, 15, y, 150, bh, a, 'b', 'tp', 21); tbox(d, 195, y, 150, bh, b, 'b', 't', 21)
        d.t(180, y + bh + 26, wrap(note, 52), 's')
        return d
    raise ValueError(kind)
count = 0
for lid, secs in SECTIONS.items():
    for i, (spec, q) in enumerate(secs):
        d = render(f'{lid}-{i}', spec)
        open(os.path.join(SOUT, f'{lid}-{i}.svg'), 'w').write(d.svg(spec[-1])); count += 1
print('wrote', count, 'section diagrams')
