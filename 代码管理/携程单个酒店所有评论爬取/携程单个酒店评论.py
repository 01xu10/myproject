# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------
# @project : Py_Project
# @File    : 携程单个酒店评论.py
# @Software: PyCharm
# @Author  : Xu
# @Time    : 2021/4/11 15:02
# ------------------------------

from requests_html import HTMLSession
from fake_useragent import UserAgent
from jsonpath import jsonpath
from pprint import pprint
import json
session = HTMLSession()
ua = UserAgent()

class xiecheng_hotel(object):
    def __init__(self):
        self.start_url = 'https://m.ctrip.com/restapi/soa2/16709/json/GetReviewList'
        self.headers = {
            'Content-Type': 'application/json',
            'user-agent': ua.chrome,
            'referer': 'https://hotels.ctrip.com/',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"'
        }
        self.list = [5298139,857279,61667794,5499666,36144604,7279070,9450919,35922450,9560259,41794783,17276458,1841863,63044434,5965726,848766,5804522,435528,12649418,2374742,61737360,65268142,19580056,17923046,939449,435534,6920860,5661193,17278076,35906621,25268671,21160760,8582870,55193108,8394839,68561273,65281206,976389,62688399,9055645,5499414,971713,895485,981810,6861096,20299102,36866447,929005,8655555,50463197,21789910,828316,852227,8511925,1903388,1371630,63582908,18598993,39268713,929031,16448133,36468838,2527090,1983524,4852422,32620273,63058545,61742340,1213580,8533977,2318140,1409434,7112774,31943368,2006658,22774715,2057582,2298358,890207,11083458,42579888,1961673,1531195,2280173,1532207,480193,899722,966789,793528,2269822,20613385,874699,21788369,5209154,6906077,7651479,42514432,931277,53494248,67234268,1522218,61768201,71498238,62632681,17362837,48584424,18517050,21489350,3395942,2298348,65108763,7487247,7855411,2375573,977708,35552694,1007291,8445698,35542039,6891676,62813031,1072384,2139612,7355967,5301589,5247295,54771377,1686257,834547,2253410,2270842,36246784,973765,8058347,2298992,65178495,1372447,66672568,1208397,2206828,60815918,1965833,6828842,6834416,4797044,999418,8020903,10925508,61144314,6419287,42325125,841894,1219924,23965069,5237799,6954051,2080503,33546673,1980157,1522217,995658,5548852,855115,63596042,7092085,810649,8029322,1961720,21428829,17533437,35504658,435599,848772,1054655,845620,8329933,66856751,5272844,5099395,5024485,6860986,435594,22762584,1005874,654486,2299064,6769657,36650528,5033591,1230772,8357218,64999253,7090153,8137475,17173888,61835335,789795,66672619,66840876,430482,72967905,6444189,17472709,2486886,481846,1941312,63287849,72971443,1102869,8406018,1965975,1965821,8576471,5982787,2513507,435595,1997138,789796,1879602,2042701,8692503,1838856,535841,39273553,5232775,2219523,4835894,72949553,1219291,8352259,7939720,1193256,603034,4845808,756059,72138769,850865,804790,16901233,64268928,2534373,72563178,40607448,5613008,39961123,1714342,2289172,834334,1889573,1780199,16018636,2063815,5338434,2304142,5803928,6033361,1714483,72890081,2298366,6465527,5694712,856510,6959066,1501161,3037885,5652965,42908955,1074105,608559,2137668,1640880,689675,1713987,10841645,2347050,5074159,1715422,977056,36830452,64885360,44736652,1714382,895544,17100795,971507,17526603,4037253,8060600,70162054,850735,40616510,878723,435585,62689644,758381,1254264,40606157,9216212,6860050,6861207,2626524,44166803,17902530,50813608,5460600,61919697,25280844,1400577,2302348,19452525,2611931,72672952,1432053,5668583,6042269,931040,13952544,8111680,17467089,5204782,5482478,2290913,72915441,64270136,18481500,6738363,6168556,3915739,68078273,34018665,7120674,2302426,2338812,50444806,8667899,2151035,840961,6419180,1416601,6838856,5446686,4837897,38602018,1500792,1714213,23649961,804689,897445,891534,977522,6308137,1416599,41634089,2035983,2345504,923746,2594466,72924096,5523178,4845695,1948235,6022841,72896157,17540767,1965632,8197667,6740861,8529368,1192260,5493032,62659604,804601,15041570,5401265,435582,977612,6838808,854875,8576507,834487,810678,7335216,1714370,17491944,964756,1548158,68474056,5677085,17339269,2301654,6814900,4889379,973035,2078987,17276122,8576469,62689810,850884,1826277,1715425,49567292,965177,1097313,6906056,48633528,4661292,62802883,29592472,850921,793268,8192639,63632841,43949558,7519404,5529746,931517,6841094,895204,920152,2219927,2330556,2525031,2652276,70869286,5979139,3708105,5237868,6315403,24410533,850836,21793679,6392158,2148119,1193610,43886831,6755785,71574137,6972445,2213746,5980782,2878285,8599718,834209,8533144,1964614,848768,1995670,35912170,1969210,7591857,972399,72585908,6412719,978248,5296881,3158328,33516671,7423109,45413866,5695472,2150565,19453053,2058192,1207957,8946037,10913916,5249929,2380209,8722473,2167444,6719007,1916912,25213926,41414035,2097178,72845016,856516,64225037,1526477,2599598,8806568,5896794,72324377,999477,6856436,804444,9196928,965170,43666233,5981795,2075475,2536365,4508811,43574347,1965902,2220057,1071156,812061,7352205,1715633,2384004,2311270,6956792,20051822,3202299,5979752,4544993,23699839,1978369,4840093,1664572,6868003,1373662,72213343,997708,5234786,26405275,6815501,32799622,8576453,5304047,1978877,70378583,72873229,5297916,1504952,1971335,6981595,6838952,1714590,844307,4547180,1714519,8427723,31429650,5246545,1001068,6835543,5245669,8317786,1050343,1766613,6793771,5429974,5255921,970700,6749958,6030782,940366,35925718,72971661,2102515,24361374,5093188,2089571,39464903,23464448,72843965,72895227,1714402,6128478,10301078,6763431,2998984,72972174,36262225,2966777,61470017,1424119,5233410,6809139,42919023,2307827,42210040,1948682,1962566,5614886,2272321,1970832,72674572,1609698,19440663,5007674,6422354,5246741,5666216,41394736,1795594,17360957,44326021,2187641,6847150,6810317,891236,68323831,804695,60910848,5237491,5246381,6900732,72235938,8589190,57010067,1715815,23876810,28649443,6118407,5463594,52187065,1715625,1404390,9188155,54668191,2299649,926030,2247055,72584008,2526680,8576578,3000062,1714534,4090338,8921525,5316579,5339873,5265448,2021529,43571435,54540004,988197,7355969,971217,17879331,4846085,917320,2021354,8523778,2490378,72788791,5316240,5568150,2471718,10520778,15901315,44175619,968377,17297486,18494653,2011842,50780051,67731814,2468689,6663064,5218663,6793616,5128301,2131757,17998978,2170440,19812170,5669981,6843231,5607555,2617825,22823304,2021583,62796564,2541484,3045579,895780,50777604,6022838,6162094,805152,805010,8576468,805199,51306403,72965182,54873869,21148785,2220171,928246,66977143,1964339,5655434,1193201,840155,17358062,6764825,1235818,19613821,1938512,72750525,8576462,1370157,1316046,1949402,72148268,7996418,8556268,5980432,50486422,2116521,6788945,946648,68091648,41062567,7287522,6860902,19571339,5316153,23756089,42577902,56970470,2387752,846828,5939843,805211,8060810,2021550,6763000,5244602,4980758,704611,15040732,879531,50996292,1325597,5247073,7427837,5983136,2365896,5978550,18465755,5249942,1299976,2468560,4694948,1715657,26579657,46467469,5548575,2647523,18437642,18462435,805083,43643171,7819345,43576812,15053285,8060807,72896400,26196428,1522219,3328179,17361934,1308399,804957,39413841,5380203,845493,1935108,6268029,928178,5792400,1713974,8546434,991565,1855085,5379021,4836643,26533796,2130637,1854636,50018726,5276274,5250060,5315816,4845837,2002961,928473,66460401,4687259,35623731,8435940,9325341,1935074,50782091,1496634,1989471,5238022,11888498,834524,4629296,928238,8576503,11403610,35907575,8401589,5599525,5645058,21800907,65811042,1551374,6037794,2605573,5272101,804975,1980399,1487774,16101841,5772014,6817669,8576430,70352117,21788163,1714067,971224,21908585,28336416,7050625,1713770,8327547,5316631,2002912,5635420,5669807,805121,7783992,855342,70415052,9067566,50777201,4522294,5971576,46029757,1677937,52807055,8921654,5519779,68047173,4500667,11274197,6789581,43132364,72796603,51734485,2247302,39269249,6838133,6789626,70516791,6478411,50773842,72817841,70886842,1432932,5967131,5620202,56381026,5386756,43266046,6929409,5481041,5803177,72637360,2343496,68092082,5664768,23673468,5668868,63353911,52757616,61791121,50434255,5249892,1106701,61100113,2114689,54628930,878860,67826245,62623866,58468820,53061062,5278978,23838539,10911920,34024654,5981500,5612437,72922942,54757876,15958343,2091144,14640908,963500,43959000,2151231,43498623,43424080,4835896,2486374,48000515,72872677,54566031,64579304,61617782,43372484,1070679,5980970,993556,17342823,11245512,5665064,35926184,2890350,2728530,2643882,65110154,67846819,50383225,41610923,17354755,5567115,1949680,45970520,2009276,10482670,6160842,9206054,53221194,42366110,2128850,47869276,891449,72816632,1268461,6855908,2313162,8921562,5887027,68639321,4335667,65031142,51045574,1223893,72970159,5668115,18514983,50740152,65109398,64180263,60814175,805013,72990831,31620378,9077200,72688920,72634075,43265049,72688922,72648362,72646543,8921634,61743478,5248174,45816672,2245145,34051477,68386226,43538237,19549977,70475234,43326749,62445344,43453680,50777285,44231971,53020191,22418915,55922127,51144043,70371978,68544019,33587429,66937458,70474724,19479980,18081781,1308456,4372506,65035404,2213069,11893100,6720502,9447513,9670142,17502700,12105116,7364903,39485735,1530513,5451759,8580183,1713745,890447,6864679,8871370,5074156,8077199,6159860,18056572,42690885,1714473,6724272,1964560,6856341,21133678,981887,1920274,16152530,930350,8921671,6045043,4687132,17346451,2252482,5265836,4846011,5419024,1121940,1192278,72674636,6770175,7293122,6916975,43489994,43458375,7239398,907975,6959138,1570117,2056252,31204358,44091223,42827354,12803366,66777240,1989469,43429672,8576406,41506882,43502469,9455659,67517595,68030547,70165066,805169,17532317,9456694,13959729,2150265,2053758,10218488,44720594,43835951,1967642,1964607,48892969,6207876,17375341,64024291,50775130,5665080,43360202,8576224,899524,5803205,20026210,5635364,1100331,14082132,928168,1073233,5660576,8401789,8075662,10936151,8077202,44232342,42262549,43635233,43640257,43331287,42892566,9450599,13950826,17338733,35527507,43473931,42369030,13992795,13953444,7338924,43348791,42186809,43325169,18287078,17345896,15963873,18472423,15850771,18487369,9456669,11288370,8576510,43500726,18520436,26620842,8576631,17330262,18535963,15963964,5250289,5892409,12675335,8503086,1371709,8110358,18487376,10985595,18485779,12801060,15986641,972992,1909325,11296012,8576351,43638212,29996275,834556,8902469,8075664,8576229,13995315,8576274,17327708,15988050,23935920,42729593,48094048,18488990,1713881,15051760,6846734,16100715,37484846,37047036,18470063,65049818,8576283,23928658,18488998,14082365,16101432,15958318,12829515,9507240,35526418,19913310,10935103,13953436,44117171,18461478,12514250,13958343,13991355,40256042,65650785,12093173,71942711,11306497,58721471,42485033,29706739,68193436,66685129,19647926,17353783,70896051,9457913,68097840,11000130,18521082,8576293,55190361,13952527,10939243,9448503,15986573,71677118,11088864,71989206,67563780,28521724,26621787,11156551,1965918,43457254,8576396,28520457,18408854,13303498,42153252,43642525,42139015,42180734,44235576,17359637,18486352,14569840,15963937,18471339,11075072,18487380,42740613,44555589,8576231,18495695,15964015,8075660,18524703,38828953,42772738,18536903,51812820,8576456,28517221,28521873,8576377,15964122,61099756,54754425,50776555,42746468,11270398,70817646,18472409,5234573,43429996,43640021,28517372,42131472,43637374,43624972,42123640,44220687,43428252,43378411,43459793,42345672,42255651,43455477,44427872,43266665,43358803,43477787,42266847,29999650,6746320,1226777,43482679,43639457,5266515,43373781,42187389,42164119,6808459,44231964,37046872,43461518,17353790,66731809,42740602,44236379,43486228,42126569,43326740,42725767,42729220,44223077,43376606,44226550,41840017,38828668,38828653,43418693,42370682,43464873,37062968,43389760,43424867,43644245,44234226,43501660,42158508,44227082,43494039,42369257,43647073,43324863,43421287,42259075,37043152,10841249,43644188,62630691,45939717,8576276,42238946,43325154,37059445,42178028,42174695,43464956,43392836,37062344,42738901,43636418,42122990,43356289,42123676,37062120,42209535,42131160,43452110,37069398,43420362,42264214,54631020,37069450,8576297,37065123,38829233,8576421,12458744,51800552,42170482,28519858,43639365,43337016,18485399,44225797,7335227,15964113,18442676,12651690,43420340,16100191,29706725,53237689,15963926,15958326,54727929,50780084,11218077,23687327,37069984,18462448,16100837,13959221,28516931,53876675,18473788,23843561,15852468,2010157,64802073,43635733,43453571,53895139,50777186,50155582,18487378,15986609,17343324,18487727,15852890,42711746,13952563,42250213,42246301,18064654,18488978,18467333,13980817,17345891,51876869,53083665,43383601,37062866,42209458,15963894,18522550,12799929,42721790,6479707,48042477,53256910,50778429,14577028,12196531,43270959,36269489,16002375,13336399,28521495,44227786,18535952,16100192,50774481,15958358,10954469,43378388,16101027,41629858,53495444,42130496,45705676,44216310,15963982,13951399,43392865,11059164,37063538,53800125,54629400,53224446,43525192,43489794,37060096,43430035,44236778,43519733,44236559,28520453,43435995,43327996,42704881,43644342,37070459,43382668,43355678,43640924,43571911,42728021,36279172,42262582,43328034,42252082,43442757,42158522,42717838,44219334,44236068,43647800,43435286,44225142,43444159,42189490,43452810,43423189,43325877,43474100,42738412,43311737,44212679,44228899,44231496,43479674,44217710,43645821,38698447,43640543,42342900,43328574,43275440,43393854,42141021,43422417,15040731,42147523,43383012,38698323,42247514,42126156,43960719,37048587,42146344,44218628,43458291,43328425,43476222,42133989,42892929,43433363,50774387,50778895,50775781,52538267,54637881,37046758,43269510,37061235,51741208,39401698,8576225,11289984,10946499,10950464,11270387,52807076,8576418,53078325,50777928,28612911,37065168,43326447,43268544,37045078,42236084,44217569,42745424,37065417,43636631,42369140,37062416,43650329,43649118,43640892,43462917,43367195,42126612,42130419,37062809,43355620,44214571,42892851,42370878,43635849,11242464,43378685,42150744,42266536,44235628,37059982,44219728,43647932,43486767,43388862,37063765,43650050,43520129,44226734,43637192,42131968,43493641,44232838,38697756,44235544,42122573,67827943,44234086,72182031,54637959,50775002,37065174,10954460,42510588,42133942,43208091,43268516,43405001,43452303,42122294,37065183,42738603,44214527,37061398,42729014,42703760,43451211,42369109,42718911,15963919,43320425,35526444,42735367,42726357,43482541,43635772,43425801,43413695,38829751,49992586,17280666,54734864,6797162,43273660,37059289,15963865,37069890,42772539,43445992,43345484,39485770,43494632,43480894,43644744,37059934,43370115,42714115,15980209,13951367,43442275,53222090,12675371,35526603,12671126,43519786,35526926,53898539,53578967,52990337,53212519,42344663,43376937,42749385,17247178,6432757,16100194,43451404,43645593,50775182,50779431,1856560,50741625,53866173,13951345,64184503,1940958,11075074,6832294,25464547,43647959,43357820,51674663,54632193,50745707,51812408,50782744,42772782,42124140,42715845,18485497,2101209,53039048,54621275,43649201,43380313,27009021,13991783,5638968,52819912,52171371,50774965,50778717,18462449,2562068,38697207,52180591,12799843,50747076,53260419,26622949,44234355,52166097,13952573,50474249,50023650,50533817,54257628,50495346,50494806,53587701,50777498,50523821,50525426,43482531,53233196,50434648,50499823,50469256,52765634,70526640,50474786,50442572,53014783,52180373,50477418,50461782,6290257,42483111,43434302,43272989,43634666,43488507,35527353,38697513,18495697,43650639,42772813,43374407,44215631,11271157,43646810,53008925,37065078,36258147,43270941,44235795,8576413,53588747,11101842,9454631,11289986,15958311,43635881,50995425,43502619,15964067,28520440,16105925,43271233,52848876,50782129,50773987,29998284,54638147,43642658,50385106,57672120,53496736,52178723,52171021,8576498,11154822,53077910,64550916,53577790,56365440,50747928,52186634,60162179,54628453,66769504,50746568,51161349,57261458,61100193,54629911,57165204,52102338,57986919,54566414,52803442,53213491,50774745,50843614,54635933,68091061,53580698,56383655,55194847,44236277,59299328,68090274,42702905,61416787,52818596,52178974,63288962,68224214,42206682,43638188,50773868,57727495,68393765,52183381,36272944,43645754,68397091,36254199,61765864,54756589,68177435,50383009,64228881,50434674,48255053,61101625,68393444,52847852,61630525,54756115,42258308,50744335,56973854,51997868,68091041,70518204,48087918,48005304,70518694,53577658,57443806,63440173,57723487,68392266,43634979,43635889,66001640,50780850,50780577,54730435,60186104,8576548,68396484,52176996,57436371,52180106,52182241,43477827,52538491,43504899,50782792,13953446,43520861,43637752,6734885,50778316,54638289,53071788,50780195,45695920,38829051,18072418,44220485,5982368,43445503,42131271,42725893,44219398,42244334,35526937,37062937,36298841,43267739,43326583,44232408,37064994,51045711,50778169,43638644,35526121,43272551,37070065,44215525,42124929,42738287,42133090,42150729,43495283,42892575,37062927,37064858,37060479,43640564,23687346,67851083,8576372,43450817,37060795,42731020,43437521,43500936,43666799,43572230,43526688,18461943,54638279,43325181,55233387,51050152,54629855,52172645,50389011,68397217,70894898,50774129,53579096,54727439,52846322,70411334,68395915,43474068,43640768,18485781,8576497,8576368,53876363,18494683,1094632,53222954,54668616,43537922,35526311,53221173,54248239,53234873,54635723,51841371,62623413,57020051,50437013,43713087,54637284,11154810,68590094,53224037,70888830,68397346,38698195,53140916,17334847,42149808,18550995,43319056,37046932,43571596,37049452,43403632,37048683,5250061,15995003,28517383,16100828,50470120,57670971,52628788,52186185,53925664,48028196,62446093,51879131,50778308,44234062,44226344,52185457,36262561,54894757,53509553,50775753,54567957,54729114,50781289,70410852,17354750,43274615,55221372,43641885,43638250,53263955,53903438,56660036,70308264,50782533,68085807,28520023,5524621,37047297,36252850,43314666,53709239,54669671,38235614,36277128,57034674,68096091,43491509,45696420,44993082,36261257,50745442,36254425,36271763,35527185,57007408,42738933,71451987,57017092,62623974,55723027,53585041,64243281,54548365,52987885,8576376,58755983,69472923,64246966,62381897,56613889,52944908,70352005,70483612,56245349,42123336,43458219,43514465,55506402,43418697,42265986,43420664,53212350,50471961,43538213,37045301,38829875,42725920,45743627,37049732,43571870,36265191,38829091,37052412,36184684,57681871,67672174,61767145,52527113,50780539,60038103,57034007,53477836,50389732,36257952,64239683,50777514,53077936,52944202,57183233,51757405,54728080,50773990,35526634,56449816,57430131,52180762,50777427,68589333,64993757,55928630,70305765,52828791,50739522,65274742,43643786,70795638,68177045,61672093,70897110,48008294,43636688,52944778,71509492,61632343,68397328,57929927,72184219,63288885,55212618,53511497,43488372,13950777,65419406,42122276,5803206,43640219,43635366,43636510,36272874,50774983,53239047,43337070,43571932,52022948,70913855,50466408,52628603,64230371,57727668,55744713,52980476,54568065,28517759,50534827,54636801,41601369,1967295,43454824,43338667,43524347,42713961,8576366,50776447,43667133,54430465,54992032,42153040,43641623,43422511,52622401,52522937,67901743,50392167,50384873,52185469,48590628,52971683,66981603,57162979,53232180,64979164,60147509,50775434,53263146,46044165,70314248,57033974,60147740,52623061,50444411,53085140,46154223,45810147,70797522,54268839,53221564,45816847,50781360,53260552,11054217,43453321,43399816,56382612,64241647,53576731,57447360,55466796,43624770,47993843,54731823,2128371,6802865,8576648,2035856,57171231,14083133,57080397,52173216,53261656,60596827,60815278,54116491,53578626,62623971,61415338,53258037,68347965,53229535,44236500,43641681,13959088,43637080,50741099,1094625,1100163,37053442,43417566,43490155,43273249,42713762,43380454,43453829,52102206,36257878,68090483,46701399,53258187,54632447,52315661,50381949,68406586,55235178,53024464,52175694,54730944,68395577,61945028,53590571,50776790,53223061,54651959,43506617,43321889,42743551,43350246,36269650,54651425,55933220,50135550,48688882,36258331,52811941,52184269,54637926,52020827,50195154,42169135,57202364,61636203,50747181,53485246,57165384,50778535,53224689,52820150,53579162,54631027,52013219,36259168,36261172,54266895,36256525,57408063,61638608,54628006,50778928,45702583,56174918,70645426,52803278,61945901,70353936,70353942,70305087,36259125,57164950,70306820,50776125,70305976,62623003,70308866,36262528,70817238,61935838,70308368,70540133,36266647,54567387,36267561,50538289,52979258,60597463,70412307,68397223,70838704,54701376,61944346,57897201,55734500,53261860,52114506,70319512,60817347,50740564,70875809,70875804,50740290,28068570,2057749,5245592,44212753,2253126,51822283,36267555,50776556,54670514,5380669,44216419,42749273,15963935,45816868,53015117,57443873,62623388,37044642,46009452,43314414,42220477,43353416,52000277,43519585,61665200,53219527,43423089,52802924,51840450,56237561,55767947,56382657,66962796,54602536,53498202,56219572,70412610,57701886,54734662,53218166,49463031,43538057,52811556,43420492,42715449,43426678,43326733,43522470,43426976,46828039,45695146,36276563,45748467,44624151,42135199,43355882,45717553,43638589,36268271,44627251,43351848,43417641,68347886,53498184,54566108,54508126,50777902,53866181,57178578,70305106,52521814,57164333,71451918,58721898,70353774,70305898,50777293,48960453,70308271,54728060,55238130,60039697,70411658,70315055,70971558,53263151,70351359,49485696,43326237,43488708,54650781,53866224,36254225,53055938,54669609,61631596,50493316,54429589,48563070,50745604,36276666,37048330,50157376,51838341,50777854,53497576,66760921,50434063,50469012,66770022,70305068,54637704,54699829,54633716,50388774,52849716,45879214,53024144,70305865,53576185,57164767,45747965,53587975,53489128,64511454,53052542,54628992,51050467,38697803,50382173,53578300,42746281,52816676,51840451,8921586,6860262,56116062,45762245,45812077,53023749,53585752,46756596,52807079,52812372,45904888,59409454,50463366,55462947,50745647,47962892,66969412,52115808,52972253,48564367,50778790,45811348,53221897,49738175,46809663,43323695,50525064,47643617,52173281,47995982,48871535,53497946,52114490,70304506,53223303,57009122,50471825,46180960,50850391,50505810,52014989,52114623,50742152,71962254,51616681,71671364,55238083,57269706,70411605,53043609,54632628,52848946,52113398,48001373,36255435,52114978,53263063,52803659,51840024,45761902,50482306,45815876,54024208,64184084,61631464,45885724,55225429,52179756,54636963,46777056,36258595,50382688,50438072,52813776,44229283,45736627,70427862,50473588,52801672,53262015,46838953,44627279,47643442,57178581,45695228,53576128,53577506,61638204,48563337,36262650,52531857,48584355,48010311,45750595,45768245,55729242,48700801,48098139,45754647,45756752,45757459,52114640,52804354,47643473,64993706,45743762,48562264,60817744,36258205,50251344,70304411,70304548,66962646,53576887,52169565,66980485,54479164,50284906,53481420,66932335,50777761,52761463,66933040,53237732,48584194,48044975,66755009,71949837,70411579,53223712,45720001,52814000,46115355,50801187,45756293,45757089,45756935,54638346,70889713,52115014,52114487,47643348,70304814,67224733,70305071,70305201,53903383,50530223,64980525,51479843,48071847,62490051,53806498,70304545,70304552,66962657,50482135,70307442,70979510,70354955,70305883,70305860,48582525,53579456,44223668,43437557,50156515,54628623,45766275,70832324,46011454,46815665,50452631,52813738,55713313,55124503,58106602,45818135,66988011,55240575,53585818,52110890,54732336,51045500,45902358,46050298,45755378,70871042,66760615,47623945,70888112,49508562,70416027,70416137,51050483,52114843,70810733,47626924,45808253,45693290,45760213,57163771,52821538,36257139,70353958,70304788,70353945,70353933,70304851,48022181,46154289,70304964,70304971,70305085,71451988,70305042,70305034,71451911,53051681,54755349,53903426,55984350,70535148,70305770,70354927,46170401,49119515,70320437,55232121,50480818,70533568,70320585,46154894,70304445,58721662,70976278,67666754,70304637,70353745,66962578,70796106,70304672,70304673,70304674,70304675,70304678,70304680,70304684,70353836,70304652,67666906,70353891,45761885,70435806,70353860,70353869,67685403,57166637,53480369,59296492,50432658,59296365,66816505,70307638,70307620,70307624,70307589,52103324,45697288,70979464,70979558,70305809,70354970,70354972,45813385,70305893,48025221,70355025,70355028,70355031,70355033,70355019,70355023,53465070,45764212,70305986,45813319,55234101,46010137,66932216,50777365,46009552,57183707,42716262,52186606,67685170,50449530,52186358,52761409,48960123,45765542,70817173,70817269,56660294,56660046,50450515,70309803,70309770,61935705,70309837,54548269,50534277,52172402,70816064,70308287,70308260,70308267,70423019,70308404,52188442,46159065,52188596,53220762,45814893,45766036,70308709,53582647,52976397,50748263,45767361,66755444,65362804,70868133,65362755,48470589,70425942,52812461,50748062,70868357,55220875,66771392,70655612,50534847,70655625,46012483,52172889,70541152]
        self.paylaod_1 = {"PageNo":'',"PageSize":10,"MasterHotelId":'',"NeedFilter": True,"UnUsefulPageNo":1,"UnUsefulPageSize":5,"isHasFold":False,"head":{"Locale":"zh-CN","Currency":"CNY","Device":"PC","UserIP":"","Group":"","ReferenceID":"","UserRegion":"CN","AID":"1881","SID":"2209","Ticket":"","UID":"","IsQuickBooking":"","ClientID":"1618114092608.33n7u4","OUID":"5673F96C4538A5F36B036E6718374C23%7C100.1030.00.000.00","TimeZone":"8","P":"79688637668","PageID":"102003","Version":"","HotelExtension":{"WebpSupport":True,"group":"CTRIP","Qid":"534939057807","hasAidInUrl":False},"Frontend":{"vid":"1618114092608.33n7u4","sessionID":3,"pvid":59}},"ServerData":""}


    def parse_start_url(self):
        print('************欢迎来到携程酒店***********')
        # for id_list in self.list:
        name_url = 'https://hotels.ctrip.com/hotels/detail/?hotelId={}'.format(55193108)
        response_1 = session.get(name_url,headers=self.headers)
        house_name = response_1.html.xpath('//*[@id="ibu-hotel-detail-head"]/div[1]/div[1]/div[1]/h1/text()')[0]
        pprint(house_name)
        self.paylaod_1["MasterHotelId"] = 55193108
        self.parse_review_data(house_name)
            # break

    def parse_review_data(self,house_name):
        i = 1
        j = 1
        while True:
            print('--------第{}页---------'.format(i))
            self.paylaod_1["PageNo"] = i
            payload = json.dumps(self.paylaod_1)
            response = session.post(self.start_url, headers=self.headers, data=payload)
            if i == 1:
                ctripTotalReviewsForPage = (jsonpath(response.json(), '$..ctripTotalReviewsForPage'))[0]
                ReviewBaseInfo = jsonpath(response.json(), '$..ReviewBaseInfo')
                # pprint(categoryScore)
                score = jsonpath(ReviewBaseInfo, '$..score')[0]
                recommendPercent = jsonpath(ReviewBaseInfo, '$..recommendPercent')[0]
                print(house_name, score, recommendPercent, ctripTotalReviewsForPage)

            if j <= int(ctripTotalReviewsForPage):
                Review_List = jsonpath(response.json(), '$..ReviewList')[0]
                # pprint(ReviewList)
                for review in Review_List:
                    room_Type = ''.join(jsonpath(review, '$..roomType'))
                    release_Date = ''.join(jsonpath(review, '$..releaseDate'))
                    review_Score = ''.join(jsonpath(review, '$..score'))
                    travel_Type = ''.join(jsonpath(review, '$..travelType'))
                    review_Content = ''.join(jsonpath(review, '$..reviewContent'))
                    print('*********第{}条评论下载完成***********'.format(j))
                    print(room_Type, release_Date, review_Score, travel_Type, review_Content)
                    j += 1
            else:
                break
            i += 1



if __name__ == '__main__':
    hotel = xiecheng_hotel()
    hotel.parse_start_url()
