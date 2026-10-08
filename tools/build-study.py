"""Writes data/study.json (the chapters), data/sources.json and data/plates.json.
Every quotation is taken from data/file.json (read at the page images) or from a source checked as noted
in sources.json. Run from the repository root:  python tools/build-study.py"""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent

def q(de, en, href, label):
    return {"de": de, "en": en, "cite": {"href": href, "label": label}}

CH = [
 {"id": "weapon", "n": 1, "date": "1943 – 16 April 1944", "part": "April 1944: the plan",
  "title": "Beethoven",
  "lede": "A pilotless Ju 88 packed with explosives, steered to its target by a fighter on its back. In April 1944 the Luftwaffe's operations staff asked what to do with it.",
  "body": [
   "The \"Mistel\" (mistletoe) was a composite aircraft: a Junkers Ju 88 bomber without a crew, its crew cockpit taken off and a hollow-charge warhead fitted in its place, carried into the air by its own two engines and guided by a Messerschmitt Bf 109 fighter mounted on struts above it. Near the target the fighter pilot aimed the whole combination, released the bomber and turned for home. The project's cover name was \"Beethoven\".",
   "On 16 April 1944 the Luftwaffe Operations Staff sent a short study \"on the possible uses of the Mistel\" up the chain of command, with a technical annex, a note on the enemy's heavy ships and two maps. The file survives in the war diary of the operations staff, captured by the Allies and filmed by the US National Archives (microfilm T-321, roll 10). It is the planning document behind this study.",
   "The technical annex sets out what the staff had: two prototypes for training, thirteen more combinations due by 15 June, two hollow-charge warheads for each aircraft, a crane with a hook 7.50 m high to fit them, and 45 men, 21 of them soldiers and the rest from industry. The trials were in the hands of 2./KG 101 under Hauptmann Rudat; the attack itself was to go to IX Air Corps, \"since General Peltz personally suggested the Mistel method\".",
   "Everything depended on range. Without extra fuel the combination reached 400–500 km, which the staff thought \"of little value\". With a 300-litre tank on the fighter it reached 750–800 km; that was demanded and could be done \"without technical difficulty\". A depth of 1,400 km would have needed \"larger trials\", and the staff proposed to do without it."
  ],
  "quotes": [q("Eindringtiefe 750 - 800 km bei Verwendung eines 300 l Zusatzbehälters wird vom Führungsstab gefordert und ist ohne technische Schwierigkeiten erreichbar.",
               "A depth of 750–800 km, using a 300-litre auxiliary tank, is demanded by the operations staff and can be reached without technical difficulty.", "#/file/a1", "Covering memo, 16 April 1944, p. 1")],
  "facsimiles": [{"src": "assets/file/a1.jpg", "href": "#/file/a1", "caption": "The covering memo of 16 April 1944: \"Chef-Sache! Nur durch Offizier!\""}],
  "data": ["mistel"],
  "decision": {"key": "base", "prompt": "Where should the combinations take off?", "file": "grove",
   "options": [
    {"value": "grove", "label": "Grove, in Jutland", "detail": "775 km to Scapa Flow with the 300-litre tank. The base the file names."},
    {"value": "sola", "label": "Stavanger-Sola, in Norway", "detail": "510 km: a shorter flight and a safer way home, but the combinations must first be moved to Norway, where they can be seen."}],
   "fileNote": "The study reckons from Grove: \"775 km vom Flugplatz Grove, bei Einbau eines 300 l Kraftstoffzusatzbehälters\". Stavanger appears only as the reason why no fighter escort is possible."},
  "sources": ["t321file"]},

 {"id": "target", "n": 2, "date": "4–16 April 1944", "part": "April 1944: the plan",
  "title": "Remains Scapa Flow",
  "lede": "Gibraltar, Scapa Flow or the Soviet fleet at Leningrad. A note at the foot of the study settles it in one line.",
  "body": [
   "The staff looked for heavy warships within reach. Its naval liaison officer listed where they could be found: the Arctic near Bear Island, covering the convoys to Russia; Scapa Flow, \"main base of the English Home Fleet\"; the Clyde with its repair yards; the Mediterranean. The study named three targets as the most promising: Gibraltar, Scapa Flow and the Soviet fleet at Leningrad.",
   "Gibraltar needed the 1,400 km that the technical staff did not want to promise, and a flight over Spain, which, the study notes, the Führer had so far refused. At Leningrad no surprise was possible. A note added below the study by Christian, of the operations staff, draws the conclusion: \"bleibt Scapa Flow\", remains Scapa Flow. A greater \"material and moral effect\" was expected there.",
   "Then the arithmetic. The covering memo expects to find in Scapa \"no more than at most 2 battleships and 1–2 carriers\". Since one hit was reckoned to destroy a battleship, two Mistel against each heavy ship would do: eight in all. Of the fifteen expected, seven could be kept back for a second attack, on Scapa again or on Leningrad. The memo proposes exactly that: first 50 per cent, then decide.",
   "The estimate of what lay at anchor rested on no reconnaissance the file mentions. Chapter 7 sets it beside the Home Fleet's own war diary."
  ],
  "quotes": [q("In Scapa, das in erster Linie vorgeschlagen wird, werden nicht mehr als höchstens 2 Schlachtschiffe und 1 - 2 Träger anzutreffen sein.",
               "In Scapa, which is proposed in the first place, no more than at most 2 battleships and 1–2 carriers will be found.", "#/file/a3", "Covering memo, p. 3"),
             q("Da Gibraltar nur durch Überfliegung spanischen Gebiets - was bisher immer vom Führer abgelehnt wurde - erreicht werden kann und die Voraussetzung einer Überraschung bei Angriff auf Leningrad nicht gegeben ist, bleibt Scapa Flow.",
               "Since Gibraltar can be reached only by flying over Spanish territory, which the Führer has always refused so far, and the condition of surprise is not given in an attack on Leningrad, Scapa Flow remains.", "#/file/b3", "Study, p. 3, note signed Christian")],
  "facsimiles": [{"src": "assets/file/b3-remains.jpg", "href": "#/file/b3", "caption": "\"… bleibt Scapa Flow. Vorschlag: Vorbereitungen auf Scapa Angriff festlegen. gez. Christian\""},
                 {"src": "assets/file/a3-most.jpg", "href": "#/file/a3", "caption": "\"höchstens 2 Schlachtschiffe und 1 - 2 Träger\": the memo's estimate, and its arithmetic of eight."}],
  "plates": ["rangemap"],
  "decision": {"key": "count", "prompt": "How many combinations go against Scapa Flow?", "file": "8",
   "options": [
    {"value": "8", "label": "Eight, keep seven back", "detail": "Two against each heavy ship the memo expects; decide on the rest after the first attack."},
    {"value": "15", "label": "All fifteen at once", "detail": "The memo's option (a): everything against Scapa, nothing held back."}],
   "fileNote": "The memo proposes \"zunächst 50% (8) der Mistel gegen Scapa\", and to decide on the rest only after the first attack."},
  "sources": ["t321file"]},

 {"id": "approach", "n": 3, "date": "16 April 1944", "part": "April 1944: the plan",
  "title": "Low and late",
  "lede": "The same file gives two answers to the question how the combinations should come in, and they contradict each other.",
  "body": [
   "The study is plain about the defence. \"In the target area the strongest defence is to be expected.\" It had no exact data, because the Luftwaffe's radio intercept service reached only as far north as The Wash; its intelligence branch reckoned with 160 to 200 fighters between the Firth of Forth and the north coast of Scotland, and with a belt of radar stations covering the sea \"without gaps\". Fighter escort was impossible: Stavanger to Scapa Flow was 510 km.",
   "So the Mistel had to be seen by radar so late that the fighters could no longer reach it. The study concludes that the only possible approach is very low flight, pulling up as late as possible and gliding onto the target. Combined attacks with other bombers are ruled out, and so is a high-level approach. And: \"Flight in bad weather or at night is not possible.\"",
   "The covering memo, written the same day by the same staff, sees it differently: surprise is \"most likely\" in a night flight in the second half of a moonlit night, arriving at dawn; at any other time a low approach with a late pull-up \"already gives the enemy chances to defend\". The file does not resolve the contradiction.",
   "The technical annex gives the last two kilometres: release at 700 m, 2 km from the ship, the Ju 88 gliding at 20 degrees and 550–600 km/h, a scatter of 18 by 18 metres. A battleship should be attacked obliquely from astern."
  ],
  "quotes": [q("Schlechtwetter- oder Nachtflug ist nicht möglich.", "Flight in bad weather or at night is not possible.", "#/file/b2", "Study, p. 2"),
             q("Überraschung am ehesten bei Nachtflug in zweiter Nachthälfte einer Mondnacht mit Eintreffen am Ziel bei Morgengrauen", "Surprise is most likely in a night flight in the second half of a moonlit night, arriving at the target at dawn", "#/file/a2", "Covering memo, p. 2")],
  "facsimiles": [{"src": "assets/file/c2-attack.jpg", "href": "#/file/c2", "caption": "The method of attack: release at 700 m, 2 km from the target; scatter 18 × 18 m."},
                 {"src": "assets/file/b2-scapa.jpg", "href": "#/file/b2", "caption": "\"Im Zielgebiet ist stärkste Abwehr zu erwarten.\""}],
  "data": ["probabilities"],
  "decision": {"key": "method", "prompt": "How should the combinations come in?", "file": "day",
   "options": [
    {"value": "day", "label": "By day, at very low level", "detail": "The study's method: under the radar, pull up late, glide in. Good navigation, more exposure to fighters."},
    {"value": "dawn", "label": "By moonlight, arriving at dawn", "detail": "The covering memo's method: harder to find the anchorage, easier to surprise the defence."}],
   "fileNote": "The study: the only possible approach is very low flight with a late pull-up; night flight \"is not possible\". The covering memo prefers the moonlit night. The study's answer is marked as the file's."},
  "sources": ["t321file"]},

 {"id": "eye", "n": 4, "date": "1939 – April 1944", "part": "April 1944: the plan",
  "title": "Photographs with the ships marked",
  "lede": "A pilot skimming the sea cannot look for his target. He has to know where it lies before he takes off.",
  "body": [
   "For the way out the annex counts on the instruments: three-axis course control in the Ju 88, a homing receiver in the fighter, a radio buoy called \"Schwan\" (swan) that could be picked up 80 to 100 km away at 200 m, and the long-wave \"Sonne\" beacon at Stavanger. If all of that failed, a fast pathfinder, a Ju 188, was to lead the way.",
   "At the anchorage, instruments were no help. The study is emphatic: the attack must be preceded by reconnaissance, and the crews must be able to steer straight for their targets from aerial photographs \"on which the position of the ships is marked\". They could not pick out their targets on arrival.",
   "What the Luftwaffe had on file were target dossiers made in 1939–41: maps, aerial photographs and record cards of the batteries, tanks and airfields round the Flow. The dossier on Lamb Holm, a small island on the eastern edge of the Flow, dated January 1941, records coastal batteries \"partly still under construction\", photographed on 8 October 1940. A year later the island became the site of a prison camp (chapter 9).",
   "A reconnaissance flight would bring fresh photographs, if it came back, and could warn the defence. The file demands it all the same."
  ],
  "quotes": [q("Die Besatzungen müssen anhand von Luftbildern mit eingezeichneter Lage der Schiffe unmittelbar ihr Ziel ansteuern können.",
               "The crews must be able to steer straight for their targets from aerial photographs on which the position of the ships is marked.", "#/file/b3", "Study, p. 3")],
  "plates": ["lambholm-photo", "lyness"],
  "decision": {"key": "recon", "prompt": "Fly a reconnaissance first?", "file": "recon",
   "options": [
    {"value": "recon", "label": "Yes, photograph the anchorage first", "detail": "As the file demands. Fresh positions for the crews, if the aircraft comes back."},
    {"value": "old", "label": "No, use the old dossiers", "detail": "No warning to the defence, but the crews fly with photographs of 1939–41."}],
   "fileNote": "\"Dem Einsatz muss eine Aufklärung vorausgehen\": the operation must be preceded by reconnaissance."},
  "sources": ["t321file", "dossiers"]},

 {"id": "when", "n": 5, "date": "April – June 1944", "part": "April 1944: the plan",
  "title": "Not a surprise weapon",
  "lede": "The Allied landing in France was expected any week. The study argued against holding the Mistel back for it.",
  "body": [
   "The study proposes \"immediate use\" once the pilots were trained. If the Allies landed in force, their heavy ships would stay out of range of the German glide bombs and would not intervene directly; holding the Mistel back as a \"surprise weapon\" for that day was not expedient. And the longer the staff waited, the more time the enemy had to prepare, \"especially since complete secrecy is not assured\".",
   "The annex gives the timetable: training from 18 April on two prototypes, the other thirteen combinations ready about 15 June. Whether the file was approved, and by whom, is not in it.",
   "The choice of date mattered more than the file could know. In the Home Fleet's war diary, Scapa Flow in the second half of May 1944 held between four and seven battleships and one to three fleet carriers on any one day; by the second half of June, after the carriers Victorious and Indomitable had sailed for the Far East and other ships had gone south for the landing, it held two battleships and one carrier: what the memo had expected.",
   "Later accounts, all secondary, say that the Mistel were first used in June 1944 against shipping off the Normandy coast. No document found for this study confirms it, and the study does not follow that branch."
  ],
  "quotes": [q("Je länger mit dem Einsatz gezögert wird, desto mehr Zeit bleibt dem Feind Abwehrmassnahmen zu treffen, insbesondere da eine unbedingte Geheimhaltung nicht gewährleistet ist.",
               "The longer the operation is delayed, the more time the enemy has to take countermeasures, especially since complete secrecy is not assured.", "#/file/b1", "Study, p. 1")],
  "data": ["fleet"],
  "decision": {"key": "when", "prompt": "When should the attack be made?", "file": "june",
   "options": [
    {"value": "may", "label": "At once, in late May, with what is ready", "detail": "Perhaps nine combinations; the anchorage full of heavy ships."},
    {"value": "june", "label": "After 15 June, with all fifteen", "detail": "The file's schedule; by then much of the fleet has sailed."},
    {"value": "hold", "label": "Hold them back for the landing", "detail": "Against the study's advice. Scapa Flow is not attacked in 1944."}],
   "fileNote": "The study proposes immediate use after training; the annex expects the last combinations about 15 June."},
  "sources": ["t321file", "nhn", "roskill3"]},

 {"id": "drachen", "n": 6, "date": "November 1944 – 16 February 1945", "part": "February 1945: the decision",
  "title": "Dragon's Lair",
  "lede": "Ten months later the plan came back, under a new name, in a Luftwaffe that no longer had the fuel to fly it.",
  "body": [
   "In November 1944 Major Horst Hans Beeger joined the staff of KG 200, the Luftwaffe's special-operations wing under Oberstleutnant Werner Baumbach. Interrogated by the British in the winter of 1945–46, he said that in January 1945 he prepared \"an operation planned against SCAPA FLOW\" at Schloss Boitzenburg near Prenzlau, and in February went to Tirstrup in Jutland \"to direct the operation\". The interrogator added that the prisoner \"has not impressed IO\", but might be speaking the truth.",
   "The war diary of the operations staff gives the decisions. On 2 February 1945 Göring agreed that beyond the 130 Mistel built or under construction no further hundred were to be built. On 12 February, after a report by the commodore of KG 200, he put off the final decision on \"Unternehmen Drachenhöhle\", Operation Dragon's Lair, for three days; Operation Eisenhammer, the Mistel attack on the power stations round Moscow, was to go ahead \"under all circumstances\". On 13 February Dragon's Lair was \"postponed for the time being\". On 16 February Göring decided that it was \"not to be carried out for the time being\"; the fuel set aside for it, stored in Norway, remained blocked.",
   "The diary does not name the target of Dragon's Lair. That it was Scapa Flow follows from Beeger's statement and from the later literature. Nor does it say why. On the same days it records a fuel crisis: about 400 tons of aviation fuel were expected from industry for the whole of February. Beeger said bad weather made them abandon the project. A later account, based on a German pilot's memory and a post-war letter, adds an RAF attack on Tirstrup on 14 February and the suspicion that Baumbach warned the British; no document found for this study confirms either.",
   "Tirstrup lies about 865 km from Scapa Flow: beyond the 750–800 km of the Mistel of 1944, within the 1,500 km of the combinations being built in 1945, as the Eisenhammer file of 7 February 1945 puts it."
  ],
  "quotes": [q("Nach Vortrag Kommodore KG 200 hat Reichsmarschall den endgültigen Entscheid über Durchführung des Unternehmens \"Drachenhöhle\" noch auf 3 Tage verschoben.",
               "After a report by the commodore of KG 200, the Reichsmarschall has put off the final decision on carrying out Operation \"Drachenhöhle\" for another three days.", "#/file/k2", "War diary, 12 February 1945"),
             q("Reichsmarschall hat nunmehr entschieden, daß das Unternehmen \"Drachenhöhle\" vorerst nicht mehr durchzuführen ist.",
               "The Reichsmarschall has now decided that Operation \"Drachenhöhle\" is not to be carried out for the time being.", "#/file/k5", "War diary, 16 February 1945")],
  "facsimiles": [{"src": "assets/file/k2-drachen.jpg", "href": "#/file/k2", "caption": "12 February 1945: the decision on \"Drachenhöhle\" put off for three days."},
                 {"src": "assets/file/v2-beeger.jpg", "href": "#/file/v2", "caption": "Beeger's interrogation: \"Bad weather made them abandon this project.\""}],
  "data": ["map"],
  "decision": {"key": "drachen", "prompt": "February 1945: attack Scapa Flow?", "file": "postpone",
   "options": [
    {"value": "attack", "label": "Fly Dragon's Lair", "detail": "From Tirstrup, on the first day the weather allows, with the fuel stored in Norway."},
    {"value": "postpone", "label": "Postpone it", "detail": "As Göring decided on 13 and 16 February: the fuel goes to Eisenhammer."}],
   "fileNote": "The war diary: postponed on 13 February, not to be carried out on 16 February 1945."},
  "sources": ["t321ktb", "csdic", "ironhammer", "forsyth"]},

 {"id": "fleet", "n": 7, "date": "1939 – May 1945", "part": "The other side",
  "title": "What lay at anchor",
  "lede": "The Home Fleet kept a diary of where every ship was on every day. It answers the question the file could only estimate.",
  "body": [
   "Scapa Flow, a natural harbour enclosed by the Orkney islands, was the main base of the British Home Fleet in both world wars. In April 1944 it was full: on the day the study was signed, the battleships Duke of York, Rodney and Ramillies lay there; Anson, the carriers Furious and Victorious and others came and went between operations off Norway, refits in Rosyth, Liverpool and Plymouth, and exercises in the Clyde.",
   "The fleet was about to shrink. Roskill's official history records that the fleet carriers Victorious and Indomitable sailed for the Far East on 12 June 1944 and the battleship Howe on 1 July; from July the Duke of York was the only modern battleship left to the Commander-in-Chief. By early 1945, Roskill writes, \"he had no more than one battleship\". In the war diary that ship is the Rodney, the fleet's flagship at Scapa for most of the time from October 1944 until she left on 22 May 1945. In February 1945, when Göring decided on Dragon's Lair, she was the only battleship in the Flow.",
   "The defences had grown since 1939, when, by Roskill's account, there were \"still only eight heavy A.A. guns at Scapa\", placed to defend the oil tanks, with one squadron of naval fighters and a single line of nets across the main entrances. A balloon barrage was formed in February 1940, and fighters were based on the islands. How strong the anti-aircraft defence still was in 1944–45 has not been found in a public-domain source; the study's model assumes, and says so.",
   "Whether British intelligence knew of Dragon's Lair is not settled by any source read here: an Air Ministry file titled \"Mistel: German intentions\" (February–March 1945) has not been seen. The fleet knew of the U-boats: in December 1944 several lay off the Orkneys to catch the carriers, and one, U-312, damaged herself trying to enter the Flow through Hoxa Sound. \"None of the U-boats … ever sighted any of the aircraft carriers they had been sent to catch.\""
  ],
  "quotes": [q("The strength generally available to Admiral Moore was, by earlier standards, small; for he had no more than one battleship, seven cruisers or anti-aircraft cruisers and four flotillas of destroyers", "", "#/sources", "Roskill, The War at Sea, vol. III part 2 (1961), on early 1945")],
  "plates": ["chart35", "wasp", "boom"],
  "data": ["fleet"],
  "sources": ["nhn", "roskill1", "roskill3", "roof"]},

 {"id": "barriers", "n": 8, "date": "October 1939 – May 1945", "part": "What the file does not count",
  "title": "The barriers",
  "lede": "The eastern entrances to the Flow were closed with stone and concrete after a U-boat had come through them and sunk a battleship.",
  "body": [
   "In the night of 13–14 October 1939 the German submarine U-47 slipped into Scapa Flow through Kirk Sound, one of the shallow eastern channels between the islands, past the old blockships sunk there to close it, and torpedoed the battleship Royal Oak. \"Twenty-four officers and 809 men of her complement perished\", Roskill writes: 833 men. Churchill told the House of Commons that \"the last blockship required reached Scapa Flow only on the day after the disaster had occurred\".",
   "The Admiralty decided to close the eastern entrances for good with causeways of rock and concrete blocks, linking the islands from Mainland by Lamb Holm and Burray to South Ronaldsay. They are known as the Churchill Barriers. Preparatory work began in 1940 (accounts differ on when the main building started); by the end of 1942 the barriers were proof against submarines; the first was complete in August 1943, all four by September 1944. They were opened as roads on 12 May 1945.",
   "Among the workers were about 520 British labourers and, from January 1942, Italian prisoners of war. Ten men died in accidents on the works, seven of them drowned. Chapter 9 follows the prisoners.",
   "In the Luftwaffe's target dossiers Lamb Holm appears in January 1941 as \"fortifications\": coastal batteries guarding Holm Sound. The planners of 1944 needed photographs of the anchorage, not of the barriers. But a heavy ship hit in the Flow, by the measure of the Royal Oak, meant hundreds of men."
  ],
  "quotes": [q("Twenty-four officers and 809 men of her complement perished.", "", "#/sources", "Roskill, The War at Sea, vol. I (1954), p. 74")],
  "plates": ["royaloak", "lambholm-map", "blockship", "barrier"],
  "sources": ["roskill1", "hansard", "custodis", "dossiers"]},

 {"id": "prisoners", "n": 9, "date": "January 1942 – December 1945", "part": "What the file does not count",
  "title": "The prisoners of Lamb Holm and Burray",
  "lede": "About twelve hundred Italian prisoners of war built the barriers. They argued that they should not have had to.",
  "body": [
   "The first Italian prisoners reached Orkney in January 1942 and were put into two camps on the islands they were to join: Camp 34 on Burray and Camp 60 on Lamb Holm. A Red Cross inspection in August 1942 counted 1,170 men, 267 of them in tents; the camps were a third over capacity. At the peak, in 1943, about 1,200 Italians worked on the barriers beside some 520 British workmen.",
   "In March 1942 both camps stopped work. The Geneva Convention of 1929 forbade using prisoners of war on work connected with the operations of the war, and on dangerous work; the prisoners said that closing the eastern entrances of a fleet base was both. The Swiss protecting power and the International Committee of the Red Cross accepted the British view that the work was allowed, and the camp leaders were removed. From then on the official papers called the barriers \"causeways\": roads between the islands. The historian Johann Custodis, who has studied the files, concludes that the British broke the Convention, and that housing prisoners next to a likely bombing target did so too.",
   "Of the ten men killed on the works, two were Italians, according to an Orkney history cited by Custodis. Most of the prisoners left for a camp at Skipton in September 1944; 420 were still on Burray in November 1945; the last had gone by mid-December 1945. On Lamb Holm a few of them stayed into 1945 to finish converting a Nissen hut into a chapel, painted inside by Domenico Chiocchetti. It is the only building of Camp 60 still standing.",
   "In June 1944, when the file's fifteen Mistel were due, the camps were still occupied."
  ],
  "plates": ["chapel"],
  "sources": ["custodis", "hes"]},

 {"id": "end", "n": 10, "date": "June 1944 – May 1945", "part": "The end",
  "title": "The end of the plan",
  "lede": "No Mistel ever attacked Scapa Flow. The file survived the war; the reasons for its failure have to be pieced together.",
  "body": [
   "Whether anyone decided on the study of April 1944 is not in the file. The later literature, not confirmed here from documents, says the Mistel unit was sent to France after the landing. The war diary of February 1945 shows Dragon's Lair once more, in three entries, between a fuel crisis and the higher priority of Eisenhammer; Beeger remembered the weather. Each source gives a reason that suits it, and none of them gives the full one.",
   "In May 1945 the Home Fleet dispersed. The barriers were opened as roads on 12 May 1945; the Rodney left Scapa Flow for Rosyth on 22 May. The censorship of letters from Orkney was still in force in March 1945 \"as an essential measure of operational security\"; Orkney remained a restricted area after Shetland had been released in June 1945. The Italian prisoners went home by the end of the year.",
   "The accounting at the end of this study sets the file's arithmetic beside the war diary of the Home Fleet and runs the plan you chose. It counts ships, because that is what the file counts. The reflection says what it does not."
  ],
  "facsimiles": [{"src": "assets/file/k5-abandon.jpg", "href": "#/file/k5", "caption": "16 February 1945: \"Drachenhöhle\" not to be carried out \"for the time being\"; the fuel in Norway stays blocked."}],
  "sources": ["t321file", "t321ktb", "csdic", "nhn", "hansard", "custodis"]},
]

