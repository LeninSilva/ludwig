"""Source for data/visuals.json. Run: python3 scripts/visuals-source.py
Every example is an invented teaching example, not a quotation."""
import json, os
V = {
'begin': dict(
 plain="Many philosophical puzzles come from a misleading picture of how words work. Wittgenstein’s method: look closely at how words are actually used, and the puzzle often loosens.",
 caption="Not new facts, but a clearer look at familiar ones.",
 example=("“What is time?”", "Asked out of the blue, you are stuck. Yet you use “time” perfectly well every day: “Is it time to go?”, “That took a long time.” Looking at those uses helps more than hunting for a hidden essence of time."),
 concept="A person standing in a cluttered study, gently untangling a large knotted ball of thread that becomes neat parallel lines as it leaves their hands; a window with soft daylight.",
 ex="A person at a kitchen table glancing at a wall clock and a calendar while putting on a coat, a small thought cloud with a question mark that is unravelling into a simple ribbon."),
'picture': dict(
 plain="A sentence can work like a model: its parts stand for things, and how the parts are arranged says how things are. That is why it can be true or false.",
 caption="The model shares an arrangement with reality, not a look.",
 example=("Explaining a car accident with salt and pepper shakers", "You place the salt for your car and the pepper for the other car. Nobody thinks the shakers are cars, yet the layout shows what happened, and someone could say “No, it was the other way round.”"),
 concept="A tabletop model of a street junction made of buttons and matchsticks, with a faint ghostly image of real cars at the same junction hovering above it, dotted lines linking each button to a car.",
 ex="Two friends at a café table, one pushing a salt shaker and a pepper shaker across the tablecloth to re-enact a small car accident, the other leaning in to watch."),
'facts': dict(
 plain="The world is not just a pile of things; it is how those things stand to each other. “The cup is on the book” is a fact. A list of the cup and the book is not.",
 caption="Same things, different arrangement, different fact.",
 example=("Moving one cup", "A cup, a book and a lamp sit on your desk. Move the cup from the book to the shelf: no new thing appeared, yet what is the case has changed."),
 concept="Two side-by-side panels of the same desk with the same three objects (a cup, a book, a lamp); in one the cup rests on the book, in the other it sits on a shelf.",
 ex="A hand lifting a coffee cup off a closed book on a tidy desk and placing it on a shelf, motion suggested with soft curved lines."),
'logic': dict(
 plain="“It is raining” tells you something because it could be false. “It is raining or it is not” is true no matter what, so it tells you nothing about the weather. It shows the structure of logic instead.",
 caption="Information rules something out. A logical truth rules nothing out.",
 example=("A useless forecast", "A weather app that always says “Rain or no rain tomorrow” is never wrong, and never helpful. Its sentence is perfectly logical and completely empty of news."),
 concept="A calm landscape split down the middle: rain on one side, sunshine on the other, with a single umbrella-shaped sign in the centre covering both halves equally.",
 ex="A person looking at a phone whose screen shows half a raincloud and half a sun, shrugging with a gentle, amused expression."),
'limits': dict(
 plain="Some things cannot be stated in words but can still show themselves, such as the logic of language itself. Wittgenstein says his own book is a ladder: climb it, then put it away.",
 caption="Inside: what can be said. The edge itself is only shown.",
 example=("Explaining a joke", "You can describe every word of a joke and still not show why it is funny; the humour shows itself when someone gets it. Some understanding is reached rather than stated."),
 concept="A wooden ladder leaning against a high stone wall in a meadow, a figure at the top looking out over a wide view, the ladder about to be set aside.",
 ex="Two friends laughing together at a café table while a third person looks at a notebook of written-out explanations, puzzled."),
'ethics': dict(
 plain="“Good” can mean good for a purpose, which you can measure, like a good runner. Ethics is about a different kind of good, and Wittgenstein argues it is not one more fact you could look up.",
 caption="A ruler can measure a runner, not the worth of a life.",
 example=("Two kinds of “good”", "“That’s a good knife” means it cuts well, and you can test it. “He is a good person” isn’t settled by any test of that kind, though it matters far more."),
 concept="A large old book open on a lectern, its pages filled with precise measurements and charts, while a small figure outside the window helps someone carry groceries; warm light falls on the helper, not the book.",
 ex="A kitchen knife slicing a tomato cleanly on one side of the image; on the other, a person holding a door open for an elderly neighbour."),
'builders': dict(
 plain="A language-game is talking and doing woven together. Words get their life from the activities they are part of, like a builder calling “Slab!” and a helper bringing one.",
 caption="The word works inside the activity.",
 example=("“Scalpel!”", "In surgery, one word is a complete order. Outside the operating room the same word might be a question, a joke or a spelling test. The activity sets its job."),
 concept="Two builders on a sunny building site: one calls out with a raised hand while the other carries a large stone slab toward them; stacks of blocks, pillars and beams around.",
 ex="An operating theatre seen in soft muted colours: a surgeon extends an open hand and a nurse places an instrument in it, both focused and calm."),
'meaning-use': dict(
 plain="For many words, the meaning is how the word is used, not some object hidden behind it. Words are like tools in a toolbox: they do very different jobs.",
 caption="One word, different jobs in different settings.",
 example=("“Fine”", "“I’m fine” can mean “I’m well”, “stop asking” or “I’m not fine at all”, depending on tone and situation. You learn what it means by seeing how it is used."),
 concept="An open wooden toolbox in which the tools (hammer, screwdriver, ruler, glue pot) each have a small word-shaped tag, laid out neatly on a workbench.",
 ex="Three small scenes in a row of the same person saying a word: smiling at a café, turning away from a nosy colleague, and staring at rain from a window with crossed arms."),
'family': dict(
 plain="Some ideas have no single feature all their cases share. “Game” covers chess, catch and make-believe through overlapping likenesses, like family members who resemble each other in different ways.",
 caption="Overlapping fibres make a strong rope.",
 example=("What makes something a “sport”?", "Football has teams, golf doesn’t; chess has competition but little running; yoga has skill but no winner. There is no one common feature, yet we use “sport” without trouble."),
 concept="A family portrait of four generations: each person shares some features with a neighbour (the same nose, the same eyes, the same hair) but no single feature runs through them all.",
 ex="A park scene with people playing chess on a bench, kids playing catch, someone playing solitaire, and a child playing pretend with a cardboard crown."),
'life': dict(
 plain="Language rests on shared ways of living: how we greet, count, trade, play and grieve. Understanding words means sharing enough of the life they belong to.",
 caption="Words grow out of what we do together.",
 example=("Tipping abroad", "A traveller can know the word for “tip” and still be lost about when to give one, how much, and what it means. The word only makes sense against a whole practice."),
 concept="A bustling village square: people greeting, a market stall weighing apples, children playing, a small funeral procession at the edge; speech is suggested only by gestures.",
 ex="A traveller at a restaurant table holding coins over the bill, hesitating, while a waiter waits politely."),
'going-on': dict(
 plain="Knowing a rule means being able to go on correctly in new cases. No formula or inner flash forces the next step; training and shared practice do.",
 caption="After 1000, “add 2” needs a practice behind it.",
 example=("Learning to knit", "The pattern says “knit two, purl two”. You understand it when your hands can keep going row after row, not when you can recite it."),
 concept="A teacher and a pupil at a blackboard covered with a number series; the series runs smoothly then forks into two paths at the edge of the board.",
 ex="Hands knitting a scarf, the pattern of stitches visibly repeating, a printed pattern card lying beside the yarn."),
'interpretation': dict(
 plain="If every rule needed another rule to explain how to apply it, we would never act. At some point we simply follow it; understanding shows in what we do.",
 caption="An endless chain of interpretations never reaches an action.",
 example=("Instructions that never end", "Imagine a recipe that says “season to taste”, then a note explaining “to taste”, then a note explaining that note… A cook just tastes and adds salt."),
 concept="A traveller standing at a wooden signpost in open country; the signpost points down a path, and the traveller is already walking that path.",
 ex="A cook tasting soup from a wooden spoon over a pot, a recipe card on the counter with a long trail of tiny footnotes spilling off its edge."),
'private': dict(
 plain="Could someone invent a word that only they could ever understand, for a sensation only they could check? Wittgenstein argues such a sign would have no standard of correct use.",
 caption="A public word can be corrected. A purely private sign can’t.",
 example=("The diary of “S”", "Someone writes “S” in a diary whenever a certain feeling comes back. But what decides whether today’s feeling is really the same one? If only memory decides, “seems right” and “is right” can’t come apart."),
 concept="A small open diary on a nightstand, with the letter S written on several days of a calendar page, lit by a bedside lamp at night.",
 ex="A person sitting on the edge of a bed in the morning, pen in hand over a diary, pausing with a thoughtful, unsure expression."),
'beetle': dict(
 plain="Imagine everyone has a box with a “beetle” that no one else can see. The word “beetle” still works, so what is in the box plays no part in the word’s shared meaning.",
 caption="No one sees into another box, and the word still works.",
 example=("“Tastes like coriander”", "You can’t compare your taste experience with mine directly, yet we both say coriander is soapy or fresh and argue about it. The shared word lives in what we say and do."),
 concept="A row of people each holding a small closed wooden box close to their chest, each peeking into their own box; one of them is speaking to the others.",
 ex="Two friends at a market stall smelling fresh coriander, one wrinkling their nose, the other smiling."),
'criteria': dict(
 plain="A criterion is what counts as something; evidence only makes it likely. Rain falling counts as rain; wet streets are evidence of rain.",
 caption="What counts as rain versus what suggests rain.",
 example=("Is the cake done?", "A clean toothpick is evidence that the cake is baked. Being cooked through is what being done means. Evidence can mislead; that is why we still sometimes cut into a raw cake."),
 concept="A city street in two panels: one with rain visibly falling on umbrellas, the other dry sky but wet pavement and a street-cleaning truck around the corner.",
 ex="A person pulling a toothpick out of a cake in an oven, examining it in warm kitchen light."),
'aspects': dict(
 plain="You can look at the same picture and suddenly see it differently, like a cube that flips. Nothing on the paper changed, yet what you see did.",
 caption="Same lines, two ways of seeing.",
 example=("A familiar face in a stranger", "You look at a stranger and suddenly see your brother’s smile in them. Their face hasn’t changed, but now you can’t unsee the likeness."),
 concept="A large wire-frame cube drawn on paper on an easel, with two faint viewers on either side seeing it from above and from below.",
 ex="A person on a train looking up from a book, struck by a passenger across the aisle, with a small inset memory-frame showing a sibling with the same smile."),
'hinges': dict(
 plain="Some certainties are not conclusions we reached but the hinges our questions turn on, like “I have hands” or “the earth existed long before me”. Doubt needs something that stays fixed.",
 caption="The door moves only because the hinges stay put.",
 example=("Checking a bank statement", "You can doubt one charge and check it, but only because you take for granted that the numbers on the page don’t change while you read them."),
 concept="A heavy wooden door swinging open on two large iron hinges, the hinges lit warmly and the door slightly blurred as it moves.",
 ex="A person at a kitchen table holding a paper bank statement, circling one line with a pencil, a calculator nearby."),
'doubt': dict(
 plain="A real doubt needs a reason and a way to check. “Did I lock the door?” is a working doubt; “Do I have hands?” has no test that could settle it, so it isn’t really doubting.",
 caption="Doubt that can be checked versus doubt with nowhere to go.",
 example=("The locked door", "Halfway to work, you wonder if you locked the door. You can go back, try the handle and settle it. Doubting whether the door exists at all would leave you nothing to check."),
 concept="A person walking back up a garden path to try a front-door handle, while a second, faint version of the same person stands confused in an empty, featureless space.",
 ex="A person on a bus checking their keys and looking back over their shoulder toward home."),
'colour': dict(
 plain="Some colour questions are for science (why does this look lighter?) and some are about our concepts (could there be a see-through white?). Wittgenstein separates the two.",
 caption="One puzzle, two kinds of question.",
 example=("Transparent white", "Green glass makes things look green. But a “white glass” would just look milky; things behind it wouldn’t look white. The puzzle is about how “white” works, not about physics."),
 concept="A painter’s table with paint tubes, a sheet of white paper beside snow outside a window, and a pane of tinted glass casting coloured light.",
 ex="Hands holding up a pane of green glass and a pane of milky glass in front of a window, the view through one green, through the other cloudy."),
'will': dict(
 plain="Being predictable is not the same as being forced. A law of nature describes what tends to happen; it doesn’t push you to act.",
 caption="A regularity is not a hand on your back.",
 example=("Your morning coffee", "Your friend can predict you’ll order coffee at 8 a.m. That prediction doesn’t make you order it; you do, for your own reasons."),
 concept="A calm figure walking along a path of evenly spaced footprints, contrasted with a faint second figure being shoved by a large hand, the two separated by a clear line.",
 ex="A person ordering coffee at a café counter at 8 a.m. while a friend nearby smiles knowingly, holding up a clock."),
'grammar': dict(
 plain="In Wittgenstein’s sense, a word’s grammar is the rules for using it, much like a chess king is defined by how it may move, not by its shape.",
 caption="The rules for moving it make it a king.",
 example=("A bottle cap as a king", "Lose the king from a chess set and use a bottle cap instead. It works perfectly, because what makes it the king is the moves allowed, not the carving."),
 concept="A chessboard seen from above with a carved king, soft arrows showing its possible one-square moves, and the other pieces at rest.",
 ex="Two people playing chess on a porch where one king has been replaced by a bottle cap, both players perfectly serious."),
'ritual': dict(
 plain="Rituals are not always bad attempts at science. Kissing a photo of someone you love isn’t a mistaken prediction that the kiss will reach them; it expresses love.",
 caption="An act can express something without trying to cause something.",
 example=("Blowing out birthday candles", "No one thinks the candles physically grant wishes, yet the act is full of meaning. Asking “does it work?” misses what it means."),
 concept="A person by a window gently kissing a framed photograph, a candle and flowers on the sill, evening light.",
 ex="A family around a birthday cake as a child blows out the candles, everyone clapping."),
'psychology': dict(
 plain="We learn words for feelings through how feelings show (wincing, saying “ouch”) in situations like a burn or a fall. The critic Peacocke asks whether this explains everything about experience.",
 caption="Experience, expression and circumstances, learned together.",
 example=("Learning “ouch”", "A toddler bumps a knee, cries, and a parent says “Ouch! That hurts.” The child learns “hurt” from the bump, the crying and the comfort together, not by pointing inward."),
 concept="Three overlapping circles drawn on paper on a desk, with a small figure in each: one holding their hand after touching a stove, one wincing, one with a calm inner glow.",
 ex="A parent kneeling to comfort a toddler with a bumped knee on a playground, the toddler mid-cry."),
'method': dict(
 plain="Philosophy, for Wittgenstein, is not about discovering new facts but about clearing up confusion by arranging what we already know, so we can see our way out.",
 caption="A fly in a bottle: the way out was always open.",
 example=("Lost in your own home", "In a dark room you bump into furniture you know well. Turning on the light adds nothing new to the room; it lets you see what was already there."),
 concept="A glass bottle on a windowsill with a fly inside; the bottle’s neck is open to the sky and a soft beam of light shows the way out.",
 ex="A hand switching on a lamp in a familiar living room, the furniture becoming clear, a person who had bumped a chair now smiling."),
'reading-lab': dict(
 plain="Read a numbered remark slowly: find exactly which edition and section it is, notice who is speaking, what idea it targets, which hedges matter, and what you think.",
 caption="Five steps for reading a remark closely.",
 example=("Reading §43", "Note the hedge: meaning is use “for a large class of cases”, not for all. Dropping those words turns a careful remark into a slogan."),
 concept="A reading desk with an open book, a pencil, small sticky tabs marking numbered sections and a magnifying glass resting on one paragraph.",
 ex="A close-up of a page with one sentence underlined and a margin note circling the words “a large class of cases”."),
'daily-life': dict(
 plain="Bring the tools into an ordinary day: notice a word doing too much work, look at how it is used here, compare cases, decide, and stay open to correction.",
 caption="A small, repeatable habit.",
 example=("“Productive”", "Your team argues about whether a week was “productive”. Ask: productive in which sense? Shipped work, learning, rest? The argument often turns out to be several smaller, answerable questions."),
 concept="A person walking through an ordinary day (breakfast, a bus, an office, a park) with a small notebook, pausing to jot down a word at each stop.",
 ex="A team around a whiteboard where the word “productive” is circled and split into three branches, people nodding."),
}
STYLE = ("Style: mid-century modernist print illustration, flat shapes with subtle paper grain, ivory paper background, "
         "pine green, muted terracotta, sand and sage accents, calm and inviting, no text, letters or numbers in the image, "
         "4:3 landscape, 1600×1200 pixels.")
