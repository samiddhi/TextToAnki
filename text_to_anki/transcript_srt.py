import re
from datetime import datetime, timedelta

def parse_transcript(transcript: str) -> list[tuple[str, str]]:
    """
    Parse the transcript to extract timestamps and text.

    :param transcript: The input transcript string.
    :return: A list of tuples containing start time, end time, and text.
    """
    lines = transcript.strip().split('\n')
    parsed_lines = []
    for i in range(len(lines)):
        # Match the format "00:15 - text"
        match = re.match(r"(\d{2}:\d{2}) - (.+)", lines[i])
        if match:
            start_time = match.group(1)
            text = match.group(2)
            end_time = calculate_end_time(start_time, i, lines)
            parsed_lines.append((start_time, end_time, text))
    return parsed_lines

def calculate_end_time(start_time: str, index: int, lines: list[str]) -> str:
    """
    Calculate the end time for a subtitle.

    :param start_time: The start time of the current subtitle.
    :param index: The index of the current subtitle.
    :param lines: The list of all transcript lines.
    :return: The end time for the current subtitle.
    """
    next_start_time = None
    if index + 1 < len(lines):
        next_match = re.match(r"(\d{2}:\d{2}) - .+", lines[index + 1])
        if next_match:
            next_start_time = next_match.group(1)
    
    if next_start_time:
        end_time = next_start_time
    else:
        # If it's the last subtitle, assume it lasts for 2 seconds.
        start_dt = datetime.strptime(start_time, "%M:%S")
        end_dt = start_dt + timedelta(seconds=2)
        end_time = end_dt.strftime("%M:%S")
    
    return end_time

def format_time_srt(time_str: str) -> str:
    """
    Format the time string to SRT format.

    :param time_str: The input time string in "MM:SS" format.
    :return: The formatted time string in "HH:MM:SS,mmm" format.
    """
    dt = datetime.strptime(time_str, "%M:%S")
    return dt.strftime("00:%M:%S,000")

def convert_to_srt(transcript: str) -> str:
    """
    Convert the transcript to SRT format.

    :param transcript: The input transcript string.
    :return: The formatted SRT string.
    """
    parsed_lines = parse_transcript(transcript)
    srt_lines = []
    for i, (start_time, end_time, text) in enumerate(parsed_lines):
        srt_lines.append(f"{i + 1}")
        srt_lines.append(f"{format_time_srt(start_time)} --> {format_time_srt(end_time)}")
        srt_lines.append(text)
        srt_lines.append("")
    return "\n".join(srt_lines)

def main(transcript):
    # Example usage
    srt_output = convert_to_srt(transcript)
    with open("output.srt", "w", encoding="utf-8") as file:
        file.write(srt_output)

    return srt_output