SOURCES = {
 "t321file": {"short": "The Mistel study, 16 April 1944 (NARA T-321, roll 10)", "cite": "National Archives and Records Administration (NARA), Record Group 242, microfilm T-321 (Records of Headquarters, German Air Force High Command), roll 10, item OKL 2382: war diary of the Luftwaffe Operations Staff, annex volume C (Chefsachen), no. 89: covering memo Ia no. 9532/44, study, technical annex, naval note and maps, 16 April 1944, images 282–298. Transcribed and translated here in full.", "url": "https://catalog.archives.gov/id/315968627", "status": "Captured German official records; NARA: unrestricted. Read at the page images.", "read": "checked"},
 "t321ktb": {"short": "War diary of the operations staff, February 1945 (NARA T-321, roll 10)", "cite": "NARA, RG 242, T-321, roll 10, item OKL 2593: war diary of the Luftwaffe Operations Staff Ia, text volume, February 1945, entries of 2, 12, 13 and 16 February (images 368, 418–419, 425, 441).", "url": "https://catalog.archives.gov/id/315968627", "status": "Captured German official records; NARA: unrestricted. Read at the page images; dates assigned by the sequence of day headings.", "read": "checked"},
 "csdic": {"short": "Interrogation of Maj. Horst Hans Beeger (CSDIC, 1945–46)", "cite": "CSDIC (WEA) BAOR, Final Report FR 30, \"Maj Horst Hans Beeger\", 21 January 1946, and Preliminary Interrogation Report 71, 13 December 1945; NARA, Record Group 498, HQ ETOUSA, MIS Prisoner of War Interrogation Section.", "url": "https://catalog.archives.gov/id/295816244", "status": "Reports of the British and US armies; declassified 1979. The final report read at the page images; the preliminary report only through the catalogue's text recognition.", "read": "checked"},
 "nhn": {"short": "War diary of the Commander-in-Chief, Home Fleet, 1944–45", "cite": "Admiralty war diaries (The National Archives, Kew, ADM 199), war diary of the Commander-in-Chief, Home Fleet, April 1944 – May 1945, as transcribed by Don Kindell for naval-history.net (Home Fleet pages 1944–45).", "url": "https://www.naval-history.net/xDKWD-HF1944b.htm", "status": "The original is an unpublished Crown record; the transcription is modern. Used here as data on ship movements, not quoted; to be checked against the original before any print use.", "read": "research"},
 "roskill1": {"short": "Roskill, The War at Sea, vol. I (1954)", "cite": "S. W. Roskill, The War at Sea 1939–1945, vol. I: The Defensive (London: HMSO, 1954), pp. 74, 79–81.", "url": "https://archive.org/details/worldat-sea-1939-1945-vol-1", "status": "Published Crown copyright, expired; public domain. Quotations checked in the text.", "read": "checked"},
 "roskill3": {"short": "Roskill, The War at Sea, vol. III part 2 (1961)", "cite": "S. W. Roskill, The War at Sea 1939–1945, vol. III: The Offensive, part 2 (London: HMSO, 1961), pp. 156, 164, 251, 260.", "url": "https://archive.org/details/war-at-sea-1939-1945-vol-3-part-2", "status": "Published Crown copyright, expired; public domain. Quotations checked in the text.", "read": "checked"},
 "roof": {"short": "Roof over Britain (HMSO, 1943)", "cite": "Ministry of Information, Roof over Britain: the official story of the A.A. defences, 1939–1942 (London: HMSO, 1943), p. 77.", "url": "https://archive.org/details/roofoverbritain", "status": "Published Crown copyright, expired; public domain.", "read": "checked"},
 "hansard": {"short": "Hansard, House of Commons, 1939–1945", "cite": "House of Commons debates, 17 October 1939 (vol. 352, cc. 686–690) and 8 November 1939 (vol. 353, c. 253); written answers 7 March 1945 (vol. 408, c. 2029W) and 6 June 1945 (vol. 411, c. 901W).", "url": "https://api.parliament.uk/historic-hansard/", "status": "Parliamentary copyright, Open Parliament Licence. Quotations checked in the text.", "read": "checked"},
 "custodis": {"short": "Custodis, \"Exploiting the Enemy in the Orkneys\" (2011)", "cite": "Johann Custodis, \"Exploiting the Enemy in the Orkneys: Italian Prisoners of War and the Churchill Barriers, 1942–1945\", Journal of Scottish Historical Studies 31.1 (2011), pp. 72–98, doi:10.3366/jshs.2011.0007; based on The National Archives ADM 116/5790, ADM 116/4111, WO 32/10740, FO 916/308 and ICRC camp reports.", "url": "https://doi.org/10.3366/jshs.2011.0007", "status": "Modern scholarship in copyright: summarised and cited, not reproduced.", "read": "research"},
 "hes": {"short": "Historic Environment Scotland, Italian Chapel (listing LB12728)", "cite": "Historic Environment Scotland, listed building record LB12728: Lamb Holm, Italian Chapel, category A.", "url": "https://portal.historicenvironment.scot/designation/LB12728", "status": "Modern record in copyright: summarised.", "read": "research"},
 "dossiers": {"short": "German target dossiers, Orkney, 1939–41 (NARA)", "cite": "Luftwaffe target dossiers \"Lamb-Holm (Scapa Flow), Befestigungsanlagen\", GB 16 800, January 1941, and \"Scapa Flow SW\", GB 111, 1939; NARA, Target Dossiers Pertaining to the British Isles, 1938–1945 (NAIDs 259486587, 259486853), via Wikimedia Commons.", "url": "https://catalog.archives.gov/id/259486587", "status": "Captured German records; public domain in the US.", "read": "checked"},
 "ironhammer": {"short": "The Eisenhammer file, 7 February 1945 (NARA T-971)", "cite": "NARA, RG 242, T-971, roll 22, item 4406/72, memo of the Chief of the Luftwaffe Operations Staff, 7 February 1945: Mistel with a penetration depth of 1,500 km in construction. See the study Iron Hammer, 1945.", "url": "https://iron-hammer-1945.netlify.app/", "status": "Captured German official records; read at the page images for Iron Hammer, 1945.", "read": "checked"},
 "forsyth": {"short": "Forsyth and later accounts (modern)", "cite": "Robert Forsyth, Mistel (2001) and Luftwaffe Mistel Composite Bomber Units (2015), as reported in the press; a Danish local history of Tirstrup and Taars, February 1945 (Kystmuseet). Not seen in full.", "url": "", "status": "Modern literature in copyright: referred to only, and marked as such where used.", "read": "referred"},
}