lessons = json.load(open(os.path.join(os.path.dirname(__file__), '..', 'data', 'lessons.json')))
ids = [l['id'] for l in lessons]
assert set(ids) == set(V), set(ids) ^ set(V)
import sys; sys.path.insert(0, os.path.dirname(__file__))
from insights import INSIGHT, QUESTION_WAYS
from sections import S as SECTIONS, GUIDE
alts = json.load(open(os.path.join(os.path.dirname(__file__), '..', 'data', 'illustration-alts.json')))
assert set(INSIGHT) == set(V)
import re
def clean_stage(g):
    g = re.sub(r'^(First|Then|Later still|Later|Deeper|With use|Living with it|At first)[:,]?\s+', '', g)
    return g[0].upper() + g[1:]
out = []
for i in ids:
    v = V[i]
    ins = INSIGHT[i]; assert len(ins['ask']) == 3
    out.append({'id': i, 'plain': v['plain'], 'diagramCaption': v['caption'],
                'example': {'title': v['example'][0], 'text': v['example'][1], 'label': 'Invented example'},
                'insight': {'misreading': ins['misreading'], 'matters': ins['matters']},
                'askYourself': ins['ask'],
                'sectionQuestions': [q for (_, q) in SECTIONS[i]],
                'guide': {'say': GUIDE[i][0], 'read': GUIDE[i][1], 'grow': [clean_stage(g) for g in GUIDE[i][2]]},
                'illustrations': {
                    'concept': {'file': f'{i}-concept', 'alt': alts.get(f'{i}-concept', ''), 'prompt': v['concept'] + ' ' + STYLE},
                    'example': {'file': f'{i}-example', 'alt': alts.get(f'{i}-example', ''), 'prompt': v['ex'] + ' ' + STYLE}}})
json.dump(out, open(os.path.join(os.path.dirname(__file__), '..', 'data', 'visuals.json'), 'w'), ensure_ascii=False, indent=1)
json.dump([{'question': q, 'how': h, 'example': e} for q, h, e in QUESTION_WAYS], open(os.path.join(os.path.dirname(__file__), '..', 'data', 'questions.json'), 'w'), ensure_ascii=False, indent=1)
print('wrote', len(out), 'visual entries and', len(QUESTION_WAYS), 'question ways')