if __name__ == "__main__":
    vrt="""
        00:15 - Dejansko lahko rečemo, da je Triglavski narodni park
00:17 - nek izjemen preplet kulturne krajine in pa ohranjanja narave.
00:25 - Mislimo predvsem na področja nad gornjo gozdno mejo,
00:27 - se pravi visokogorje, kjer človekov vpliv v zadnjih stoletjih ni bil
00:31 - tako intenziven.
00:38 - Na območju gozda in pa v alpskih dolinah pa je seveda človekova
00:41 - dejavnost tista, ki je oblikovala tudi trenutno stanje
00:44 - naravnega okolja.
00:51 - In zagotovo so vse dejavnosti, ki so prepoznane kot sprejemljive
00:58 - na področju ohranjanja narave, tudi tiste, pri katerih moramo najti
01:02 - neko srednjo pot. Naša vloga kot upravljavca narodnega parka
01:07 - je predvsem uskladiti različne težnje po rabah prostora,
01:11 - tako socialne, ekološke kot seveda tudi ekonomske vloge
01:15 - tega območja.
01:31 - Zagotovo prve resne ideje o zavarovanju tega edinstvenega
01:36 - gorskega sveta segajo že v začetek 20. stoletja.
01:44 - Seveda, pravi korak je bil storjen leta 1924 z ustanovitvijo
01:49 - Alpskega varstvenega parka, se pravi s podpisom pogodbe,
01:53 - kjer se je prvič zavarovala dolina Triglavskih jezer,
01:57 - z letom '61 pa se je potem tudi prvič pojavilo ime Triglavski
02:02 - narodni park kot zavarovano območje. Današnja velikost pa seveda
02:07 - sega v leto '81 z ustanovitvijo tega velikega triglavskega
02:12 - narodnega parka, kjer se je z letom 2010 samo še košček,
02:16 - za nekaj deset hektarov, povečala površina.
02:45 - Če so bili v preteklosti izzivi predvsem na področju neposredne
02:49 - rabe naravnih virov, kot je recimo gozdarstvo, kmetijstvo, je danes
02:53 - poudarek na uravnavanju splošne rabe, to pomeni pa področja
02:57 - obiskovanja in izvajanja turističnih aktivnosti, rekreacijskih aktivnosti
03:01 - v tem prostoru. Ta socialna vloga prostora Triglavskega narodnega
03:06 - parka je namreč izjemno poudarjena in ta pritisk se
03:10 - iz leta v leto samo povečuje.
03:17 - Predvsem v preteklosti je bilo to povezano s problematiko odpadkov,
03:22 - potem nepravilnega parkiranja oziroma parkiranja v naravnem
03:26 - okolju, predvsem v zadnjem obdobju pa poudarjamo velike posledice
03:33 - na živali oziroma na tiste živalske vrste, ki so občutljive
03:38 - na vznemirjanje,
03:41 - kot so denimo rastišča divjega petelina ruševca,
03:46 - potem tudi občutljivost barjanskih, visokobarjanskih površin
03:49 - na prisotnost človeka oziroma na kakršno koli obliko rabe.
04:29 - Vpliv človeka se najbolj kaže z njegovo stalno prisotnostjo,
04:33 - se pravi povsod smo razpršeni in zmanjkuje nam mirnih kotičkov,
04:37 - različne dejavnosti so povsod in treba se je zavedati,
04:41 - da žival splaši prvi človek zjutraj in če za njim pride še sto ljudi
04:46 - ali pa nobeden, je ona splašena. In tukaj lahko res veliko naredimo,
04:53 - da tiste mirne predele prepustimo še naprej njim.
05:08 - Belka je res fenomenalno prilagojena na življenje v visokogorju.
05:12 - V bistvu je pozimi že višje kot poleti. Tukaj praktično ona edina
05:17 - kljubuje tem zimskim razmeram, kjer najde hrano na plaziščih,
05:22 - potem spomladi začne pa ona iskati mesta, ki so boljša
05:27 - za gnezdenje, se pravi bolj ravna, več travišč, predvsem z vidika tega,
05:32 - da bodo tam lahko odraščali mladiči, ampak še vedno so pa to višine
05:36 - nad tisoč. Mi imamo naše Alpe strme na vrhu in zaradi tega je
05:41 - teh območij malo in zelo pomembno je, da so ta območja mirna.
05:56 - Belka se pa sooča še z enim problemom.
06:00 - Ona začne gnezditi junija, ko so hribi popolnoma mirni,
06:04 - mladiči se izvalijo potem julija in zaradi tega lahko locira gnezda
06:09 - nekje, kjer bo kasneje, ko se bo zgodil naval s koncem šole,
06:15 - postal problem za gnezdenje. Zaradi tega se nam lahko zgodi,
06:19 - da gnezdo leži na obljudeni poti in potem tik preden se izvalijo
06:23 - mladiči, propade.
06:30 - Zelo pomembno je, da poznamo vse njihove kotičke, vsa njihova
06:35 - gibanja, zato smo se lotili telemetrije. Telemetrija nam
06:39 - v bistvu pokaže ne samo mesta, kjer gnezdi, ampak mesta,
06:43 - kjer se giblje pozimi, kjer se giblje jeseni, sploh v času,
06:48 - ko je težje zaznavna. In telemetrija je lepo pokazala navezanost
06:54 - na gnezdišče. Presenetilo nas je, kako je res celo leto visoko,
06:59 - nikoli ne gre v dolino zaradi ostre zime, bi rekel,
07:03 - in ogromno smo se naučili in ta način jo bomo
07:08 - bistveno lažje varovali.
07:13 - In tukaj pri belki se zelo lepo vidijo cilji projekta. Se pravi,
07:16 - po eni strani si želimo vrsto ohraniti tukaj, po drugi strani
07:21 - se moramo pa naučiti sobivati z njo, če hočemo vrsto
07:24 - dolgoročno ohraniti.
07:31 - Zelo pomembo je naravo spoznavati. Spodbujam to
07:36 - in vedno je dobro. Če hočemo naravo razumeti, rabimo izkušnjo,
07:41 - če hočemo do nje gojiti neka čustva, rabimo izkušnjo. In več kot imamo
07:46 - teh izkušenj, lažje nam bo uspelo. In zato sem jaz prepričan,
07:51 - da bo tukaj najlažje s tistimi povratniki, ki so vsak dan tukaj.
07:57 - Tisti bodo mirne cone zelo spoštovali. Verjetno bo najtežje
08:02 - z nekom, ki pride na vsakih deset let v to krajino, tudi taki so
08:07 - številčni, ampak s to izkušnjo jaz mislim, da nam bo uspelo.
08:22 - Triglavski narodni park kot tak je prostor, v katerega naj
08:25 - prireditve ne bi sodile, čeprav vsi vemo, da imamo tudi
08:28 - množične prireditve, kot so biatlon, Planica in tako naprej.
08:32 - Tako da mi se mu kot organizatorji športnih prireditev v tem prostoru
08:35 - poskušamo izogibati čim bolj, poskušamo iti nekako na meje
08:39 - tega prostora, s tem da je pa včasih nemogoče narediti,
08:44 - speljati tekmovanje, da je zanimivo, da se ga ne bi vsaj dotaknili
08:47 - oziroma prečili. In tukaj mi iščemo konstanten dialog med nami
08:51 - in Triglavskim narodnim parkom, da poskušamo nekatere stvari,
08:55 - ki so smiselne, potem tam tudi izpeljati.
09:02 - Vsi vemo, da ljudje, ki bodo hodili v predprostor tega prostora,
09:07 - bodo isto vstopali v ta prostor. Tako da je za nas zelo pomembno,
09:10 - da razmišljamo, katere tujce vabimo, kdo so tisti ljudje, ki bodo prišli
09:14 - v ta prostor. In če mi vemo, da ta prostor ne prenese nekega
09:18 - množičnega turizma in si želimo ljudi, ki imajo odnos do narave,
09:22 - potem je na nas kot organizatorjih potovanj ali pa prireditev
09:26 - konec koncev, da vabimo take ljudi, ki bodo imeli nek zdrav odnos
09:29 - do narave, jo spoštovali in se nekako pravilno gibali
09:32 - v tem prostoru. Zame je najpomembnejše vprašanje,
09:36 - na katerega si moramo odgovoriti in katerega moramo najprej
09:40 - imeti v mislih, je ljudje v Triglavskem narodnem parku,
09:43 - kakršno koli dejavnost imajo. Se pravi, oni morajo o tem,
09:46 - morajo imeti možnost tukaj preživeti in tudi normalno živeti.
09:54 - To bi bil prostor srečnih ljudi, od koder se ljudje ne bi
09:57 - odseljevali. Manko teh ljudi se pač občuti. Kdo so potem
10:03 - tvoji sogovorniki, kdo so tisti, ki ta prostor ustvarjajo?
10:08 - Midva se zavedava, da čeprav živiva od turizma,
10:12 - je prva in najpomembnejša narava in pa ohranjanje tega okolja.
10:15 - In če so naši predniki lahko to ohranili za nas, zato da lahko
10:18 - mi to pokažemo obiskovalcem, da mi v tem uživamo in tukaj živimo,
10:22 - je "number one", če lahko temu tako rečemo, to, da mi na nek način
10:25 - zaščitimo oziroma ohranimo naravo tudi za prihodnje generacije.
10:35 - Seveda turizem prinaša ogromno pozitivnih učinkov,
10:38 - pa tudi kakšnega negativnega. In tukaj je na vseh nas,
10:41 - da z nekimi pametnimi pristopi, ukrepi in pa res s tistim
10:46 - zavedanjem, da ne bomo ničesar nesli s sabo v grob, da nekako
10:49 - poskušamo razdeliti, razpršiti ali pa razporediti te naše
10:53 - obiskovalce in pa tudi našo ponudbo čez celo sezono,
10:56 - če je mogoče.
11:11 - Mi tudi opozarjamo naše obiskovalce, da vse ni dostopno
11:17 - in samo zaradi nas tam. Imamo kanjone, imamo reke,
11:22 - imamo potoke, imamo jezera, kjer kopanje ni dovoljeno.
11:25 - In če se domačini ne kopajo in če se naši otroci ne kopajo,
11:29 - morajo tudi tuji razumeti, da se pač v teh zadevah ne bodo mogli.
11:34 - Ker posledično človek že vpliva na te drobne ekosisteme
11:38 - in jaz si ne bi mogel odpustiti, da bi se ta naša narava
11:42 - kdaj spremenila.
11:48 - Včasih je tudi tako, da mogoče omejitev na prvo žogo izgleda
11:52 - res kot neka omejitev, pa je v resnici lahko tudi rešitev.
11:56 - Tako da, če se bomo pogovarjali pa z iskrenimi kartami drug
12:00 - do drugega prišli, jaz mislim, da lahko najdemo nekaj,
12:04 - kar je "win-win" situacija za vse vključene.
12:15 - Domačini, ki že praktično od rojstva živimo v Bohinju,
12:18 - mogoče ne prepoznamo lepote Bohinja, kot jo prepozna
12:22 - nekdo drug, ki sem pride pogledat Bohinj, je pa velik plus tega,
12:28 - da živimo v Bohinju, da imamo praktično veliko aktivnosti
12:32 - pred hišnim pragom. Sam sem del folklore praktično že od malih nog
12:38 - in takrat smo začeli tako, pač vsi so bili tam in smo bili
12:41 - tudi mi. Predvsem bi rekel, da je največja vrednost tukaj
12:47 - torej druženje, torej da v tem uživamo, hkrati pa še ohranjamo
12:52 - to ustno izročilo in predstavljamo, kako je bilo včasih, tudi ostalim.
13:00 - Ja, mogoče res mi domačini, predvsem recimo Triglavski
13:04 - narodni park, mogoče prevečkrat vidimo kot eno oviro, ki nas ovira
13:08 - pri raznih posegih v okolje, morebiti že pri sami obnovi
13:12 - stanu, morebiti ne vidimo toliko te vrednosti na dolgi rok,
13:17 - torej zakaj sploh Triglavski narodni park je, da ima namen
13:21 - ohranjati to naravo tako, kot je.
13:28 - Kmetje in prebivalci tega območja, to so že vseskozi, tudi če ni bilo
13:33 - nobenega nadzora in vsega, gospodarjenje je bilo
13:37 - vedno pozitivno.
13:43 - Sicer problem, recimo, današnjih izboljšav kmetovanja
13:49 - in vsega je tudi administracija, ker moramo te stvari spraviti
13:55 - tako rekoč vse na papir. Tudi vse te omejitve, nadzori,
14:02 - tega včasih ni bilo, bi rekel, pa je isto vse funkcioniralo,
14:07 - ker smo vaščani tega območja sami ozavestili to, da stvari držimo
14:13 - čim bolj v naravnih okvirih, da se to ne uničuje. To je naše
14:20 - okolje, to je naše življenje. Turisti prihajajo pa odhajajo,
14:27 - mi smo pa tukaj prebivalci, vedno na tem prostoru
14:31 - in premalo je tega posluha, kaj mi predstavljamo v tem prostoru.
14:42 - Saj pomoči prav veliko ni. Te subvencije ... To je tako
14:45 - malo več, kar rečeš, da to nič toliko ne odtehta.
14:52 - Mene predvsem ta papirologija, tega je noro, da vsa ta dovoljenja
15:00 - dobiš skupaj. Za domačine, jaz mislim, da bi moralo biti
15:04 - bolj enostavno to urejeno.
15:11 - Da bi tisto, kar imaš željo, da bi te v tem smislu malo podprli.
15:17 - Pa tudi magari denarno, da bi malo to delali,
15:20 - da ostaneš tukaj, da vztrajaš, da imaš zaposlitev doma.
15:29 - Jaz rada tukaj živim, sploh ne pomislim, da bi šla kam drugam
15:33 - živet, ker meni je tukaj super. Je pa toliko več stroškov in tega,
15:38 - moraš pa zato tudi več proizvesti in narediti, da lahko
15:43 - vse to poplačaš.
15:49 - Moraš biti, po domače, buldožer, pa riniti, pa riniti,
15:52 - da nekaj dosežeš. To moraš biti res trmast kot Krucmanov vol,
15:58 - so včasih rekli.
16:03 - Po eni strani mi je fino, da živim v parku in to je ena
16:06 - dodatna vrednost, absolutno. Bohinj je zelo lep.
16:09 - Ampak dejstvo je to, da moramo ponuditi še nekaj več.
16:15 - Moramo še vseeno paziti naravo, jo maksimalno zaščititi.
16:22 - Bog ne daj, da bi prišlo do prevelikega pozidavanja
16:25 - in tako naprej. Kmetijstvo mora biti v Bohinju v ospredju, potem je
16:31 - turizem. Tega bi se morali bolj zavedati. V bistvu mislim,
16:35 - da se večina zaveda tega, da je narava v Bohinju praktično vse,
16:41 - kar imamo, in če tega ne bomo čuvali, potem pa res ne vem,
16:44 - kaj nam še ostane.
16:48 - Jezero je bilo letos nadpovprečno toplo, to je že en podatek.
16:54 - In če bo šlo v tem trendu naprej, kaj pa veš, kaj bo čez 20 let.
17:00 - Mogoče bo pa konec koncev le ena topla mlakuža. Upam, da ne,
17:04 - ampak bomo videli.
17:49 - V 18. stoletju so za namene fužinarstva na Pokljuki posekali
17:52 - skoraj vsa odrasla bukova drevesa. Takrat so ugotovili, da takšen način
17:57 - gospodarjenja ne omogoča trajnih donosov in zato je bil
18:01 - že leta 1837 napisan prvi načrt za pokljuške gozdove.
18:14 - V tistem času je bila uveljavljena tako imenovana nemška šola
18:18 - gozdarstva. Gozdove so takrat gledali predvsem skozi
18:21 - lesno-proizvodno funkcijo, želeli so iz gozdov čim večje donose.
18:26 - Zato so v tistem času sejali, sadili in pospeševali samo smreko.
18:36 - Ne moremo reči, da so takrat gozdarji naredili napako,
18:40 - namreč danes lahko gledamo te lepe odrasle smrekove sestoje,
18:45 - vendar pa imamo na drugi strani tudi težave z njimi. Vsako leto
18:48 - nam ujme poškodujejo kakšnih 10, 50 hektarov gozda,
18:54 - imamo težave z vetrolomi, snegolomi in zadnja leta tudi s podlubniki.
19:07 - Bil je tak, dober meter, macesnov kol z rdečo glavo, da se je na daleč
19:12 - videlo. Zdaj pač pridemo gozdarji v gozd, vzamemo telefon ali GPS,
19:18 - pritisnemo in vemo, kje smo. Takrat tega ni bilo,
19:21 - imeli so pa karte, natančno, ročno izrisane od geodetov
19:26 - in na njih so bile tudi oznake teh mejnih kamnov.
19:31 - Eden od ukrepov, ki so ga na terenu izvedli, so bile tudi
19:35 - preseke med gozdno-gospodarskimi oddelki. Te so prvič naredili
19:39 - na prelomu iz 19. v 20. stoletje. Te preseke so v naravi štiri-
19:45 - do osemmetrski posekani pasovi, ki označujejo meje med oddelki.
19:51 - Na presekah so tudi kamni z oznakami, ki so enako označeni
19:55 - tudi na kartah. Nekoč so bile te preseke pomembne predvsem
19:59 - z gospodarskega vidika, danes pa so zelo pomembne kot habitat
20:03 - za divjega petelina in druge živali. Na teh presekah
20:08 - pogosto zrasejo borovnica, brusnica, brin in druga plodonosna zelišča
20:14 - in grmovje, kar izboljša pestrost habitata za divjega petelina.
20:28 - Ukrepi, ki se jih gozdarji držimo z namenom ohranjanja divjega
20:32 - petelina, so, da v času rastitve, to je od 1. marca do konca junija,
20:37 - ne gospodarimo z gozdovi znotraj rastišč, v radiu sto metrov
20:43 - od rastišč divjega petelina ne umeščamo novih gozdnih prometnic,
20:48 - v radiu 500 metrov od rastišč ne dopuščamo krčitev gozda,
20:53 - znotraj mirnih con pa se tudi izogibamo kakršnim koli drugim
20:58 - posegom že v času zime, znotraj mirnih con tudi ne pustimo
21:03 - pluženja gozdnih cest, za divjega petelina tudi načrtno ohranjamo
21:08 - pevska drevesa v gozdu, sadimo in ohranjamo plodonosno drevje,
21:14 - ki je pomembno za prehrano divjega petelina.
21:26 - Divji petelin je vrsta starih odmaknjenih gorskih gozdov,
21:29 - svetla smrekovja z veliko borovnice, rabi pa mir. To je zelo plaha vrsta
21:34 - kljub svoji velikosti, vedno se človeku odmika in največkrat
21:38 - najde prostor tam nekje do gozdne meje, ampak to so
21:42 - že višine 1400, 1700 metrov.
21:51 - Mirna območja na Pokljuki so zasnovana na območju barij
21:55 - in pa rastišč divjega petelina. Na območju mirnih con
21:58 - divji petelin nujno potrebuje svoj mir v obdobju rastitve.
22:03 - Takrat se namreč razmnožuje in če takrat prekinemo ta proces,
22:07 - izgubimo naslednjo generacijo. Povsod po Sloveniji številčnost
22:11 - petelina močno upada, na Pokljuki pa nekako še drži
22:15 - svojo številčnost.
22:23 - Petelin živi na relativno majhnem območju, dva, tri kvadratne
22:27 - kilometre in če vemo, da je vpliv človeka več sto metrov, 300 metrov,
22:34 - vidimo, da že, bi rekel, ena pot skozi to območje,
22:37 - ena prisotnost človeka veliko tega vzame. In tukaj je res pomembno,
22:41 - da mi ohranjamo majhne skrite kotičke, ki so res popolnoma
22:46 - nedotaknjeni. Je pa pomembno to seveda v času parjenja,
22:50 - v času izleganja mladičev, pa tudi pozimi. Sploh zima je
22:53 - za koconoge kure problem za energijo. One jejo
22:57 - slabokalorično hrano in imajo pozimi manke energije in trošenje
23:01 - energije s plašenjem je lahko za njih velik problem.
23:09 - Ljudje znamo petelina poslušati samo spomladi, ko poje seveda,
23:12 - telemetrija nam pa omogoča, da celo leto spremljamo, kje je,
23:15 - in odkrijemo tudi tiste skrite kotičke skozi leto, skozi zimo,
23:19 - ki je zelo pomembno, da jih zavarujemo, pa jih do zdaj
23:23 - nismo znali izrisati. In če si predstavljate, telemetrija izriše
23:27 - najbolj priljubljena mesta, kamor petelin zahaja,
23:33 - in v ta se bomo osredotočili z mirnimi conami.
23:38 - Bomo pa seveda imeli opravka s človeškim egom. Ljudje si vedno
23:42 - želimo iti, tudi mi, v mirna območja, se moramo pa zavedati,
23:46 - da s tem, ko smo mi dosegli mir, vnašamo nemir nekje, kjer nas
23:49 - prej ni bilo. Zagotovo je bil človek prvi pokazatelj, da se je naše
23:57 - visokogorje, naši gozdovi začeli polniti z ljudmi, ker planinci,
24:02 - izletniki in vsi ugotavljajo, da tega miru, ki je bil včasih
24:06 - v hribih, danes ni več. In to se seveda prenaša in nekatere vrste,
24:11 - niso vse občutljive, ampak nekatere vrste imajo z mirom
24:14 - velik problem.
24:29 - Gozd mi pomeni življenjski prostor rastlin in živali, za človeka je
24:34 - pač izvor mnogih dobrin. Gozd zadržuje vodo pred odtekanjem,
24:40 - gozd blaži hitrost vetra, gozd blaži temperaturne ekstreme,
24:47 - zelo, zelo pomembne funkcije gozda.
24:53 - Pri svojem delu pri izbiri dreves za posek lahko izbiram drevesa
24:59 - pri rednem gospodarjenju, ker s posekom poskušam pomagati
25:03 - nekaterim drugim drevesom, lahko pa odkrijem neka bolna drevesa,
25:08 - kakor koli, poškodovana drevesa, ki jih je pa iz gozda treba
25:11 - odstraniti zaradi sanitarnih razlogov.
25:15 - Pomemben del gozda je tudi
25:17 - odmrla lesna masa. V naravnem gozdu je je skoraj polovica.
25:21 - V gospodarskem gozdu si takega odstotka ne moremo privoščiti,
25:25 - ampak želimo si pa povečati delež odmrlih dreves, tako da bi
25:30 - tudi s pomočjo odmrlih dreves povečali vrstno pestrost v gozdu.
25:38 - Odmrla drevesa so zelo, zelo pomembna v prvi vrsti za ptice,
25:42 - ki v odmrlih drevesih gnezdijo, lahko tudi v odmrlih drevesih
25:47 - najdejo nekaj hrane. Poleg ptic naseljujejo odmrla drevesa tudi
25:53 - mnoge žuželke, mnoge glive, omeniti je potrebno tudi netopirje.
26:00 - In s krepitvijo števila različnih živalskih vrst pravzaprav krepimo
26:05 - imunski sistem gozda.
26:31 - Kot gozdarji, kot lastniki in kot upravljavci tega prostora
26:35 - želimo seveda na dolgi rok gozd razvijati v smer,
26:40 - ki ob zagotavljala trajnost in pa tudi vse ostale funkcije.
26:46 - Zdaj, pri trajnosti se zavedamo, da te klimatske spremembe povzročajo
26:52 - spremembe in zahtevajo drugačen pristop. Potrebno bo več pozornosti
26:57 - posvečati tudi drugim vrstam, ki jih žal na Pokljuki trenutno ni,
27:01 - to sta predvsem bukev in pa jelka, javor je seveda zelo dobrodošel,
27:07 - in pa te minoritetne drevesne vrste, kot so jerebika, mokovec
27:11 - in pa vse ostale. In zato smo bili zelo veseli
27:19 - enega takega praktičnega projekta, kakršen je Vrh Julijcev.
27:25 - Z njim si predstavljamo, in delno se to že uresničuje, da se obisk
27:31 - ne bo preprečeval, ampak se bo obisk ljudi usmerjal. Kot okolijsko
27:40 - odgovoren lastnik seveda podpiramo tudi ekološki del tega projekta,
27:45 - ki bo spodbudil pestrost rastlinskih in živalskih vrst.
27:52 - Že v preteklosti smo se precej, precej smo se jim povečali s svojo
27:59 - dejavnostjo in predvsem prilagajali. S finim načrtovanjem gozdarskih del
28:03 - se to da dokaj normalno tudi prenesti v realnost.
28:26 - Pri načrtovanju gozdov za naprej se vedno oziramo na 150,
28:31 - 200 let naprej. Danes je v lesni zalogi 96 odstotkov smreke,
28:36 - mi pa bi radi s sadnjo vnesli še druge drevesne vrste,
28:40 - poleg tega pa bi radi vertikalno razgibali te sestoje.
28:47 - Tako da na dolgi rok pravzaprav lahko pričakujemo, kljub temu,
28:51 - da si ne želimo, da bomo ravno te ključne vrste, ki jih zdaj
28:54 - varujemo, izgubili, spremembe pa so vsekakor neizogibne.
28:59 - Želimo si pa gozdove z več listavci, z bolj pestro vrstno sestavo,
29:04 - tako rastlinskih kot živalskih vrst.
29:10 - Osebno si kot gozdar in kot upravitelj teh gozdov želim
29:15 - dosledno spoštovanje gozda kot takega, ob tem da lahko ponuja
29:23 - vse ostale stvari, ki jih ljudje pričakujejo od tega. Na ta način
29:29 - jaz smatram, da je sobivanje sigurno možno, ampak seveda pa
29:35 - ob doslednem spoštovanju narave, gozda in pa vsega ostalega,
29:41 - kar nam je dano pač samo v začasno uporabo.
30:02 - Jaz sem zdaj na TNP-ju 12 let, drugače sem v bistvu
30:06 - že od majhnega vključen v te dejavnosti tukaj po tem prostoru,
30:09 - ker sem tudi lokalni prebivalec, tako da jaz tu tukaj čutim to
30:13 - poslanstvo, ki sem ga vzel za svojega. To v bistvu ni služba,
30:18 - to je način življenja.
30:22 - Prednostna naloga v Triglavskem narodnem parku nas,
30:25 - nadzornikov, je naravovarstveni nadzor. To pomeni spremljanje
30:28 - območja, monitoringi posameznih vrst, sploh zaščitenih,
30:32 - ukrepanje v skladu s prekrškovnim postopkom, seveda nas je pa
30:36 - nekaj nadzornikov tudi lovskih čuvajev, ki v zimskem času predvsem
30:41 - skrbimo za divjad, pač tudi nadziramo ta stanja.
30:48 - Zavarovana območja so namenjena ohranitvi nekih ekosistemov
30:52 - v čim bolj naravnem stanju s čim manjšim človeškim vplivom.
30:59 - Zato moramo v bistvu skrbeti, da krmarimo med vplivi človeka
31:05 - in tem ohranjanjem okolja v največji možni meri, kar pomeni,
31:09 - da brez določenih omejitev ne moremo tega tako izvajati,
31:14 - da bi to lahko nekako obrodilo sadove.
31:19 - Prek projekta Vrh Julijcev smo uvedli tako imenovana
31:23 - mirna območja, te mirne cone, ki zajemajo to najstrožje varstvo.
31:28 - Vsak obiskovalec zavarovanega območja se je v bistvu dolžan
31:33 - prepričati o nekih varstvenih režimih na tem območju,
31:36 - tako kot prideš, kamor koli pač prideš, ti si tukaj na obisku
31:40 - in tukaj veljajo določena pravila, ki jih je treba spoštovati.
31:45 - Kakor smo začeli s projektom Vrh Julijcev, je bilo kar,
31:49 - kako bi rekel, po domače povedano vroče, kaj bomo zdaj naredili,
31:52 - ali zdaj nihče nikamor več ne bo mogel. Ni to res,
31:55 - da nihče nikamor več ne more, marsikaj se da, ampak peš,
31:58 - ne morete se pa povsod voziti. Pač to ne gre. In to razumevanje
32:02 - je bilo kar malce kritično v startu, ampak smo mi to z vsemi temi
32:07 - obvestili, s tem ozaveščanjem javnosti v dosti kratkem času
32:11 - dosegli, da ljudje nekako to le sprejemajo, da bomo izgubili
32:16 - neke naravne danosti, ki smo jih še do nedavnega imeli.
32:22 - V bistvu jih še imamo, ampak če ne bi začeli s tem, bi to šlo.
32:45 - Poslanstvo markacista vidim predvsem v tem, da poskrbimo
32:48 - za varnost ljudi, varnost pohodnikov ter seveda tudi za samo naravo.
32:52 - Vse prevečkrat vidimo prevelik vpliv človeštva, pohodnikov
32:57 - na naravo. Nekateri v zadnjih časih niso več tako vzgojeni,
33:02 - kot so bili mogoče pred časom, uporabljajo neke bližnjice,
33:07 - se poslužujejo nenadelanih poti, vse to pa, moramo vedeti,
33:12 - da povzroča negativne efekte, kot je erozija, hkrati pa tudi njih
33:15 - pelje lahko v kakšno nevarnost. Tudi tu za mano na Studorskem
33:21 - prevalu je eden izmed žalostnih primerov, ampak definitivno
33:25 - je mogoče ljudi z neko konkretno nadelavo in v osnovi tudi
33:29 - pravilno označitvijo usmeriti na eno pot.
33:36 - V preteklosti so že potekale številne akcije, kot je recimo
33:40 - Iz doline v gore. Tudi v letošnjem letu je na planinski zvezi zopet
33:45 - velik poudarek na tem, da ljudi usmerimo nekako
33:50 - iz izhodišč v gore, se pravi mogoče od zadnje železniške
33:54 - postaje, zadnje avtobusne postaje oziroma lokalne infrastrukture,
33:59 - da se ne podajajo več v hribe do zadnje možne dovozne točke
34:02 - in potem hitro skočijo na vrh.
34:09 - Definitivno je želja mogoče, ko govorimo o Triglavskem
34:13 - narodnem parku, da ostane takšen, kot je bil pred stotimi leti,
34:16 - brez nekakšnih velikih vplivov, čemur smo priča dandanes,
34:20 - ko se v Julijske Alpe, v TNP valijo množice,
34:24 - trume turistov. Mogoče je tudi nek cilj, želja, da te ljudi
34:30 - usmerimo v sredogorje, tudi tam je narava prečudovita.
34:34 - Ni potrebe, da vsi hrepenimo po nekih dvatisočakih,
34:38 - ampak da gremo v naravo, da uživamo v naravi.
35:20 - Začetki raziskovanj Sedmerih jezer oziroma naših visokogorskih jezer
35:25 - sega nekako v leto 1990, ko smo opravili prvi poizkusni
35:30 - pregled rastlinstva in živalstva v teh jezerih. Kmalu po tem smo se
35:36 - tudi prvič srečali s problemom rib v jezeru. Približno štiri leta
35:40 - ni bilo opaziti nobenih sprememb in ko so se te ribje mladice
35:46 - prvič začele drstiti, so pa seveda zaradi številčnosti močno vplivale
35:52 - na sestavo živalstva in izkazalo se je, da je živalstvo pravzaprav
35:58 - tisti ključ, ki tudi vzdržuje kvaliteto vode v teh jezerih.
36:09 - Zdaj vemo, da je bila leta 1991 jezerska zlatovčica prinesena
36:14 - v Dvojno jezero, da bi pač lahko lovili ribe tudi v Dvojnem jezeru.
36:21 - Nihče se verjetno takrat ni niti zavedal, kakšne dolgoročne
36:25 - posledice bo to pač prineslo.
36:34 - Ribe so se hranile s temi planktonskimi organizmi,
36:41 - ki jih je bilo pred vnosom veliko, po letu '95, '96 je pa njihovo
36:48 - število začelo zelo strmo upadati in tam leta '98 praktično ni bilo
36:56 - več planktonskih organizmov, ni bilo več ličink žuželk na dnu.
37:02 - Vloga teh organizmov je pa ta, da so se pasli po algah,
37:06 - ki so rasle na dnu jezera, in s tem so pravzaprav vzdrževali
37:12 - kvalitetno vodo. Ko pa so seveda te živali bile odstranjene s strani
37:17 - rib, so se pa začele razmnoževati alge in to je pravzaprav bil
37:22 - začetek te slabe situacije.
37:40 - Jezerska zlatovčica ni evropska domorodna vrsta, ona je prilagojena
37:43 - na dolge zime, kratka poletja, na jezera, ki so zamrznjena
37:48 - in tako naprej. To je pač njen habitat. Populacija je rasla in tam,
37:53 - leta 2000 so že vsi bíli plat zvona, ker so pač določene planktonske
37:58 - vrste praktično izginile iz jezera po podatkih Niba, ki je delal
38:03 - monitoring, po drugi strani se je pa začela razrast alg,
38:06 - so se začele te alge dvigovati na površino, veter jih nanaša
38:11 - na obalo in te stvari. Po treh letih aktivnega izlova
38:16 - in predvsem prebivanja na Dvojnem jezeru v poletnem času,
38:21 - ko jezero ni zamrznjeno ali pod snegom, smo zdaj že
38:24 - tako daleč, da imamo zdaj v mrežah samo še par rib, včasih smo jih
38:28 - imeli sto. Vidimo, da v bistvu tukaj uspešnost napreduje.
38:33 - Med samim izlovom rib smo tudi spremljali, kaj se dogaja s samim
38:37 - jezerom in ugotavljali, da se pač s tem jezerom nekaj dogaja,
38:41 - nekaj, kar verjeno ni direktno povezano z ribami, čisto enostavno,
38:45 - in da je tukaj najbližja stvar, ki je jezeru v bližini, je koča,
38:49 - koča z 200 ležišči s čistilno napravo in iztokom in pred dvema
38:56 - letoma so bili tudi uradno narejeni sledilni poskusi in je bilo
39:00 - v glavnem, da se pač iz čistilne naprave iz iztoka v zelo kratkem
39:04 - času pač ta iztok pojavi v jezeru.
39:12 - V preteklosti je bilo število obiskovalcev v koči in pa tudi
39:15 - ob jezeru precej manjše, v zadnjih letih se je ta naval
39:20 - močno povečal, tako da seveda tudi učinkovitost čistilne naprave,
39:25 - s katero naj bi reševali tudi ta problem jezera, je verjetno
39:32 - že na meji zmogljivosti.
39:41 - Danes smo pač prišli do točke, ko nam postaja to planinstvo
39:45 - ali zdaj lahko rečemo planinski turizem ena izmed točk,
39:50 - ki na nek način obremenjujejo okolje. Koče kljub temu,
39:55 - da so opremljene s čistilnimi napravami in tako dalje,
40:00 - ne moremo reči, da nimajo nobenega vpliva na okolje.
40:02 - Seveda se trudimo z različnimi možnostmi, kako ta vpliv zmanjšati.
40:08 - Pri tem jezeru je mogoče ta problem, da je ta vpliv
40:15 - zelo hitro viden. Strokovnjaki, ki na tem področju delajo,
40:19 - seveda iščejo rešitve v različnih smereh. Ena izmed možnosti je
40:23 - nadgradnja obstoječe čistilne naprave, ki bi seveda v določeni
40:27 - meri izboljšala stanje, drugo je pa tudi možnost vgradnje suhih
40:32 - stranišč in tako naprej. Vsaka od teh variant ima pozitivne
40:36 - in negativne zadeve. Kako pa v bodoče, ko se bodo tehnologije
40:42 - izboljševale, še ta sistem, ki je zdaj, kakršen koli na koncu
40:46 - že bo, še nadgraditi, je pa seveda izziv za naslednje generacije.
40:52 - Hiša je res že stara, ampak se mi zdi, da se tukaj vedno
40:56 - nekaj nadgrajuje, pa se mi zdi, da se matica dosti trudi,
41:00 - saj sem zdaj tukaj kar nekaj let. Po drugi strani te pa zmoti,
41:05 - ker je toliko enih strokovnjakov, pa ne najdejo končno ene skupne
41:10 - besede, pa kaj se naredi. Vsak nekaj na svoje vleče.
41:14 - To je dejstvo.
41:17 - Daj mi enega podaj.
41:24 - Mogoče se je spremenilo to, da je bilo včasih vse malo bolj
41:27 - preprosto. Recimo si imel tri jedi, pa so bili ljudje čisto zadovoljni.
41:33 - Zdaj se pa to vsako leto nekaj nadgrajuje. Drugače, da bi se pa
41:39 - tako kaj spremenilo, se mi pa zdi, da se ni. Ja, mogoče edino to,
41:43 - da je zdaj veliko več tujcev, kot jih je bilo deset let nazaj.
41:49 - Sami ljudje, da bi se nekako spremenili, se niso. Eno so ful fajn,
41:56 - je v redu, pridejo z dobro energijo gor, pa pridejo zato, da uživajo,
42:01 - tisti, ki pa pride že slabe volje gor, pa itak najde kakšne napake.
42:13 - Kar se tiče tega prostora, ne samo tukaj, celega alpskega
42:16 - pogorja Julijcev in tako naprej, ki so nekako najbolj oblegani,
42:20 - imamo ne planinci kot taki, ampak Slovenija, neko nedodelano
42:26 - strategijo, da temu tako rečem. Po eni strani ministrstvo
42:30 - za gospodarstvo s promocijskimi aktivnostmi doma in v tujini
42:33 - privablja ljudi v Slovenijo, kar je s stališča turizma seveda
42:37 - pozitivno, medtem ko pa institucije, ki se ukvarjajo
42:41 - z varstvom narave, pa želijo, da ravno na planinskih kočah
42:44 - z zmanjševanjem standarda nekako ta pritisk zmanjšamo.
42:48 - Jaz mislim, da si moramo tukaj v Sloveniji naliti čistega vina
42:52 - in uravnotežiti, koliko ljudi bomo v Slovenijo pripeljali,
42:55 - koliko jih bomo zadržali v dolini, kako jih bomo pa spustili
42:58 - v visokogorje, je pa seveda ne vprašanje samo za planinske
43:01 - koče, ker planinske koče morajo konec koncev tudi
43:04 - ekonomsko preživeti, tega ne smemo pozabiti,
43:07 - in tukaj smo v tistem, bom rekel, zdaj nekem odločilnem trenutku
43:11 - in mislim, da ta nova strategija razvoja turizma, ki nekako
43:13 - nakazuje bolj umirjeno rast, kar se tiče obsega, je nek tisti
43:17 - korak v pravo smer. Do tega, da bomo dosegli neko obremenilno
43:22 - sposobnost tega okolja, mislim, da bo pa preteklo še nekaj vode,
43:27 - da bomo prišli do nekih rezultatov, ki bodo potem zadovoljili
43:30 - obe strani.
43:45 - Varovanje gorske narave v okviru Planinske zveze Slovenije
43:47 - sega že daleč v zgodovino. Zgodovinski naziv pa seveda tudi
43:54 - prva usposabljanja znotraj Planinske zveze Slovenije so bili
43:58 - tečaji za gorske stražarje, ki so se pa potem v začetku 2000,
44:03 - 2001 recimo, pa spremenili, se recimo bolj poglobili na tečajih
44:08 - za varuhe gorske narave. Njihovo poslanstvo je predvsem to,
44:15 - da sami prepoznajo, prvič, da se znajo sami primerno obnašati
44:19 - v gorskih območjih, hkrati pa svoje znanje prenašajo naprej.
44:28 - Naravo imam zelo rad, tako da jo srkam v različnih elementih.
44:32 - Vsi ti naši različni sistemi življenjskega prostora so zelo lepi,
44:38 - zato si pa tudi želim, da bi se narava v neki meri ohranila
44:42 - tudi za zanamce.
44:49 - Ko smo delali recimo anketo o tem, zakaj pravzaprav ljudje obiskujejo
44:53 - Triglavski narodni park, je bil na prvem mestu mir.
44:56 - In tega, če vidimo, kaj se dogaja po Triglavskem narodnem parku,
45:00 - na veliko območjih več ni. O tem se pogovarjamo.
45:04 - Kaj bo v prihodnje, kaj bo s tem našim doživljanjem.
45:09 - Ampak tukaj se že dotikamo bolj te socialne nosilne zmogljivosti,
45:12 - ne toliko narave. Narava si že nekako opomore. Pač vseeno moramo
45:16 - biti zelo previdni, ampak tudi to, kakšne so relacije med nami,
45:21 - kaj počnemo, koliko smo drug do drugega nenazadnje tudi obzirni,
45:24 - to je pa tisto ključno, kar si tudi jaz osebno želim, da odnesejo
45:28 - od tega tečaja.
45:37 - Zdaj pa, če pogledamo tale naš Triglavski narodni park,
45:41 - ki naj bi pokrival štiri odstotke slovenskega teritorija,
45:45 - je kar v določenih mesecih zelo, zelo obljuden in je to res
45:49 - en velik pritisk na naravo. In tudi sam kot kolesar
45:54 - v gorskem svetu sem tudi na tem tečaju spoznal mogoče
45:57 - ene zadeve in sem rekel, to pa jaz tudi počnem, pa ni zdravo.
46:04 - Pa moramo to prenesti naprej, pa moramo ljudem nekako
46:07 - dopovedati. Saj tisti, ki želi, bo, bo sledil tem napotkom.
46:11 - Tisti, ki ne želi, pa upam, da ga bomo prepričali,
46:14 - se pa bojim, da brez nekih omejitev v prihodnosti ne bo šlo.
46:19 - Preprosto ne bo šlo, ker smo ljudje zelo komot, preveč komot,
46:22 - pa mislimo, da je čisto vse naše. Pa je lepo, da lahko vsepovsod
46:26 - gremo, ampak je pa tudi lepo, da kaj ostane.
46:44 - Jaz sem izredno zadovoljen, da živim v tem okolju
46:48 - in je velika odgovornost mene, da poskušamo to okolje ohraniti
46:52 - tako, kot so nam ga dali ti, ki so nam ga dejansko pustili.
46:56 - In tudi pravilno je, da v bistvu triglavski narodni park ima
47:00 - ta pravila, ki so lahko za nekatere tudi zelo restriktivna,
47:03 - ampak na drugačen način žal to ne gre.
47:11 - Dejstvo pa je, da se je pač svetovna populacija povečala,
47:15 - "outdoor" aktivnosti so se zelo razmahnile, svoje so naredila
47:19 - socialna omrežja, posledično so pač ti pritiski tukaj,
47:22 - če se pogleda triglavsko pogorje, nenormalni.
47:30 - Predvsem moramo biti mi zgled in tukaj doma in kamor koli gremo
47:35 - drugam. Tudi če gremo drugam, je pač stvar taka, da se moramo
47:39 - podrediti tem pravilom, najbrž z enim razlogom.
47:43 - Tukaj potem ta pravila spoštujemo in ko jih bomo pa
47:46 - spoštovali, bo pa lahko okolje še naprej ostalo tako, kot je.
47:49 - In z neko veliko mero ozaveščanja tako parka, planinske zveze,
47:53 - nas, vodnikov, ostalih agencij in tako naprej lahko pripomoremo
47:57 - k temu, da se stanje ohranja ali pa se celo izboljšuje.
48:03 - Po drugi strani je pa tudi dejstvo, da nekemu odstotku števila ljudi
48:07 - na žalost ni pomoči in ni druge, kot pa neka represija,
48:11 - ki se je vsi najtežje poslužujemo, ampak žal drugače ne gre.
48:19 - Ko je potovanje osnovano v neki glavi človeka, je v bistvu
48:22 - pomembno tudi to, da ve, kam gre in prebere tudi neka
48:26 - lokalna pravila. Če recimo gorski vodnik lahko vodi štiri osebe
48:33 - na Triglav, jih več kot štiri pač ne sme vzeti. Seveda mora biti
48:38 - neko sobivanje med tem, da recimo, ne vem, gorski vodnik
48:41 - ali pa agencija lahko preživi, po drugi strani je pa pač treba
48:44 - na ta način omejevati, da z nekim prevelikim številom ljudi
48:47 - ne obremenjujemo okolja. In ne vem, ali si ljudje znamo
48:52 - sami sebi postaviti neke meje pa reči, OK, mogoče pa tega
48:55 - ne bom videl prav zaradi tega, da ne bom še jaz dodatno
48:59 - obremenil tiste točke, ki je že itak preobremenjena.
49:08 - Jaz sem sicer zelo vehementna oseba pa bi kakšne stvari rad imel
49:11 - zelo urejene čez dve sekundi, pa se pač ne da, ker zakonodaja
49:15 - tako hoče, včasih tudi naravni procesi in tako naprej.
49:18 - Ampak saj drugega kot to, da se usedemo za skupno mizo
49:21 - pa dorečemo določene stvari, v življenju res ni. Pač z glavo
49:26 - skozi zid se ne da in vsak mora v bistvu, če hočemo,
49:30 - če gledamo za ohranjanje narave, popustiti v tem smislu, da reče,
49:33 - OK, kapitalno bomo pač malo manj, pa ne uspešni,
49:37 - malo manj bo pač tega kapitala prišlo v žep in imeli bomo tukaj
49:41 - na koncu lepo naravo, ohranjeno naravo, ki jo bodo
49:46 - lahko občudovali tudi zanamci, za to si moramo res, res vsi
49:50 - prizadevati, lokalna skupnost, prebivalci lokalne skupnosti,
49:56 - država, predvsem pa obiskovalci."""
    print(main(vrt))