PLATES = {"credit": "Plates: a map from the file (NARA), German target dossiers captured by the Allies (NARA, public domain), a British Admiralty chart and photographs of the Royal Navy and the US Navy whose copyright has expired, and three recent photographs under Creative Commons licences; each is named with its original. Resized.",
 "plates": [
  {"id": "rangemap", "titel": "Range of the Mistel, April 1944", "caption": "Annex 3 to the study: \"Tactical penetration depth for Beethoven 'Mistel'\", with arcs of 400 km (without tank) and 750 km (with the 300-litre tank) round the jump-off airfields from Banak in the far north to Rennes, among them Sola (3) and Grove (4). On the film the black and red arcs cannot be told apart.", "source": "NARA, RG 242, T-321, roll 10, image 298 (https://catalog.archives.gov/id/315968627)"},
  {"id": "lambholm-photo", "titel": "Lamb Holm as a German target, 1941", "caption": "Luftwaffe target dossier \"Lamb-Holm (Scapa Flow), Befestigungsanlagen\", GB 16 800 bc, January 1941, from an aerial photograph of 8 October 1940: two coastal batteries and huts at the entrance of Holm Sound. A year later Camp 60 for Italian prisoners was built on the island.", "source": "NARA via Wikimedia Commons, File:Target Dossier for Lamb-Holm, Orkney, Scotland - DPLA - 38b945587612b0a58b8761354d0c156c (page 2).jpg (public domain)"},
  {"id": "lambholm-map", "titel": "Holm Sound on a German target map, 1941", "caption": "The map sheet of the same dossier (GB 16 800 a, 1:100,000): the eastern entrances of Scapa Flow between Mainland, Lamb Holm, Burray and South Ronaldsay, which the Churchill Barriers were to close.", "source": "NARA via Wikimedia Commons, File:Target Dossier for Lamb-Holm, Orkney, Scotland - DPLA - 38b945587612b0a58b8761354d0c156c (page 1).jpg (public domain)"},
  {"id": "lyness", "titel": "Lyness, a German target, 1939", "caption": "Luftwaffe target dossier \"Lyness (Scapa Flow)\", GB 111 bc: aerial photograph of the naval base and oil tanks on Hoy with an anti-aircraft battery, the kind of photograph the crews of 1944 were to fly with if no new reconnaissance came back.", "source": "NARA via Wikimedia Commons, File:Target Dossier for Scapa Flow SW, Orkney, Scotland - DPLA - b8d8aa3675753153e8eed763560d7794 (page 2).jpg (public domain)"},
  {"id": "chart35", "titel": "Admiralty chart of Scapa Flow, 1944", "caption": "Admiralty chart no. 35, Scapa Flow, northern part, published 1944 (surveys of 1906–09 with later corrections).", "source": "United Kingdom Hydrographic Office; National Library of Scotland, via Wikimedia Commons, File:Admiralty Chart No 35 Scapa Flow Northern Part, Published 1944.jpg (public domain)"},
  {"id": "wasp", "titel": "Scapa Flow, April 1942", "caption": "The US heavy cruiser Wichita at anchor in Scapa Flow, with the carrier Wasp behind her, in April 1942, when American ships reinforced the Home Fleet.", "source": "US Navy photograph NH 97884, Naval History and Heritage Command, via Wikimedia Commons (public domain)"},
  {"id": "boom", "titel": "The boom, May 1943", "caption": "Boom defence vessels towing an anti-submarine net into position at Scapa Flow, May 1943. Photograph by J. A. Hampton, Royal Navy, IWM A 16572.", "source": "Imperial War Museums, via Wikimedia Commons, File:Royal Navy Vessels Maintain the Boom Defence at Scapa Flow, Scotland, May 1943 A16572.jpg (Crown copyright expired)"},
  {"id": "royaloak", "titel": "HMS Royal Oak, 1937", "caption": "The battleship Royal Oak, sunk inside Scapa Flow by U-47 on 14 October 1939 with the loss of 833 men.", "source": "Royal Navy photograph, via Wikimedia Commons, File:HMS Royal Oak (08).jpg (Crown copyright expired)"},
  {"id": "blockship", "titel": "A blockship at Barrier No. 4", "caption": "The hull of one of the old ships sunk to close the eastern channels, beside Churchill Barrier No. 4 between Burray and South Ronaldsay, photographed in 1988.", "source": "Harald Kucharek, geograph.org.uk, via Wikimedia Commons, File:Blockship at Churchill Barrier No 4 - geograph.org.uk - 1331240.jpg (CC BY-SA 2.0)"},
  {"id": "barrier", "titel": "Churchill Barrier No. 4", "caption": "The fourth barrier, from Burray towards South Ronaldsay, in 2006: now a road.", "source": "Lis Burke, geograph.org.uk, via Wikimedia Commons, File:Churchill Barrier 4 South Ronaldsay.jpg (CC BY-SA 2.0)"},
  {"id": "chapel", "titel": "The Italian Chapel, Lamb Holm", "caption": "The chapel of the Italian prisoners of Camp 60, converted from a Nissen hut, in 2008. Its painted interior, by Domenico Chiocchetti, is not shown here: the paintings are still in copyright.", "source": "John Haslam, via Wikimedia Commons, File:The Italian Chapel, Orkney (Exterior) (2926632589).jpg (CC BY 2.0)"},
 ]}

(ROOT / "data" / "study.json").write_text(json.dumps({"chapters": CH}, ensure_ascii=False, indent=1), encoding="utf-8")
(ROOT / "data" / "sources.json").write_text(json.dumps(SOURCES, ensure_ascii=False, indent=1), encoding="utf-8")
(ROOT / "data" / "plates.json").write_text(json.dumps(PLATES, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(CH), "chapters,", len(SOURCES), "sources,", len(PLATES["plates"]), "plates")
