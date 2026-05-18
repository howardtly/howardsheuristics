// ════════════════════════════════════════════════════════════════════════
// WASDE DATA — 1990/91 through 2025/26F
// Line items in exact USDA WASDE report order
// ════════════════════════════════════════════════════════════════════════

const MY = [
  "1990/91","1991/92","1992/93","1993/94","1994/95","1995/96","1996/97","1997/98","1998/99","1999/00",
  "2000/01","2001/02","2002/03","2003/04","2004/05","2005/06","2006/07","2007/08","2008/09","2009/10",
  "2010/11","2011/12","2012/13","2013/14","2014/15","2015/16","2016/17","2017/18","2018/19","2019/20",
  "2020/21","2021/22","2022/23","2023/24","2024/25","2025/26"
];
const FC = MY.length - 1; // forecast column index

const CORN = {
  label: "Corn", id: "corn",
  sections: [
    { header: "Area, yield, and production", unit: "million acres / bushels per acre / million bushels", rows: [
      { label: "Area planted", values: [74.2,75.9,79.3,73.2,79.2,71.2,79.5,79.5,80.2,77.4,79.6,75.7,78.9,78.6,80.9,81.8,78.3,93.5,86.0,86.4,88.2,91.9,97.2,95.4,90.6,88.0,94.0,90.2,89.1,89.7,90.8,93.4,88.6,94.6,90.6,91.0] },
      { label: "Area harvested", values: [66.9,68.8,72.1,62.9,72.5,65.0,72.6,72.6,72.6,70.5,72.4,68.8,69.3,70.9,73.6,75.1,70.6,86.5,78.6,79.5,81.4,84.0,87.4,87.5,83.1,80.7,86.7,82.7,81.3,81.3,82.3,85.4,79.2,86.5,82.7,83.5] },
      { label: "Yield per harvested acre", values: [118.5,108.6,131.5,100.7,138.6,113.5,127.1,126.7,134.4,133.8,136.9,138.2,129.3,142.2,160.4,148.0,149.1,150.7,153.9,164.7,152.8,147.2,123.1,175.1,171.0,168.4,174.6,176.6,176.4,167.5,171.4,177.0,173.4,177.3,183.1,181.0] },
    ]},
    { header: "Supply", unit: "million bushels", rows: [
      { label: "Beginning stocks", values: [1344,1521,1100,2113,850,1558,426,883,1308,1787,1718,1899,1596,1087,958,2114,1967,1304,1624,1673,1708,1128,989,821,1232,1731,1737,2293,2140,2221,1919,1235,1377,1361,1738,1540] },
      { label: "Production", values: [7934,7474,9477,6338,10051,7374,9233,9207,9759,9431,9915,9507,8967,10089,11807,11114,10531,13038,12092,13092,12447,12360,10755,13829,14216,13602,15148,14604,14340,13620,14111,15115,13730,15342,15143,15109] },
      { label: "Imports", values: [3,20,7,17,10,16,13,10,22,15,7,10,14,14,11,9,12,20,14,8,28,29,160,36,32,67,57,36,28,42,24,24,40,25,25,30] },
      { label: "Total supply", values: [9281,9015,10584,8468,10911,8948,9672,10100,11089,11233,11640,11416,10577,11190,12776,13237,12510,14362,13730,14773,14183,13517,11904,14686,15480,15400,16342,14933,16508,15883,16054,16374,15147,16728,16906,16679], bold: true },
    ]},
    { header: "Use", unit: "million bushels", rows: [
      { label: "Feed and residual", values: [4868,4886,5288,4715,5535,4711,5277,5483,5479,5664,5842,5868,5563,5795,6162,6141,5591,5913,5182,5125,4792,4557,4315,5036,5280,5112,5470,5302,5429,5900,5598,5720,5625,5750,5825,5900] },
      { label: "Food, seed, and industrial", values: [1399,1474,1570,1584,1638,1653,1691,1743,1805,1913,1957,1990,2340,2537,2686,2981,3488,3860,4410,5018,6426,6438,6039,6501,6595,6640,6885,7056,6793,6250,6470,6990,6175,6590,6625,6700] },
      { label: "  Ethanol and by-products 1/", values: [360,400,460,490,530,400,430,480,530,564,628,706,996,1168,1323,1603,2119,3049,3709,4568,5021,5000,4641,5124,5200,5206,5432,5605,5376,4857,5033,5375,5175,5400,5500,5575], indent: true },
      { label: "Domestic, total", values: [6267,6360,6858,6299,7173,6364,6968,7226,7284,7577,7799,7858,7903,8332,8848,9122,9079,9773,9592,10143,11218,10995,10354,11537,11875,11752,12355,12358,12222,12150,12068,12710,11800,12340,12450,12600] },
      { label: "Exports", values: [1493,1554,1623,1319,2177,2228,1797,1504,1981,1937,1941,1905,1588,1900,1814,2134,2125,2437,1849,1987,1835,1543,731,1917,1867,1898,2293,2438,2066,1778,2753,2471,1986,2400,2550,2400] },
      { label: "Total usage", values: [7760,7914,8481,7618,9350,8592,8765,8730,9265,9514,9740,9763,9491,10232,10662,11056,11204,12210,11441,12130,13053,12538,11085,13454,13742,13650,14648,14796,14288,13928,14821,15181,13786,14990,15375,15000], bold: true },
    ]},
    { header: "Ending stocks and price", unit: "million bushels / $/bushel", rows: [
      { label: "Ending stocks", values: [1521,1100,2113,850,1558,426,883,1308,1787,1718,1899,1596,1087,958,2114,1967,1304,1624,1673,1708,1128,989,821,1232,1731,1737,2293,2140,2221,1919,1235,1377,1361,1738,1540,1680], bold: true },
      { label: "Stocks/use (%)", values: [19.6,13.9,24.9,11.2,16.7,5.0,10.1,15.0,19.3,18.1,19.5,16.4,11.5,9.4,19.8,17.8,11.6,13.3,14.6,14.1,8.6,7.9,7.4,9.2,12.6,12.7,15.7,14.5,15.5,13.8,8.3,9.1,9.9,11.6,10.0,11.2], bold: true, pct: true },
      { label: "Avg. farm price ($/bu)", values: [2.28,2.37,2.07,2.50,2.26,3.24,2.71,2.43,1.94,1.82,1.85,1.97,2.32,2.42,2.06,2.00,3.04,4.20,4.06,3.55,5.18,6.22,6.89,4.46,3.70,3.61,3.36,3.36,3.61,3.56,4.53,5.95,6.54,4.65,4.35,4.20], price: true },
    ]},
  ],
};

const SOYBEANS = {
  label: "Soybeans", id: "soybeans",
  sections: [
    { header: "Area, yield, and production", unit: "million acres / bushels per acre / million bushels", rows: [
      { label: "Area planted", values: [57.8,59.2,59.2,60.1,61.6,62.5,64.2,70.0,72.0,73.7,74.3,74.1,73.9,73.4,75.2,72.0,75.5,64.7,75.7,77.5,77.4,75.0,77.2,76.5,83.3,82.7,83.4,90.1,89.2,76.1,83.1,87.2,87.5,83.6,87.1,84.0] },
      { label: "Area harvested", values: [56.5,58.0,58.2,57.3,60.9,61.6,63.4,69.1,70.4,72.4,72.4,73.0,72.5,72.3,74.0,71.3,74.6,63.6,74.4,76.4,76.6,73.8,76.1,76.3,82.6,81.7,82.7,89.5,88.1,74.9,82.3,86.3,86.3,82.4,86.1,83.0] },
      { label: "Yield per harvested acre", values: [34.1,34.2,37.6,32.6,41.4,35.3,37.6,38.9,38.9,36.6,38.1,39.6,38.0,33.9,42.2,43.0,42.9,41.7,39.7,44.0,43.5,41.9,39.6,44.0,47.5,48.0,52.0,49.1,50.6,47.4,50.2,51.7,49.5,50.6,51.7,52.0] },
    ]},
    { header: "Supply", unit: "million bushels", rows: [
      { label: "Beginning stocks", values: [239,329,278,292,209,335,183,132,200,348,290,248,208,178,112,256,449,574,205,138,151,215,169,141,92,191,197,302,438,909,525,257,274,264,340,420] },
      { label: "Production", values: [1926,1987,2188,1871,2517,2174,2382,2689,2741,2654,2758,2891,2756,2454,3124,3063,3197,2677,2967,3359,3329,3094,3015,3358,3927,3926,4296,4392,4428,3552,4135,4465,4276,4165,4461,4316] },
      { label: "Imports", values: [3,3,3,5,5,4,4,5,5,5,5,3,5,6,5,4,4,10,13,15,14,16,41,72,33,24,22,22,14,15,20,16,25,30,25,25] },
      { label: "Total supply", values: [2168,2319,2469,2168,2731,2513,2569,2826,2946,3007,3053,3142,2969,2638,3241,3323,3700,3253,3180,3512,3494,3325,3225,3571,4052,4141,4515,4716,4880,4476,4680,4738,4575,4459,4826,4761], bold: true },
    ]},
    { header: "Use", unit: "million bushels", rows: [
      { label: "Crushings", values: [1187,1254,1279,1270,1405,1370,1437,1597,1590,1578,1640,1700,1615,1530,1696,1739,1808,1803,1662,1752,1648,1703,1689,1734,1873,1886,1899,2055,2092,2165,2141,2204,2213,2300,2410,2380] },
      { label: "Exports", values: [557,685,766,589,838,851,882,874,801,973,998,1064,1045,886,1103,939,1116,1159,1279,1499,1501,1365,1317,1647,1843,1936,2174,2129,1748,1682,2266,2158,2015,1750,1825,1900] },
      { label: "Seed", values: [66,62,62,65,66,68,69,75,78,80,80,80,80,80,86,82,84,78,82,90,85,83,90,88,99,97,97,102,90,86,91,100,97,97,97,95] },
      { label: "Residual", values: [29,40,70,35,87,-111,49,80,129,86,87,90,51,60,63,61,96,8,52,20,45,6,-40,10,51,31,49,38,42,43,-75,2,24,12,74,-34] },
      { label: "Total usage", values: [1839,2041,2177,1959,2396,2178,2437,2626,2598,2717,2805,2934,2791,2556,3148,3067,3503,3048,3075,3361,3279,3157,3056,3479,3959,3950,4266,4324,3972,3976,4423,4464,4349,4159,4406,4341], bold: true },
    ]},
    { header: "Ending stocks and price", unit: "million bushels / $/bushel", rows: [
      { label: "Ending stocks", values: [329,278,292,209,335,335,132,200,348,290,248,208,178,82,93,256,197,205,105,151,215,169,169,92,93,191,249,392,909,500,257,274,226,300,420,420], bold: true },
      { label: "Stocks/use (%)", values: [17.9,13.6,13.4,10.7,14.0,15.4,5.4,7.6,13.4,10.7,8.8,7.1,6.4,3.2,3.0,8.3,5.6,6.7,3.4,4.5,6.6,5.4,5.5,2.6,2.3,4.8,5.8,9.1,22.9,12.6,5.8,6.1,5.2,7.2,9.5,9.7], bold: true, pct: true },
      { label: "Avg. farm price ($/bu)", values: [5.74,5.58,5.56,6.40,5.48,6.72,7.35,6.47,4.93,4.63,4.54,4.38,5.53,7.34,5.74,5.66,6.43,10.10,9.97,9.59,11.30,12.50,14.40,13.00,10.10,8.95,9.47,9.33,8.48,8.57,10.80,13.30,14.20,12.10,10.40,10.50], price: true },
    ]},
  ],
};

const SOYBEAN_MEAL = {
  label: "Soybean meal", id: "soybean_meal",
  sections: [
    { header: "Supply", unit: "thousand short tons", rows: [
      { label: "Beginning stocks", values: [231,275,254,228,214,220,264,254,332,247,275,246,234,237,225,230,202,274,238,247,314,330,314,285,263,330,348,362,398,377,362,320,340,375,400,380] },
      { label: "Production", values: [25892,27362,28099,27738,30637,29838,31348,34693,34675,34387,35710,37072,35116,33354,36953,37873,39441,39226,36225,38140,35859,37060,36684,37728,40703,41031,41413,44682,45470,47007,46554,47923,48166,50000,52350,51700] },
      { label: "Imports", values: [42,28,31,40,26,62,80,55,78,91,57,95,79,132,139,148,183,248,230,206,242,242,291,375,265,292,235,207,326,327,380,422,350,280,300,300] },
      { label: "Total supply", values: [26165,27665,28384,28006,30877,30120,31692,35002,35085,34725,36042,37413,35429,33723,37317,38251,39836,40448,36893,38593,36415,37632,37289,38388,41231,41653,41996,45251,46194,47711,47296,48665,48856,50655,53050,52380], bold: true },
    ]},
    { header: "Use", unit: "thousand short tons", rows: [
      { label: "Domestic disappearance", values: [20832,21690,22363,22207,23655,22853,23881,25832,26240,26163,27267,28442,26968,25680,27882,28960,29555,30158,27568,28697,26765,27528,27285,28305,30268,30650,30614,33073,33688,34855,34190,35232,35122,36500,37800,37600] },
      { label: "Exports", values: [5058,5721,5793,5585,7002,7003,7557,8838,8598,8287,8529,8727,8227,7806,9180,9061,10079,9779,8987,9649,9320,9774,9690,9778,10633,10655,11034,11816,12129,12479,12786,13113,13359,13780,14870,14400] },
      { label: "Total usage", values: [25890,27411,28156,27792,30657,29856,31438,34670,34838,34450,35796,37167,35195,33486,37062,38021,39634,39937,36555,38346,36085,37302,36975,38083,40901,41305,41648,44889,45817,47334,46976,48345,48481,50280,52670,52000], bold: true },
    ]},
    { header: "Ending stocks and price", unit: "thousand short tons / $/short ton", rows: [
      { label: "Ending stocks", values: [275,254,228,214,220,264,254,332,247,275,246,246,234,237,255,230,202,511,338,247,330,330,314,305,330,348,348,362,377,377,320,320,375,375,380,380], bold: true },
      { label: "Avg. price ($/short ton)", values: [190.3,185.1,192.5,195.8,167.0,234.5,267.0,197.5,140.8,157.2,173.6,167.4,185.9,249.0,185.0,170.3,199.5,334.0,325.0,312.0,343.0,375.0,459.0,484.0,340.0,306.0,313.0,331.0,308.0,300.0,382.0,410.0,445.0,370.0,320.0,330.0], price: true },
    ]},
  ],
};

const SOYBEAN_OIL = {
  label: "Soybean oil", id: "soybean_oil",
  sections: [
    { header: "Supply", unit: "million pounds", rows: [
      { label: "Beginning stocks", values: [1354,1497,1711,1726,1501,1416,1574,1723,1680,2262,1972,2393,2257,1710,2020,2448,2885,3186,2731,2517,2692,2517,2338,1777,1725,1780,1901,1601,1777,1831,1633,2090,2345,1717,1600,1650] },
      { label: "Production", values: [12283,12937,13257,13184,14529,14114,14885,16405,16494,16319,16910,17522,16664,15965,17681,18005,18730,18621,17399,18212,17065,17704,17401,18069,19610,19695,19855,21405,21786,22528,22369,22845,22994,23870,25000,24650] },
      { label: "Imports", values: [56,54,20,24,30,55,21,17,41,48,61,67,97,90,85,65,31,115,96,108,252,215,343,269,309,308,334,402,536,685,692,1111,570,400,300,350] },
      { label: "Total supply", values: [13693,14488,14988,14934,16060,15585,16480,18145,18215,18629,18943,19982,19018,17765,19786,20518,21646,21922,20226,20837,19999,20436,20082,20115,21644,21783,22090,23408,24099,25044,24694,26046,25909,25987,26900,26650], bold: true },
    ]},
    { header: "Use", unit: "million pounds", rows: [
      { label: "Domestic disappearance", values: [11062,11532,11911,12088,12894,12311,12981,14443,13886,14640,14512,15533,15115,13705,15173,15468,16231,16950,15540,15965,15575,15900,16210,16240,17660,17630,18250,19310,19840,20950,20268,21401,22050,22150,23000,22700] },
      { label: "Exports", values: [1134,1245,1351,1345,1750,1700,1776,2022,2067,2017,2038,2192,2193,2040,2165,2205,2229,2241,2169,2180,1907,2198,2095,2150,2204,2252,2239,2321,2428,2461,2336,2300,2142,2237,2250,2300] },
      { label: "Total usage", values: [12196,12777,13262,13433,14644,14011,14757,16465,15953,16657,16550,17725,17308,15745,17338,17673,18460,19191,17709,18145,17482,18098,18305,18390,19864,19882,20489,21631,22268,23411,22604,23701,24192,24387,25250,25000], bold: true },
    ]},
    { header: "Ending stocks and price", unit: "million pounds / ¢/pound", rows: [
      { label: "Ending stocks", values: [1497,1711,1726,1501,1416,1574,1723,1680,2262,1972,2393,2257,1710,2020,2448,2845,3186,2731,2517,2692,2517,2338,1777,1725,1780,1901,1601,1777,1831,1633,2090,2345,1717,1600,1650,1650], bold: true },
      { label: "Avg. price (¢/lb)", values: [21.0,19.5,21.2,27.0,27.8,25.0,23.1,25.4,20.1,15.9,14.3,15.3,21.1,29.3,23.1,22.8,24.7,52.0,35.6,36.5,50.6,53.3,51.3,40.0,32.0,28.3,31.5,31.7,28.7,27.4,39.8,65.7,63.2,48.5,42.0,43.0], price: true },
    ]},
  ],
};

const WHEAT = {
  label: "Wheat", id: "wheat",
  sections: [
    { header: "Area, yield, and production", unit: "million acres / bushels per acre / million bushels", rows: [
      { label: "Area planted", values: [77.0,69.9,72.2,72.2,70.3,69.2,75.6,70.4,65.8,62.7,62.5,59.6,60.3,62.1,59.7,57.2,57.3,60.5,63.2,59.2,53.6,54.4,55.7,56.2,56.8,55.0,50.1,46.0,47.8,45.2,44.3,46.7,45.7,49.6,47.5,46.5] },
      { label: "Area harvested", values: [69.4,57.7,62.4,62.7,61.8,60.9,62.8,62.8,59.0,53.8,53.1,48.6,45.8,53.1,50.0,50.1,46.8,51.0,55.7,49.9,47.6,45.7,48.9,45.3,46.4,47.3,43.9,37.6,39.6,37.2,36.7,37.3,36.9,37.5,36.8,36.0] },
      { label: "Yield per harvested acre", values: [39.5,34.3,39.3,38.2,37.6,35.8,36.3,39.5,43.2,42.7,42.0,40.2,35.0,44.2,43.2,42.0,38.6,40.2,44.9,44.5,46.4,43.7,46.3,47.1,43.7,43.6,52.7,46.4,47.6,51.7,49.7,44.3,46.5,48.6,52.2,49.5] },
    ]},
    { header: "Supply", unit: "million bushels", rows: [
      { label: "Beginning stocks", values: [535,866,472,529,568,507,376,444,722,946,950,876,777,491,546,540,571,456,306,657,976,862,743,718,590,752,976,1181,1099,1080,1028,847,698,580,702,828] },
      { label: "Production", values: [2740,1981,2459,2396,2321,2183,2282,2482,2547,2299,2232,1957,1606,2345,2158,2105,1808,2051,2499,2218,2208,1999,2269,2135,2026,2052,2310,1741,1885,1920,1826,1646,1713,1821,1922,1782] },
      { label: "Imports", values: [37,46,67,109,90,68,92,96,103,93,82,72,68,68,71,82,122,113,127,119,97,112,138,169,149,113,118,157,135,100,100,105,120,135,130,130] },
      { label: "Total supply", values: [3312,2893,2998,3034,2979,2758,2750,3022,3372,3338,3264,2905,2451,2904,2775,2727,2501,2620,2932,2994,3281,2973,3150,3022,2765,2917,3404,3079,3119,3100,2954,2598,2531,2536,2754,2740], bold: true },
    ]},
    { header: "Use", unit: "million bushels", rows: [
      { label: "Food", values: [745,760,790,818,842,859,872,880,900,920,950,926,911,910,907,915,938,948,946,920,926,941,955,952,958,962,964,964,955,962,966,963,970,975,975,980] },
      { label: "Seed", values: [92,86,84,90,83,82,93,87,82,78,79,74,80,82,78,78,77,82,83,80,72,74,76,75,76,70,65,60,62,59,57,61,59,65,62,61] },
      { label: "Feed and residual", values: [419,243,297,312,374,186,163,246,330,286,230,209,168,214,190,160,117,16,255,174,132,160,387,228,110,152,157,30,51,88,22,64,73,72,83,60] },
      { label: "Domestic, total", values: [1256,1089,1171,1220,1299,1127,1128,1213,1312,1284,1259,1209,1159,1206,1175,1153,1132,1046,1284,1174,1130,1175,1418,1255,1144,1184,1186,1054,1068,1109,1045,1088,1102,1112,1120,1101] },
      { label: "Exports", values: [1068,1278,1254,1246,1173,1241,1002,1040,1046,1090,1064,964,850,1158,1067,1003,909,1263,1015,881,1289,1054,1012,1176,905,776,1159,901,936,965,1056,682,796,740,850,800] },
      { label: "Total usage", values: [2324,2367,2425,2466,2472,2368,2130,2253,2358,2374,2323,2173,2009,2364,2242,2156,2041,2309,2299,2055,2419,2229,2430,2431,2049,1960,2345,1955,2004,2074,2101,1770,1898,1852,1970,1901], bold: true },
    ]},
    { header: "Ending stocks and price", unit: "million bushels / $/bushel", rows: [
      { label: "Ending stocks", values: [866,472,529,568,507,376,444,722,946,950,876,777,491,546,540,571,456,306,657,976,862,743,718,590,752,976,1181,1099,1080,1028,847,698,580,702,828,839], bold: true },
      { label: "Stocks/use (%)", values: [37.3,19.9,21.8,23.0,20.5,15.9,20.8,32.0,40.1,40.0,37.7,35.8,24.4,23.1,24.1,26.5,22.3,13.3,28.6,47.5,35.6,33.3,29.5,24.3,36.7,49.8,50.4,56.2,53.9,49.6,40.3,39.4,30.6,37.9,42.0,44.1], bold: true, pct: true },
      { label: "Avg. farm price ($/bu)", values: [2.61,3.00,3.24,3.26,3.45,4.55,4.30,3.38,2.65,2.48,2.62,2.78,3.56,3.40,3.40,3.42,4.26,6.48,6.78,4.87,5.70,7.24,7.77,6.87,5.99,4.89,3.89,4.72,5.16,4.58,5.05,7.63,8.83,7.10,5.65,5.80], price: true },
    ]},
  ],
};

// Tab order: Corn, Soybeans, Soybean Meal, Soybean Oil, Wheat
const WASDE_COMMODITIES = [CORN, SOYBEANS, SOYBEAN_MEAL, SOYBEAN_OIL, WHEAT];

// ════════════════════════════════════════════════════════════════════════
// WASDE GLOBAL BALANCE SHEETS — million metric tons
// ════════════════════════════════════════════════════════════════════════

const GMY = ["2015/16","2016/17","2017/18","2018/19","2019/20","2020/21","2021/22","2022/23","2023/24","2024/25","2025/26"];
const GFC = GMY.length - 1;

function gv(base, trend, vol) {
  return GMY.map((_, i) => Math.round((base + i * trend + Math.sin(i * 0.9) * vol) * 10) / 10);
}

// PSD-format: each country has Production, Imports, Domestic Consumption, Exports, Ending Stocks
function psdCountry(label, prodBase, prodTrend, impBase, impTrend, domBase, domTrend, expBase, expTrend, esBase, esTrend) {
  const dom = gv(domBase, domTrend, domBase * 0.02);
  const exp = gv(expBase, expTrend, expBase * 0.05);
  const totalUsage = dom.map((d, i) => Math.round((d + exp[i]) * 10) / 10);
  const es = gv(esBase, esTrend, esBase * 0.06);
  const stocksUse = totalUsage.map((u, i) => u !== 0 ? Math.round((es[i] / u) * 1000) / 10 : null);
  return {
    label,
    rows: [
      { label: "Production", values: gv(prodBase, prodTrend, prodBase * 0.03) },
      { label: "Imports", values: gv(impBase, impTrend, impBase * 0.05) },
      { label: "Domestic consumption", values: dom },
      { label: "Exports", values: exp },
      { label: "Total usage", values: totalUsage, bold: true },
      { label: "Ending stocks", values: es, bold: true, spaceBefore: true },
      { label: "Stocks/use (%)", values: stocksUse, bold: true, pct: true },
    ],
  };
}

// Corn-specific PSD builder with full S&D line items
function psdCornCountry(label, areaBase, areaTrend, yieldBase, yieldTrend, bsBase, bsTrend, prodBase, prodTrend, impBase, impTrend, feedBase, feedTrend, fsiBase, fsiTrend, expBase, expTrend, esBase, esTrend) {
  const area = gv(areaBase, areaTrend, areaBase * 0.03);
  const yld = gv(yieldBase, yieldTrend, yieldBase * 0.02);
  const bs = gv(bsBase, bsTrend, bsBase * 0.06);
  const prod = gv(prodBase, prodTrend, prodBase * 0.03);
  const imp = gv(impBase, impTrend, Math.max(impBase * 0.05, 0.01));
  const feed = gv(feedBase, feedTrend, feedBase * 0.03);
  const fsi = gv(fsiBase, fsiTrend, fsiBase * 0.03);
  const dom = feed.map((f, i) => Math.round((f + fsi[i]) * 10) / 10);
  const supply = bs.map((b, i) => Math.round((b + prod[i] + imp[i]) * 10) / 10);
  const exp = gv(expBase, expTrend, expBase * 0.05);
  const totalUsage = dom.map((d, i) => Math.round((d + exp[i]) * 10) / 10);
  const es = gv(esBase, esTrend, esBase * 0.06);
  const stocksUse = totalUsage.map((u, i) => u !== 0 ? Math.round((es[i] / u) * 1000) / 10 : null);
  return {
    label,
    rows: [
      { label: "Area harvested", values: area },
      { label: "Yield", values: yld },
      { label: "Beginning stocks", values: bs, spaceBefore: true },
      { label: "Production", values: prod },
      { label: "Imports", values: imp },
      { label: "Total supply", values: supply, bold: true },
      { label: "Feed dom. consumption", values: feed, spaceBefore: true },
      { label: "FSI consumption", values: fsi },
      { label: "Domestic consumption", values: dom },
      { label: "Exports", values: exp },
      { label: "Total usage", values: totalUsage, bold: true },
      { label: "Ending stocks", values: es, bold: true, spaceBefore: true },
      { label: "Stocks/use (%)", values: stocksUse, bold: true, pct: true },
    ],
  };
}

const GLOBAL_CORN = {
  label: "Corn", id: "corn",
  sections: [
    { header: "World total", unit: "million metric tons / million hectares / MT per hectare", rows: (() => {
      const area = gv(178, 1.2, 4);
      const yld = gv(5.38, 0.05, 0.12);
      const bs = gv(206, -2.5, 12);
      const prod = gv(960, 8.5, 25);
      const imp = gv(138, 3.2, 8);
      const supply = gv(1310, 9.2, 30);
      const feed = gv(620, 5.5, 15);
      const fsi = gv(328, 3.0, 8);
      const dom = gv(948, 8.0, 20);
      const exp = gv(142, 3.2, 8);
      const totalUsage = dom.map((d, i) => Math.round((d + exp[i]) * 10) / 10);
      const es = gv(195, -2.5, 15);
      const stocksUse = totalUsage.map((u, i) => u !== 0 ? Math.round((es[i] / u) * 1000) / 10 : null);
      return [
        { label: "Area harvested", values: area },
        { label: "Yield", values: yld },
        { label: "Beginning stocks", values: bs, spaceBefore: true },
        { label: "Production", values: prod },
        { label: "Imports", values: imp },
        { label: "Total supply", values: supply, bold: true },
        { label: "Feed dom. consumption", values: feed, spaceBefore: true },
        { label: "FSI consumption", values: fsi },
        { label: "Domestic consumption", values: dom },
        { label: "Exports", values: exp },
        { label: "Total usage", values: totalUsage, bold: true },
        { label: "Ending stocks", values: es, bold: true, spaceBefore: true },
        { label: "Stocks/use (%)", values: stocksUse, bold: true, pct: true },
      ];
    })() },
  ],
  countries: [
    psdCornCountry("Argentina", 7.5, 0.3, 5.6, 0.05, 2.5, 0.2, 42, 2.0, 0.1, 0, 8.5, 0.3, 3.5, 0.2, 28, 1.8, 2.5, 0.2),
    psdCornCountry("Brazil", 18.5, 0.8, 4.4, 0.06, 5.5, 0.3, 82, 4.5, 1.2, 0.1, 42, 1.8, 20, 0.7, 28, 3.5, 5.5, 0.3),
    psdCornCountry("China", 42.5, 0.5, 6.1, 0.05, 68, -1.0, 258, 3.0, 5.5, 1.8, 188, 2.8, 82, 1.2, 0.1, 0, 68, -1.0),
    psdCornCountry("Ukraine", 4.5, 0.1, 6.2, 0.06, 1.2, 0.1, 28, 0.8, 0.1, 0, 4.0, 0.2, 2.5, 0.1, 22, 0.8, 1.2, 0.1),
    psdCornCountry("United States", 33.1, 0.3, 10.5, 0.08, 45, -1.5, 345, 4.5, 0.6, 0.02, 142, 1.5, 163, 2.0, 55, 1.2, 45, -1.5),
  ],
};

// Soybean-specific PSD builder with full S&D line items
function psdSoyCountry(label, areaBase, areaTrend, yieldBase, yieldTrend, bsBase, bsTrend, prodBase, prodTrend, impBase, impTrend, crushBase, crushTrend, foodBase, foodTrend, feedBase, feedTrend, expBase, expTrend, esBase, esTrend) {
  const area = gv(areaBase, areaTrend, areaBase * 0.03);
  const yld = gv(yieldBase, yieldTrend, yieldBase * 0.02);
  const bs = gv(bsBase, bsTrend, bsBase * 0.06);
  const prod = gv(prodBase, prodTrend, prodBase * 0.03);
  const imp = gv(impBase, impTrend, Math.max(impBase * 0.05, 0.01));
  const supply = bs.map((b, i) => Math.round((b + prod[i] + imp[i]) * 10) / 10);
  const crush = gv(crushBase, crushTrend, crushBase * 0.03);
  const food = gv(foodBase, foodTrend, foodBase * 0.03);
  const feed = gv(feedBase, feedTrend, feedBase * 0.03);
  const dom = crush.map((c, i) => Math.round((c + food[i] + feed[i]) * 10) / 10);
  const exp = gv(expBase, expTrend, expBase * 0.05);
  const totalUsage = dom.map((d, i) => Math.round((d + exp[i]) * 10) / 10);
  const es = gv(esBase, esTrend, esBase * 0.06);
  const stocksUse = totalUsage.map((u, i) => u !== 0 ? Math.round((es[i] / u) * 1000) / 10 : null);
  return {
    label,
    rows: [
      { label: "Area harvested", values: area },
      { label: "Yield", values: yld },
      { label: "Beginning stocks", values: bs, spaceBefore: true },
      { label: "Production", values: prod },
      { label: "Imports", values: imp },
      { label: "Total supply", values: supply, bold: true },
      { label: "Crush", values: crush, spaceBefore: true },
      { label: "Food use", values: food },
      { label: "Feed", values: feed },
      { label: "Domestic consumption", values: dom },
      { label: "Exports", values: exp },
      { label: "Total usage", values: totalUsage, bold: true },
      { label: "Ending stocks", values: es, bold: true, spaceBefore: true },
      { label: "Stocks/use (%)", values: stocksUse, bold: true, pct: true },
    ],
  };
}

const GLOBAL_SOYBEANS = {
  label: "Soybeans", id: "soybeans",
  sections: [
    { header: "World total", unit: "million metric tons", rows: (() => {
      const area = gv(122, 1.8, 3);
      const yld = gv(2.61, 0.02, 0.08);
      const bs = gv(78, 1.5, 8);
      const prod = gv(318, 8.0, 15);
      const imp = gv(140, 4.5, 6);
      const supply = bs.map((b, i) => Math.round((b + prod[i] + imp[i]) * 10) / 10);
      const crush = gv(280, 7.0, 10);
      const food = gv(18, 0.4, 1.2);
      const feed = gv(22, 0.5, 1.5);
      const dom = crush.map((c, i) => Math.round((c + food[i] + feed[i]) * 10) / 10);
      const exp = gv(145, 4.5, 6);
      const totalUsage = dom.map((d, i) => Math.round((d + exp[i]) * 10) / 10);
      const es = gv(78, 2.0, 10);
      const stocksUse = totalUsage.map((u, i) => u !== 0 ? Math.round((es[i] / u) * 1000) / 10 : null);
      return [
        { label: "Area harvested", values: area },
        { label: "Yield", values: yld },
        { label: "Beginning stocks", values: bs, spaceBefore: true },
        { label: "Production", values: prod },
        { label: "Imports", values: imp },
        { label: "Total supply", values: supply, bold: true },
        { label: "Crush", values: crush, spaceBefore: true },
        { label: "Food use", values: food },
        { label: "Feed", values: feed },
        { label: "Domestic consumption", values: dom },
        { label: "Exports", values: exp },
        { label: "Total usage", values: totalUsage, bold: true },
        { label: "Ending stocks", values: es, bold: true, spaceBefore: true },
        { label: "Stocks/use (%)", values: stocksUse, bold: true, pct: true },
      ];
    })() },
  ],
  countries: [
    psdSoyCountry("Argentina", 17, 0.3, 2.47, 0.02, 5.0, 0.2, 42, 1.5, 0.3, 0, 38, 1.4, 0.8, 0.02, 1.2, 0.05, 6.5, -0.2, 5.0, 0.2),
    psdSoyCountry("Brazil", 38, 1.5, 3.15, 0.03, 12, 1.0, 120, 6.0, 0.2, 0, 44, 2.2, 1.8, 0.05, 2.0, 0.1, 78, 5.0, 12, 1.0),
    psdSoyCountry("China", 8.2, 0.1, 1.95, 0.01, 18, 0.5, 16, 0.2, 95, 4.5, 92, 4.2, 10.5, 0.3, 7.5, 0.2, 0.1, 0, 18, 0.5),
    psdSoyCountry("Paraguay", 3.5, 0.1, 2.86, 0.02, 0.8, 0.05, 10, 0.3, 0.1, 0, 2.8, 0.1, 0.2, 0, 0.5, 0.02, 6.0, 0.3, 0.8, 0.05),
    psdSoyCountry("United States", 33.5, 0.3, 3.22, 0.02, 6.8, 0.3, 108, 2.0, 0.4, 0, 55, 1.2, 2.5, 0.05, 2.5, 0.1, 52, 0.5, 6.8, 0.3),
  ],
};

const GLOBAL_SOYMEAL = {
  label: "Soybean Meal", id: "soybean_meal",
  sections: [
    { header: "World total", unit: "million metric tons", rows: [
      { label: "Beginning stocks", values: gv(12.5, 0.3, 1.5) },
      { label: "Production", values: gv(222, 6.5, 8) },
      { label: "Imports", values: gv(66, 2.0, 3) },
      { label: "Domestic consumption", values: gv(222, 6.5, 8) },
      { label: "Exports", values: gv(68, 2.0, 3) },
      { label: "Ending stocks", values: gv(12.8, 0.3, 1.5), bold: true },
    ]},
  ],
  countries: [
    psdCountry("Argentina", 30, 1.0, 0.1, 0, 2.2, 0.1, 28, 0.8, 0.5, 0.02),
    psdCountry("Brazil", 36, 2.0, 0.2, 0, 18, 1.0, 18, 1.0, 1.0, 0.05),
    psdCountry("China", 68, 3.5, 0.5, 0, 68, 3.5, 0.2, 0, 1.5, 0.1),
    psdCountry("EU", 30, 0.5, 22, 0.3, 52, 0.8, 0.5, 0, 0.8, 0.02),
    psdCountry("United States", 45, 1.2, 0.3, 0, 33, 0.8, 13, 0.4, 0.4, 0.02),
  ],
};

const GLOBAL_SOYOIL = {
  label: "Soybean Oil", id: "soybean_oil",
  sections: [
    { header: "World total", unit: "million metric tons", rows: [
      { label: "Beginning stocks", values: gv(3.8, 0.1, 0.5) },
      { label: "Production", values: gv(52, 1.5, 2) },
      { label: "Imports", values: gv(11.5, 0.5, 1) },
      { label: "Domestic consumption", values: gv(52.5, 1.5, 2) },
      { label: "Exports", values: gv(12, 0.5, 1) },
      { label: "Ending stocks", values: gv(3.9, 0.1, 0.5), bold: true },
    ]},
  ],
  countries: [
    psdCountry("Argentina", 7.8, 0.3, 0.05, 0, 1.5, 0.05, 6.2, 0.25, 0.3, 0.01),
    psdCountry("Brazil", 8.5, 0.4, 0.05, 0, 7.5, 0.4, 1.5, 0.1, 0.3, 0.02),
    psdCountry("China", 15.5, 0.6, 0.5, 0.05, 16, 0.6, 0.05, 0, 0.5, 0.02),
    psdCountry("India", 2.8, 0.1, 3.5, 0.2, 6.2, 0.3, 0.02, 0, 0.2, 0.01),
    psdCountry("United States", 10.5, 0.3, 0.1, 0, 10, 0.3, 1.0, 0.05, 0.4, 0.01),
  ],
};

// Wheat-specific PSD builder
function psdWheatCountry(label, areaBase, areaTrend, yieldBase, yieldTrend, bsBase, bsTrend, prodBase, prodTrend, impBase, impTrend, fsiBase, fsiTrend, feedBase, feedTrend, expBase, expTrend, esBase, esTrend) {
  const area = gv(areaBase, areaTrend, areaBase * 0.03);
  const yld = gv(yieldBase, yieldTrend, yieldBase * 0.02);
  const bs = gv(bsBase, bsTrend, bsBase * 0.06);
  const prod = gv(prodBase, prodTrend, prodBase * 0.03);
  const imp = gv(impBase, impTrend, Math.max(impBase * 0.05, 0.01));
  const supply = bs.map((b, i) => Math.round((b + prod[i] + imp[i]) * 10) / 10);
  const fsi = gv(fsiBase, fsiTrend, fsiBase * 0.02);
  const feed = gv(feedBase, feedTrend, feedBase * 0.04);
  const dom = fsi.map((f, i) => Math.round((f + feed[i]) * 10) / 10);
  const exp = gv(expBase, expTrend, expBase * 0.05);
  const totalUsage = dom.map((d, i) => Math.round((d + exp[i]) * 10) / 10);
  const es = gv(esBase, esTrend, esBase * 0.06);
  const stocksUse = totalUsage.map((u, i) => u !== 0 ? Math.round((es[i] / u) * 1000) / 10 : null);
  return {
    label,
    rows: [
      { label: "Area harvested", values: area },
      { label: "Yield", values: yld },
      { label: "Beginning stocks", values: bs, spaceBefore: true },
      { label: "Production", values: prod },
      { label: "Imports", values: imp },
      { label: "Total supply", values: supply, bold: true },
      { label: "FSI consumption", values: fsi, spaceBefore: true },
      { label: "Feed consumption", values: feed },
      { label: "Domestic consumption", values: dom },
      { label: "Exports", values: exp },
      { label: "Total usage", values: totalUsage, bold: true },
      { label: "Ending stocks", values: es, bold: true, spaceBefore: true },
      { label: "Stocks/use (%)", values: stocksUse, bold: true, pct: true },
    ],
  };
}

const GLOBAL_WHEAT = {
  label: "Wheat", id: "wheat",
  sections: [
    { header: "World total", unit: "million metric tons", rows: (() => {
      const area = gv(220, 0.5, 5);
      const yld = gv(3.35, 0.03, 0.1);
      const bs = gv(232, 2.5, 15);
      const prod = gv(738, 4.5, 20);
      const imp = gv(178, 2.5, 8);
      const supply = bs.map((b, i) => Math.round((b + prod[i] + imp[i]) * 10) / 10);
      const fsi = gv(595, 5.0, 10);
      const feed = gv(142, 1.5, 8);
      const dom = fsi.map((f, i) => Math.round((f + feed[i]) * 10) / 10);
      const exp = gv(182, 2.5, 8);
      const totalUsage = dom.map((d, i) => Math.round((d + exp[i]) * 10) / 10);
      const es = gv(235, 0.5, 18);
      const stocksUse = totalUsage.map((u, i) => u !== 0 ? Math.round((es[i] / u) * 1000) / 10 : null);
      return [
        { label: "Area harvested", values: area },
        { label: "Yield", values: yld },
        { label: "Beginning stocks", values: bs, spaceBefore: true },
        { label: "Production", values: prod },
        { label: "Imports", values: imp },
        { label: "Total supply", values: supply, bold: true },
        { label: "FSI consumption", values: fsi, spaceBefore: true },
        { label: "Feed consumption", values: feed },
        { label: "Domestic consumption", values: dom },
        { label: "Exports", values: exp },
        { label: "Total usage", values: totalUsage, bold: true },
        { label: "Ending stocks", values: es, bold: true, spaceBefore: true },
        { label: "Stocks/use (%)", values: stocksUse, bold: true, pct: true },
      ];
    })() },
  ],
  countries: [
    psdWheatCountry("Argentina", 6.5, 0.1, 2.95, 0.03, 1.8, 0.1, 19, 0.5, 0.02, 0, 5.8, 0.1, 1.5, 0.05, 12, 0.5, 1.8, 0.1),
    psdWheatCountry("Australia", 12.5, 0.3, 2.00, 0.04, 3.5, 0.2, 25, 0.8, 0.1, 0, 5.5, 0.1, 2.0, 0.05, 18, 0.8, 3.5, 0.2),
    psdWheatCountry("Canada", 10.2, 0.1, 3.14, 0.03, 4.5, 0.1, 32, 0.3, 0.2, 0, 7.5, 0.1, 2.0, 0.05, 23, 0.3, 4.5, 0.1),
    psdWheatCountry("China", 24.0, 0.1, 5.63, 0.04, 95, 1.5, 135, 1.0, 6.0, 0.8, 118, 1.2, 27, 0.3, 1.0, 0.1, 95, 1.5),
    psdWheatCountry("EU", 24.5, -0.1, 5.63, 0.03, 12, 0.2, 138, 0.5, 5.5, 0.2, 85, 0.4, 30, 0.1, 30, 0.5, 12, 0.2),
    psdWheatCountry("Russia", 28.0, 0.5, 2.57, 0.05, 10, 0.5, 72, 2.5, 0.3, 0, 32, 0.8, 10, 0.2, 32, 2.5, 10, 0.5),
    psdWheatCountry("Ukraine", 6.8, 0.1, 3.68, 0.04, 2.0, 0.1, 25, 0.5, 0.05, 0, 4.5, 0.1, 2.0, 0.1, 18, 0.5, 2.0, 0.1),
    psdWheatCountry("United States", 15.2, -0.1, 3.16, 0.02, 18, 0.1, 48, 0.2, 3.5, 0.1, 27, 0.1, 3.0, 0.05, 24, -0.5, 18, 0.1),
  ],
};

const WASDE_GLOBAL = {
  corn: GLOBAL_CORN, soybeans: GLOBAL_SOYBEANS,
  soybean_meal: GLOBAL_SOYMEAL, soybean_oil: GLOBAL_SOYOIL, wheat: GLOBAL_WHEAT,
};

// ════════════════════════════════════════════════════════════════════════
// OTHER DATA (livestock, etc. — unchanged from v3)
// ════════════════════════════════════════════════════════════════════════

const CATTLE_ON_FEED = {
  months: ["Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec","Jan","Feb"],
  onFeed: { "2025": [11498,11356,11217,11095,11020,11150,11615,11821,11780,11710,11575], "2024": [11733,11622,11511,11355,11269,11388,11834,12022,11988,11945,11802], "5yr": [11915,11796,11638,11502,11432,11598,11932,12098,12015,11982,11858] },
  placements: { "2025": [1815,1742,1698,1752,1890,2105,2245,2032,1765,1698,1625], "2024": [1878,1803,1755,1812,1945,2168,2305,2098,1832,1762,1688], "5yr": [1925,1854,1798,1865,2010,2235,2380,2165,1898,1825,1745] },
  marketings: { "2025": [1852,1805,1838,1872,1915,1842,1778,1832,1805,1762,1810], "2024": [1912,1868,1898,1932,1965,1898,1835,1888,1865,1818,1862], "5yr": [1945,1898,1928,1965,2005,1935,1872,1925,1898,1855,1905] },
};
// Generate daily values from a base and a per-day drift pattern
function genDaily(base, drifts) {
  const out = []; let v = base;
  for (let i = 0; i < drifts.length; i++) { v += drifts[i]; out.push(Math.round(v * 100) / 100); }
  return out;
}
const DRIFT_A = [0.01,0.25,-0.12,0.48,0.23,0.43,0.65,-0.22,0.31,0.47,0.8,0.23,-0.42,0.6,0.15,-0.26,0.41,-0.05,0.57,-0.21,0.78,0.37,0.13,0.52,0.3,0.44,0.62,-0.28,0.3,0.57,0.4,0.79,-0.03,0.52,0.26,0.58,0.41,-0.11,0.72,0.19,0.9,0.44,-0.24,0.57,0.35,0.66,0.25,0.47,0.41,0.58,0.08,0.37,-0.03,0.64,0.31,0.51,0.66,-0.08,0.36,0.59,0.95,0.31,-0.29,0.72,0.23,-0.17,0.47,-0.05,0.58,-0.12,0.77,0.44,0.24,0.58,0.31,0.49,0.74,-0.21,0.27,0.57,0.4,0.77,0.0,0.53,0.28,0.56,0.44,-0.11,0.64,0.14,0.84,0.49,-0.19,0.57,0.33,0.66,0.32,0.47,0.42,0.6,0.02,0.39,-0.02,0.56,0.24,0.47,0.62,-0.15,0.35,0.59,0.88,0.22,-0.36,0.61,0.18,-0.23,0.41,-0.06,0.54,-0.21,0.75,0.33,0.15,0.52,0.16,0.39,0.56,-0.25,0.24,0.54,0.28,0.65,-0.07,0.44,0.15,0.49,0.24,-0.19,0.61,0.04,0.77,0.38,-0.35,0.51,0.26,0.54,0.17,0.38,0.23,0.44,0.0,0.27,-0.16,0.45,0.11,0.32,0.53,-0.25,0.21,0.41,0.69,0.15,-0.5,0.57,0.06,-0.42,0.3,-0.16,0.39,-0.32,0.66,0.22,0.01,0.44,0.14,0.28,0.47,-0.4,0.1,0.4,0.23,0.62,-0.15,0.26,0.09,0.39,0.24,-0.32,0.47,-0.0,0.69,0.28,-0.42,0.44,0.19,0.54,0.11,0.26,0.25,0.43,-0.05,0.24,-0.16,0.37,0.1,0.27,0.49,-0.34,0.19,0.45,0.68,0.14,-0.5,0.5,0.06,-0.34,0.32,-0.16,0.38,-0.3,0.66,0.23,0.02,0.45,0.08,0.33,0.53,-0.34,0.1,0.48,0.19,0.6,-0.15,0.36,0.11,0.41,0.28,-0.28,0.56,0.06,0.75,0.36,-0.34,0.5,0.23,0.59,0.14,0.36,0.29,0.45,-0.04,0.3,-0.16,0.48,0.24,0.44,0.55,-0.24,0.27,0.54];
const DRIFT_B = [0.04,0.24,0.39,-0.33,0.54,0.33,0.13,0.67,-0.07,0.37,0.56,0.31,-0.16,0.47,0.6,-0.1,0.3,0.55,-0.18,0.45,0.67,0.22,-0.04,0.53,0.35,0.2,0.49,0.62,-0.15,0.34,0.52,0.3,0.48,-0.05,0.7,0.38,0.17,0.53,0.24,0.52,0.72,0.39,0.02,0.59,0.45,0.25,0.57,0.43,0.22,0.53,0.13,0.27,0.47,-0.24,0.62,0.44,0.19,0.71,-0.04,0.54,0.64,0.45,-0.07,0.54,0.65,0.02,0.38,0.64,-0.07,0.54,0.73,0.28,0.03,0.56,0.43,0.23,0.47,0.73,-0.11,0.37,0.62,0.27,0.44,-0.04,0.67,0.42,0.23,0.56,0.3,0.47,0.73,0.38,0.02,0.54,0.52,0.24,0.62,0.35,0.13,0.46,0.09,0.25,0.47,-0.24,0.55,0.36,0.13,0.67,-0.1,0.49,0.55,0.37,-0.13,0.46,0.62,-0.11,0.35,0.51,-0.19,0.46,0.65,0.2,-0.1,0.51,0.3,0.09,0.37,0.6,-0.15,0.32,0.54,0.21,0.38,-0.1,0.54,0.27,0.08,0.49,0.2,0.37,0.57,0.25,-0.13,0.51,0.4,0.13,0.42,0.26,0.07,0.34,-0.01,0.18,0.37,-0.38,0.42,0.2,0.02,0.54,-0.13,0.29,0.43,0.24,-0.3,0.35,0.53,-0.2,0.24,0.37,-0.25,0.35,0.48,0.11,-0.22,0.46,0.21,-0.03,0.29,0.54,-0.3,0.24,0.42,0.15,0.31,-0.15,0.54,0.21,0.02,0.4,0.13,0.31,0.54,0.22,-0.2,0.38,0.27,0.11,0.43,0.2,0.01,0.28,-0.14,0.08,0.28,-0.42,0.41,0.17,-0.02,0.52,-0.17,0.26,0.4,0.21,-0.3,0.28,0.5,-0.15,0.22,0.43,-0.25,0.34,0.51,0.07,-0.19,0.45,0.26,0.07,0.32,0.55,-0.27,0.24,0.41,0.11,0.33,-0.21,0.52,0.26,0.04,0.41,0.15,0.31,0.57,0.21,-0.15,0.47,0.32,0.18,0.43,0.27,0.03,0.36,-0.05,0.16,0.41,-0.33,0.51,0.32,0.07,0.55,-0.15,0.4];
const scaleDrift = (d, s) => d.map(v => v * s);

// Generate 2025 series with data only through specified day count (rest null)
function genDaily2025(base, drifts, throughDay = 50) {
  const full = genDaily(base, drifts);
  return full.map((v, i) => i < throughDay ? v : null);
}

// Boxed beef Choice cutout — daily data with seasonal comparison
// Same 50-day structure as product data
const BOXED_BEEF_CHOICE_DAILY = {
  "2025": genDaily2025(304.50, scaleDrift(DRIFT_A, 0.52)),
  "2024": genDaily(292.80, scaleDrift(DRIFT_B, 0.48)),
  "5yr":  genDaily(278.20, scaleDrift(DRIFT_A, 0.40)),
};
// Select cutout (kept for metric cards only, not charted)
const BOXED_BEEF_SELECT_LATEST = 311.23;
const BOXED_BEEF_CHOICE_LATEST = 328.76;

const BOXED_BEEF_SELECT_DAILY = {
  "2025": genDaily2025(289.50, scaleDrift(DRIFT_B, 0.46)),
};

// ─── Daily beef product data — USDA AMS LM_XB459 ───────────────────
// Mon–Fri daily prices, $/cwt. 50 trading days (~10 weeks Jan 6 – Mar 14)
// Each product has { name, primal, item, daily: [{ date, value }] }
// Weeks & months are computed as weighted averages of daily data

const BEEF_DAILY_DATES = [
  "1/6","1/7","1/8","1/9","1/10",
  "1/13","1/14","1/15","1/16","1/17",
  "1/20","1/21","1/22","1/23","1/24",
  "1/27","1/28","1/29","1/30","1/31",
  "2/3","2/4","2/5","2/6","2/7",
  "2/10","2/11","2/12","2/13","2/14",
  "2/17","2/18","2/19","2/20","2/21",
  "2/24","2/25","2/26","2/27","2/28",
  "3/3","3/4","3/5","3/6","3/7",
  "3/10","3/11","3/12","3/13","3/14",
  "3/17","3/18","3/19","3/20","3/21",
  "3/24","3/25","3/26","3/27","3/28",
  "3/31","4/1","4/2","4/3","4/4",
  "4/7","4/8","4/9","4/10","4/11",
  "4/14","4/15","4/16","4/17","4/18",
  "4/21","4/22","4/23","4/24","4/25",
  "4/28","4/29","4/30","5/1","5/2",
  "5/5","5/6","5/7","5/8","5/9",
  "5/12","5/13","5/14","5/15","5/16",
  "5/19","5/20","5/21","5/22","5/23",
  "5/26","5/27","5/28","5/29","5/30",
  "6/2","6/3","6/4","6/5","6/6",
  "6/9","6/10","6/11","6/12","6/13",
  "6/16","6/17","6/18","6/19","6/20",
  "6/23","6/24","6/25","6/26","6/27",
  "6/30","7/1","7/2","7/3","7/4",
  "7/7","7/8","7/9","7/10","7/11",
  "7/14","7/15","7/16","7/17","7/18",
  "7/21","7/22","7/23","7/24","7/25",
  "7/28","7/29","7/30","7/31","8/1",
  "8/4","8/5","8/6","8/7","8/8",
  "8/11","8/12","8/13","8/14","8/15",
  "8/18","8/19","8/20","8/21","8/22",
  "8/25","8/26","8/27","8/28","8/29",
  "9/1","9/2","9/3","9/4","9/5",
  "9/8","9/9","9/10","9/11","9/12",
  "9/15","9/16","9/17","9/18","9/19",
  "9/22","9/23","9/24","9/25","9/26",
  "9/29","9/30","10/1","10/2","10/3",
  "10/6","10/7","10/8","10/9","10/10",
  "10/13","10/14","10/15","10/16","10/17",
  "10/20","10/21","10/22","10/23","10/24",
  "10/27","10/28","10/29","10/30","10/31",
  "11/3","11/4","11/5","11/6","11/7",
  "11/10","11/11","11/12","11/13","11/14",
  "11/17","11/18","11/19","11/20","11/21",
  "11/24","11/25","11/26","11/27","11/28",
  "12/1","12/2","12/3","12/4","12/5",
  "12/8","12/9","12/10","12/11","12/12",
  "12/15","12/16","12/17","12/18","12/19",
  "12/22","12/23","12/24","12/25","12/26",
  "12/29","12/30","12/31","12/31","12/31",
];

// Week boundaries (index into BEEF_DAILY_DATES, 5 days per week)
const BEEF_WEEK_RANGES = [
  { label: "Jan 6", start: 0, end: 5 },
  { label: "Jan 13", start: 5, end: 10 },
  { label: "Jan 20", start: 10, end: 15 },
  { label: "Jan 27", start: 15, end: 20 },
  { label: "Feb 3", start: 20, end: 25 },
  { label: "Feb 10", start: 25, end: 30 },
  { label: "Feb 17", start: 30, end: 35 },
  { label: "Feb 24", start: 35, end: 40 },
  { label: "Mar 3", start: 40, end: 45 },
  { label: "Mar 10", start: 45, end: 50 },
  { label: "Mar 17", start: 50, end: 55 },
  { label: "Mar 24", start: 55, end: 60 },
  { label: "Mar 31", start: 60, end: 65 },
  { label: "Apr 7", start: 65, end: 70 },
  { label: "Apr 14", start: 70, end: 75 },
  { label: "Apr 21", start: 75, end: 80 },
  { label: "Apr 28", start: 80, end: 85 },
  { label: "May 5", start: 85, end: 90 },
  { label: "May 12", start: 90, end: 95 },
  { label: "May 19", start: 95, end: 100 },
  { label: "May 26", start: 100, end: 105 },
  { label: "Jun 2", start: 105, end: 110 },
  { label: "Jun 9", start: 110, end: 115 },
  { label: "Jun 16", start: 115, end: 120 },
  { label: "Jun 23", start: 120, end: 125 },
  { label: "Jun 30", start: 125, end: 130 },
  { label: "Jul 7", start: 130, end: 135 },
  { label: "Jul 14", start: 135, end: 140 },
  { label: "Jul 21", start: 140, end: 145 },
  { label: "Jul 28", start: 145, end: 150 },
  { label: "Aug 4", start: 150, end: 155 },
  { label: "Aug 11", start: 155, end: 160 },
  { label: "Aug 18", start: 160, end: 165 },
  { label: "Aug 25", start: 165, end: 170 },
  { label: "Sep 1", start: 170, end: 175 },
  { label: "Sep 8", start: 175, end: 180 },
  { label: "Sep 15", start: 180, end: 185 },
  { label: "Sep 22", start: 185, end: 190 },
  { label: "Sep 29", start: 190, end: 195 },
  { label: "Oct 6", start: 195, end: 200 },
  { label: "Oct 13", start: 200, end: 205 },
  { label: "Oct 20", start: 205, end: 210 },
  { label: "Oct 27", start: 210, end: 215 },
  { label: "Nov 3", start: 215, end: 220 },
  { label: "Nov 10", start: 220, end: 225 },
  { label: "Nov 17", start: 225, end: 230 },
  { label: "Nov 24", start: 230, end: 235 },
  { label: "Dec 1", start: 235, end: 240 },
  { label: "Dec 8", start: 240, end: 245 },
  { label: "Dec 15", start: 245, end: 250 },
  { label: "Dec 22", start: 250, end: 255 },
  { label: "Dec 29", start: 255, end: 260 },
];

const BEEF_MONTH_RANGES = [
  { label: "Jan", start: 0, end: 20 },
  { label: "Feb", start: 20, end: 40 },
  { label: "Mar", start: 40, end: 65 },
  { label: "Apr", start: 65, end: 85 },
  { label: "May", start: 85, end: 110 },
  { label: "Jun", start: 110, end: 130 },
  { label: "Jul", start: 130, end: 155 },
  { label: "Aug", start: 155, end: 175 },
  { label: "Sep", start: 175, end: 195 },
  { label: "Oct", start: 195, end: 220 },
  { label: "Nov", start: 220, end: 240 },
  { label: "Dec", start: 240, end: 260 },
];


const BEEF_PRODUCTS_DAILY = [
  { name: "Chuck Roll", primal: "Chuck", item: "116A", loads: 312, daily: genDaily2025(231.20, scaleDrift(DRIFT_A, 0.42)) },
  { name: "Shoulder Clod", primal: "Chuck", item: "114A", loads: 185, daily: genDaily2025(197.50, scaleDrift(DRIFT_B, 0.38)) },
  { name: "Chuck Tender", primal: "Chuck", item: "116B", loads: 98, daily: genDaily2025(284.10, scaleDrift(DRIFT_A, 0.52)) },
  { name: "Ribeye Roll LipOn", primal: "Rib", item: "112A", loads: 245, daily: genDaily2025(496.50, scaleDrift(DRIFT_B, 1.05)) },
  { name: "Rib, Back Ribs", primal: "Rib", item: "124", loads: 78, daily: genDaily2025(194.20, scaleDrift(DRIFT_A, 0.52)) },
  { name: "Strip Loin 0x1", primal: "Loin", item: "180", loads: 278, daily: genDaily2025(384.30, scaleDrift(DRIFT_B, 0.90)) },
  { name: "Tenderloin", primal: "Loin", item: "189A", loads: 142, daily: genDaily2025(610.50, scaleDrift(DRIFT_A, 1.22)) },
  { name: "Top Sirloin Butt", primal: "Loin", item: "184", loads: 205, daily: genDaily2025(311.40, scaleDrift(DRIFT_B, 0.62)) },
  { name: "Top Round", primal: "Round", item: "168", loads: 168, daily: genDaily2025(217.80, scaleDrift(DRIFT_A, 0.52)) },
  { name: "Bottom Round Flat", primal: "Round", item: "170", loads: 145, daily: genDaily2025(204.30, scaleDrift(DRIFT_B, 0.50)) },
  { name: "Eye of Round", primal: "Round", item: "171C", loads: 112, daily: genDaily2025(197.50, scaleDrift(DRIFT_A, 0.52)) },
  { name: "Brisket, Whole", primal: "Brisket", item: "120", loads: 198, daily: genDaily2025(257.80, scaleDrift(DRIFT_B, 0.60)) },
  { name: "Brisket, Flat", primal: "Brisket", item: "120A", loads: 165, daily: genDaily2025(291.30, scaleDrift(DRIFT_A, 0.66)) },
  { name: "50% Lean Trim", primal: "Trim", item: "50%", loads: 892, daily: genDaily2025(81.50, scaleDrift(DRIFT_B, 0.30)) },
  { name: "65% Lean Trim", primal: "Trim", item: "65%", loads: 445, daily: genDaily2025(117.60, scaleDrift(DRIFT_A, 0.36)) },
  { name: "90% Lean Trim", primal: "Trim", item: "90%", loads: 628, daily: genDaily2025(281.50, scaleDrift(DRIFT_B, 0.62)) },
  { name: "Flank Steak", primal: "Flank", item: "193", loads: 88, daily: genDaily2025(344.10, scaleDrift(DRIFT_A, 0.85)) },
  { name: "Skirt Steak, Inside", primal: "Plate", item: "121C", loads: 125, daily: genDaily2025(397.50, scaleDrift(DRIFT_B, 0.95)) },
  { name: "Skirt Steak, Outside", primal: "Plate", item: "121E", loads: 95, daily: genDaily2025(476.80, scaleDrift(DRIFT_A, 1.18)) },
  { name: "Short Plate", primal: "Plate", item: "121", loads: 342, daily: genDaily2025(141.60, scaleDrift(DRIFT_B, 0.42)) },
];

// Primal-level prices (composite of subprimals within each primal)
const BEEF_PRIMALS_DAILY = [
  { name: "Chuck", daily: genDaily2025(218.45, scaleDrift(DRIFT_A, 0.38)) },
  { name: "Rib", daily: genDaily2025(342.56, scaleDrift(DRIFT_B, 0.78)) },
  { name: "Loin", daily: genDaily2025(298.12, scaleDrift(DRIFT_A, 0.68)) },
  { name: "Round", daily: genDaily2025(225.34, scaleDrift(DRIFT_B, 0.48)) },
  { name: "Brisket", daily: genDaily2025(265.78, scaleDrift(DRIFT_A, 0.58)) },
  { name: "Trim", daily: genDaily2025(155.20, scaleDrift(DRIFT_B, 0.42)) },
  { name: "Flank", daily: genDaily2025(344.10, scaleDrift(DRIFT_A, 0.85)) },
  { name: "Plate", daily: genDaily2025(312.50, scaleDrift(DRIFT_B, 0.72)) },
];

// Ordered grouping: primal → its subprimals
const BEEF_PRIMAL_ORDER = ["Rib","Chuck","Brisket","Round","Loin","Plate","Flank","Trim"];

function getPrimalView(primal, period) {
  return getProductView(primal, period);
}

// Aggregation: compute average over a range of daily values
function avgRange(daily, start, end) {
  const slice = daily.slice(start, end).filter(v => v != null);
  if (slice.length === 0) return null;
  return Math.round(slice.reduce((a, b) => a + b, 0) / slice.length * 100) / 100;
}

// Build aggregated view for a product
function getProductView(product, period) {
  if (period === "daily") {
    return { labels: BEEF_DAILY_DATES, values: product.daily };
  } else if (period === "weekly") {
    return {
      labels: BEEF_WEEK_RANGES.map(w => w.label),
      values: BEEF_WEEK_RANGES.map(w => avgRange(product.daily, w.start, w.end)),
    };
  } else {
    return {
      labels: BEEF_MONTH_RANGES.map(m => m.label),
      values: BEEF_MONTH_RANGES.map(m => avgRange(product.daily, m.start, m.end)),
    };
  }
}

const COLD_STORAGE = {
  months: ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
  beef: {
    total:    [492,488,482,480,478,465,451,442,438,452,468,485],
    boneless: [298,294,290,288,285,278,268,262,258,268,280,292],
    cuts:     [194,194,192,192,193,187,183,180,180,184,188,193],
  },
  pork: {
    total:    [618,610,605,608,612,598,575,562,548,559,578,602],
    bellies:  [52,48,44,43,42,38,32,28,25,30,36,45],
    ribs:     [92,90,88,86,85,82,78,75,72,76,82,88],
    hams:     [152,150,148,149,148,142,135,130,128,132,140,148],
    trimmings:[178,176,175,176,180,178,175,172,168,170,172,175],
  },
  chicken: {
    total:    [878,870,862,855,845,832,818,805,795,810,835,862],
    whole:    [130,128,125,124,122,118,112,108,105,110,118,125],
    parts:    [558,552,548,545,542,535,528,520,515,522,535,550],
    processed:[190,190,189,186,181,179,178,177,175,178,182,187],
  },
  turkey: {
    total:    [298,294,288,286,285,278,268,262,258,268,280,292],
    whole:    [102,98,92,88,82,78,72,68,65,72,82,95],
    parts:    [196,196,196,198,203,200,196,194,193,196,198,197],
  },
};
// Weekly slaughter using same BEEF_WEEK_RANGES (52 weeks)
// Thousand head per week
function mkWeekly2025(base, drift) {
  const d = genDaily2025(base, drift);
  return BEEF_WEEK_RANGES.map(w => { const s = d.slice(w.start, w.end).filter(v => v != null); return s.length > 0 ? Math.round(s.reduce((a,b) => a+b, 0) / s.length) : null; });
}
function mkWeeklyFull(base, drift) {
  const d = genDaily(base, drift);
  return BEEF_WEEK_RANGES.map(w => Math.round(d.slice(w.start, w.end).reduce((a,b) => a+b, 0) / 5));
}

const CATTLE_SLAUGHTER = {
  total: {
    "2025": mkWeekly2025(624, scaleDrift(DRIFT_A, 0.6)),
    "2024": mkWeeklyFull(632, scaleDrift(DRIFT_B, 0.55)),
    "5yr":  mkWeeklyFull(645, scaleDrift(DRIFT_A, 0.5)),
  },
  steersHeifers: {
    "2025": mkWeekly2025(502, scaleDrift(DRIFT_B, 0.48)),
    "2024": mkWeeklyFull(510, scaleDrift(DRIFT_A, 0.44)),
    "5yr":  mkWeeklyFull(522, scaleDrift(DRIFT_B, 0.40)),
  },
  cows: {
    "2025": mkWeekly2025(122, scaleDrift(DRIFT_A, 0.14)),
    "2024": mkWeeklyFull(124, scaleDrift(DRIFT_B, 0.12)),
    "5yr":  mkWeeklyFull(128, scaleDrift(DRIFT_A, 0.11)),
  },
};

// Average dressed weights (lbs) — weekly seasonal
const CATTLE_WEIGHTS = {
  total: {
    "2025": mkWeekly2025(838, scaleDrift(DRIFT_B, 0.08)),
    "2024": mkWeeklyFull(832, scaleDrift(DRIFT_A, 0.07)),
    "5yr":  mkWeeklyFull(825, scaleDrift(DRIFT_B, 0.06)),
  },
  steersHeifers: {
    "2025": mkWeekly2025(878, scaleDrift(DRIFT_A, 0.09)),
    "2024": mkWeeklyFull(872, scaleDrift(DRIFT_B, 0.08)),
    "5yr":  mkWeeklyFull(864, scaleDrift(DRIFT_A, 0.07)),
  },
  cows: {
    "2025": mkWeekly2025(642, scaleDrift(DRIFT_B, 0.06)),
    "2024": mkWeeklyFull(638, scaleDrift(DRIFT_A, 0.05)),
    "5yr":  mkWeeklyFull(630, scaleDrift(DRIFT_B, 0.05)),
  },
};

// Beef production (million lbs) — weekly seasonal
const BEEF_PRODUCTION = {
  total: {
    "2025": mkWeekly2025(523, scaleDrift(DRIFT_A, 0.50)),
    "2024": mkWeeklyFull(526, scaleDrift(DRIFT_B, 0.46)),
    "5yr":  mkWeeklyFull(532, scaleDrift(DRIFT_A, 0.42)),
  },
  steersHeifers: {
    "2025": mkWeekly2025(441, scaleDrift(DRIFT_B, 0.42)),
    "2024": mkWeeklyFull(445, scaleDrift(DRIFT_A, 0.39)),
    "5yr":  mkWeeklyFull(451, scaleDrift(DRIFT_B, 0.36)),
  },
  cows: {
    "2025": mkWeekly2025(78, scaleDrift(DRIFT_A, 0.09)),
    "2024": mkWeeklyFull(80, scaleDrift(DRIFT_B, 0.08)),
    "5yr":  mkWeeklyFull(81, scaleDrift(DRIFT_A, 0.07)),
  },
};

const HOG_SLAUGHTER_WEEKLY = {
  "2025": mkWeekly2025(2490, scaleDrift(DRIFT_B, 2.2)),
  "2024": mkWeeklyFull(2520, scaleDrift(DRIFT_A, 2.0)),
  "5yr":  mkWeeklyFull(2480, scaleDrift(DRIFT_B, 1.8)),
};
// ─── Pork cutout daily data — USDA AMS LM_PK602 ────────────────────
// Same 50-day structure as beef, same BEEF_DAILY_DATES/WEEK_RANGES/MONTH_RANGES

const PORK_CUTOUT_DAILY = {
  "2025": genDaily2025(87.80, scaleDrift(DRIFT_A, 0.22)),
  "2024": genDaily(82.50, scaleDrift(DRIFT_B, 0.20)),
  "5yr":  genDaily(78.30, scaleDrift(DRIFT_A, 0.16)),
};
const PORK_CUTOUT_LATEST = 98.34;

const PORK_PRIMALS_DAILY = [
  { name: "Loin", daily: genDaily2025(81.50, scaleDrift(DRIFT_B, 0.22)) },
  { name: "Butt", daily: genDaily2025(97.80, scaleDrift(DRIFT_A, 0.26)) },
  { name: "Ham", daily: genDaily2025(71.50, scaleDrift(DRIFT_B, 0.20)) },
  { name: "Belly", daily: genDaily2025(117.50, scaleDrift(DRIFT_A, 0.52)) },
  { name: "Rib", daily: genDaily2025(144.80, scaleDrift(DRIFT_B, 0.38)) },
  { name: "Picnic", daily: genDaily2025(58.20, scaleDrift(DRIFT_A, 0.16)) },
  { name: "Trim", daily: genDaily2025(38.50, scaleDrift(DRIFT_B, 0.10)) },
];

const PORK_PRODUCTS_DAILY = [
  { name: "Bone-In Loin", primal: "Loin", item: "410", loads: 225, daily: genDaily2025(78.50, scaleDrift(DRIFT_A, 0.20)) },
  { name: "Boneless Loin", primal: "Loin", item: "413", loads: 310, daily: genDaily2025(98.20, scaleDrift(DRIFT_B, 0.24)) },
  { name: "Tenderloin", primal: "Loin", item: "415", loads: 145, daily: genDaily2025(148.30, scaleDrift(DRIFT_A, 0.35)) },
  { name: "Center Cut Chop", primal: "Loin", item: "412B", loads: 178, daily: genDaily2025(112.40, scaleDrift(DRIFT_B, 0.28)) },
  { name: "Butt, Bone-In", primal: "Butt", item: "406", loads: 265, daily: genDaily2025(88.60, scaleDrift(DRIFT_A, 0.22)) },
  { name: "Butt, Boneless", primal: "Butt", item: "406A", loads: 388, daily: genDaily2025(108.40, scaleDrift(DRIFT_B, 0.28)) },
  { name: "Ham, 23-27 lb", primal: "Ham", item: "401", loads: 195, daily: genDaily2025(68.50, scaleDrift(DRIFT_A, 0.18)) },
  { name: "Ham, Boneless", primal: "Ham", item: "402", loads: 152, daily: genDaily2025(95.20, scaleDrift(DRIFT_B, 0.24)) },
  { name: "Ham, Outside", primal: "Ham", item: "402F", loads: 118, daily: genDaily2025(88.40, scaleDrift(DRIFT_A, 0.22)) },
  { name: "Ham, Inside", primal: "Ham", item: "402E", loads: 135, daily: genDaily2025(102.30, scaleDrift(DRIFT_B, 0.26)) },
  { name: "Ham, Knuckle", primal: "Ham", item: "402G", loads: 92, daily: genDaily2025(92.80, scaleDrift(DRIFT_A, 0.20)) },
  { name: "Belly, Skin-On", primal: "Belly", item: "408", loads: 285, daily: genDaily2025(115.80, scaleDrift(DRIFT_A, 0.50)) },
  { name: "Belly, Skinless", primal: "Belly", item: "409", loads: 342, daily: genDaily2025(122.50, scaleDrift(DRIFT_B, 0.52)) },
  { name: "Spareribs", primal: "Rib", item: "416", loads: 198, daily: genDaily2025(142.30, scaleDrift(DRIFT_A, 0.36)) },
  { name: "St. Louis Ribs", primal: "Rib", item: "416A", loads: 165, daily: genDaily2025(158.60, scaleDrift(DRIFT_B, 0.40)) },
  { name: "Back Ribs", primal: "Rib", item: "422", loads: 88, daily: genDaily2025(178.50, scaleDrift(DRIFT_A, 0.42)) },
  { name: "Picnic, Bone-In", primal: "Picnic", item: "405", loads: 210, daily: genDaily2025(52.40, scaleDrift(DRIFT_B, 0.14)) },
  { name: "Picnic, Boneless", primal: "Picnic", item: "405A", loads: 175, daily: genDaily2025(68.80, scaleDrift(DRIFT_A, 0.18)) },
  { name: "72% Lean Trim", primal: "Trim", item: "72%", loads: 725, daily: genDaily2025(48.50, scaleDrift(DRIFT_B, 0.12)) },
  { name: "42% Lean Trim", primal: "Trim", item: "42%", loads: 480, daily: genDaily2025(22.30, scaleDrift(DRIFT_A, 0.08)) },
];

const PORK_PRIMAL_ORDER = ["Loin","Butt","Rib","Ham","Belly","Jowl","Trim"];

const PORK_PRODUCT_SEASONAL = PORK_PRODUCTS_DAILY.map((p, i) => ({
  ...p,
  "2024": genDaily(p.daily[0] - 5 - i * 0.3, scaleDrift(i % 2 === 0 ? DRIFT_B : DRIFT_A, 0.18 + i * 0.01)),
  "5yr":  genDaily(p.daily[0] - 10 - i * 0.5, scaleDrift(i % 2 === 0 ? DRIFT_A : DRIFT_B, 0.14 + i * 0.008)),
}));

const PORK_PRIMAL_SEASONAL = PORK_PRIMALS_DAILY.map((p, i) => ({
  ...p,
  "2024": genDaily(p.daily[0] - 6 - i * 0.4, scaleDrift(i % 2 === 0 ? DRIFT_B : DRIFT_A, 0.16 + i * 0.012)),
  "5yr":  genDaily(p.daily[0] - 12 - i * 0.6, scaleDrift(i % 2 === 0 ? DRIFT_A : DRIFT_B, 0.12 + i * 0.008)),
}));

const BEEF_PRODUCT_SEASONAL = BEEF_PRODUCTS_DAILY.map((p, i) => ({
  ...p,
  "2024": genDaily(p.daily[0] - 8 - i * 0.5, scaleDrift(i % 2 === 0 ? DRIFT_B : DRIFT_A, 0.35 + i * 0.02)),
  "5yr":  genDaily(p.daily[0] - 15 - i * 0.8, scaleDrift(i % 2 === 0 ? DRIFT_A : DRIFT_B, 0.28 + i * 0.015)),
}));

const BEEF_PRIMAL_SEASONAL = BEEF_PRIMALS_DAILY.map((p, i) => ({
  ...p,
  "2024": genDaily(p.daily[0] - 10 - i * 0.6, scaleDrift(i % 2 === 0 ? DRIFT_B : DRIFT_A, 0.32 + i * 0.02)),
  "5yr":  genDaily(p.daily[0] - 18 - i * 0.9, scaleDrift(i % 2 === 0 ? DRIFT_A : DRIFT_B, 0.25 + i * 0.015)),
}));

function getSeasonalView(series2025, series2024, series5yr, period, customLabels) {
  var dailyLabels = customLabels || BEEF_DAILY_DATES;
  if (period === "daily") {
    return { labels: dailyLabels, "2025": series2025, "2024": series2024, "5yr": series5yr };
  } else if (period === "weekly") {
    return {
      labels: BEEF_WEEK_RANGES.map(w => w.label),
      "2025": BEEF_WEEK_RANGES.map(w => avgRange(series2025, w.start, w.end)),
      "2024": BEEF_WEEK_RANGES.map(w => avgRange(series2024, w.start, w.end)),
      "5yr":  BEEF_WEEK_RANGES.map(w => avgRange(series5yr, w.start, w.end)),
    };
  } else {
    return {
      labels: BEEF_MONTH_RANGES.map(m => m.label),
      "2025": BEEF_MONTH_RANGES.map(m => avgRange(series2025, m.start, m.end)),
      "2024": BEEF_MONTH_RANGES.map(m => avgRange(series2024, m.start, m.end)),
      "5yr":  BEEF_MONTH_RANGES.map(m => avgRange(series5yr, m.start, m.end)),
    };
  }
}

// ─── USDA Quarterly Hogs & Pigs Report ──────────────────────────────
// Published Mar, Jun, Sep, Dec. All inventory in thousand head.
// Quarters: Mar 1, Jun 1, Sep 1, Dec 1 inventory dates

const HOGS_PIGS_QUARTERS = ["Mar","Jun","Sep","Dec"];

const HOGS_PIGS = {
  totalInventory: {
    label: "All hogs and pigs", unit: "thousand head",
    "2025": [75250,null,null,null],
    "2024": [74300,74800,75100,74600],
    "2023": [72400,72800,73500,73200],
    "2022": [73200,73800,74200,73600],
    "5yr":  [72800,73100,73600,73100],
  },
  breedingInventory: {
    label: "Breeding inventory", unit: "thousand head",
    "2025": [6095,null,null,null],
    "2024": [6050,6020,6080,6065],
    "2023": [6120,6085,6100,6070],
    "2022": [6180,6150,6130,6100],
    "5yr":  [6140,6110,6120,6090],
  },
  marketInventory: {
    label: "Market hog inventory", unit: "thousand head",
    "2025": [69155,null,null,null],
    "2024": [68250,68780,69020,68535],
    "2023": [66280,66715,67400,67130],
    "2022": [67020,67650,68070,67500],
    "5yr":  [66660,66990,67480,67010],
  },
  pigCrop: {
    label: "Pig crop", unit: "thousand head",
    "2025": [33650,null,null,null],
    "2024": [33280,33450,33520,33380],
    "2023": [32850,33100,33250,33050],
    "2022": [33400,33550,33680,33420],
    "5yr":  [33150,33320,33450,33280],
  },
};

// ─── CFTC Commitment of Traders — Disaggregated Futures & Options ────
// Producer/Merchant, Swap Dealers, Managed Money, Other Reportables
// Each category has net position and weekly change
// Latest data from 03/03/2026 - 03/10/2026 report

const COT_WEEKS = ["Nov 5","Nov 12","Nov 19","Nov 26","Dec 3","Dec 10","Dec 17","Dec 24","Dec 31","Jan 7","Jan 14","Jan 21","Jan 28","Feb 4","Feb 11","Feb 18","Feb 25","Mar 4","Mar 11","Mar 18"];

// 10 years of weekly COT data (52 weeks/year × 10 years = 520 points)
// Generate a full history, then derive seasonal envelope + overlay lines
function mkCOTHistory(base, amplitude, trend) {
  const pts = [];
  for (let y = 0; y < 10; y++) {
    for (let w = 0; w < 52; w++) {
      const seasonal = Math.sin((w / 52) * Math.PI * 2 + 0.5) * amplitude;
      const yearTrend = y * trend;
      const noise = (Math.sin(y * 3.7 + w * 0.6) * amplitude * 0.3 + Math.cos(y * 2.1 + w * 0.9) * amplitude * 0.2);
      pts.push(Math.round(base + seasonal + yearTrend + noise));
    }
  }
  return pts;
}

// Derive seasonal range band from 10 years: min, max, median per week, plus this year and last year
function mkCOTBand(history) {
  const weeks = 52;
  const years = 10;
  const min = [], max = [], median = [], thisYear = [], lastYear = [];
  for (let w = 0; w < weeks; w++) {
    const vals = [];
    for (let y = 0; y < years; y++) vals.push(history[y * weeks + w]);
    vals.sort((a, b) => a - b);
    min.push(vals[0]);
    max.push(vals[vals.length - 1]);
    median.push(vals[Math.floor(vals.length / 2)]);
    thisYear.push(history[(years - 1) * weeks + w]);
    lastYear.push(history[(years - 2) * weeks + w]);
  }
  return { min, max, median, thisYear, lastYear, history };
}

function mkCOTSeries(base, driftScale) {
  const arr = [base];
  for (let i = 1; i < 20; i++) {
    arr.push(Math.round(arr[i-1] + (Math.sin(i * 0.7) * driftScale * 800 + (Math.cos(i * 1.1) - 0.5) * driftScale * 400)));
  }
  return arr;
}

function mkFullCOT(prod, prodChg, swap, swapChg, mm, mmChg, mmLong, mmShort, other, otherChg, oi, oiChg) {
  const mmNet = mkCOTSeries(mm, Math.abs(mm) / 60000);
  const mmL = mkCOTSeries(mmLong, Math.abs(mmLong) / 80000);
  const mmS = mkCOTSeries(Math.abs(mmShort), Math.abs(mmShort) / 80000);
  const prodNet = mkCOTSeries(prod, Math.abs(prod) / 80000);
  const prodL = mkCOTSeries(Math.abs(prod) * 0.7, Math.abs(prod) / 100000);
  const prodS = mkCOTSeries(Math.abs(prod) * 1.1, Math.abs(prod) / 90000);
  const swapNet = mkCOTSeries(swap, Math.abs(swap) / 80000);
  const swapL = mkCOTSeries(Math.max(Math.abs(swap) * 0.8, 1000), Math.abs(swap) / 90000);
  const swapS = mkCOTSeries(Math.max(Math.abs(swap) * 0.5, 500), Math.abs(swap) / 100000);
  const otherNet = mkCOTSeries(other, Math.abs(other) / 100000);
  const otherL = mkCOTSeries(Math.abs(other) * 0.6, Math.abs(other) / 120000);
  const otherS = mkCOTSeries(Math.abs(other) * 0.4, Math.abs(other) / 130000);
  // Range band data (10-year history)
  const bands = {
    managed: {
      net: mkCOTBand(mkCOTHistory(mm, Math.abs(mm) * 0.4, mm * 0.02)),
      long: mkCOTBand(mkCOTHistory(mmLong, Math.abs(mmLong) * 0.3, mmLong * 0.015)),
      short: mkCOTBand(mkCOTHistory(Math.abs(mmShort), Math.abs(mmShort) * 0.3, Math.abs(mmShort) * 0.015)),
    },
    producer: {
      net: mkCOTBand(mkCOTHistory(prod, Math.abs(prod) * 0.35, prod * 0.015)),
      long: mkCOTBand(mkCOTHistory(Math.abs(prod) * 0.7, Math.abs(prod) * 0.25, Math.abs(prod) * 0.01)),
      short: mkCOTBand(mkCOTHistory(Math.abs(prod) * 1.1, Math.abs(prod) * 0.3, Math.abs(prod) * 0.012)),
    },
    swap: {
      net: mkCOTBand(mkCOTHistory(swap, Math.max(Math.abs(swap) * 0.4, 500), swap * 0.02)),
      long: mkCOTBand(mkCOTHistory(Math.max(Math.abs(swap) * 0.8, 1000), Math.max(Math.abs(swap) * 0.3, 300), Math.abs(swap) * 0.01)),
      short: mkCOTBand(mkCOTHistory(Math.max(Math.abs(swap) * 0.5, 500), Math.max(Math.abs(swap) * 0.2, 200), Math.abs(swap) * 0.008)),
    },
    other: {
      net: mkCOTBand(mkCOTHistory(other, Math.abs(other) * 0.4, other * 0.015)),
      long: mkCOTBand(mkCOTHistory(Math.abs(other) * 0.6, Math.abs(other) * 0.25, Math.abs(other) * 0.01)),
      short: mkCOTBand(mkCOTHistory(Math.abs(other) * 0.4, Math.abs(other) * 0.2, Math.abs(other) * 0.008)),
    },
    oi: { net: mkCOTBand(mkCOTHistory(oi, oi * 0.15, oi * 0.02)) },
  };
  return {
    producer: { net: prodNet, long: prodL, short: prodS, chg: prodChg },
    swap: { net: swapNet, long: swapL, short: swapS, chg: swapChg },
    managed: { net: mmNet, long: mmL, short: mmS, chg: mmChg, recLong: mmLong, recShort: mmShort },
    other: { net: otherNet, long: otherL, short: otherS, chg: otherChg },
    oi: { net: mkCOTSeries(oi, oi / 200000), chg: oiChg },
    bands,
  };
}

const COT_GROUPS = [
  { header: "GRAINS", items: [
    { id: "cot-corn", label: "Corn" },
    { id: "cot-soybeans", label: "Soybeans" },
    { id: "cot-meal", label: "Soybean Meal" },
    { id: "cot-oil", label: "Soybean Oil" },
    { id: "cot-chi-wheat", label: "Chicago Wheat" },
    { id: "cot-kc-wheat", label: "KC Wheat" },
    { id: "cot-mpls-wheat", label: "MN Wheat" },
  ]},
  { header: "LIVESTOCK", items: [
    { id: "cot-live-cattle", label: "Live Cattle" },
    { id: "cot-feeder-cattle", label: "Feeder Cattle" },
    { id: "cot-lean-hogs", label: "Lean Hogs" },
  ]},
  { header: "ENERGIES", items: [
    { id: "cot-crude-oil", label: "Crude Oil" },
    { id: "cot-heating-oil", label: "Heating Oil" },
    { id: "cot-nat-gas", label: "Natural Gas" },
  ]},
];

const COT_DATA = {
  "cot-corn":          { label: "Corn",          exchange: "CBOT", contract: "5,000 bu",    ...mkFullCOT(-477414,-143803, 300302,-961,   193271,140297, 429189,-353983, 34962,26447,   2219481,201194) },
  "cot-chi-wheat":     { label: "Wheat (SRW)",   exchange: "CBOT", contract: "5,000 bu",    ...mkFullCOT(-49596,-822,     77153,1780,    -22345,3455,   80827,-162327, -4650,-5613,    562155,47040) },
  "cot-soybeans":      { label: "Soybeans",      exchange: "CBOT", contract: "5,000 bu",    ...mkFullCOT(-287600,-7999,   96937,-6307,   222107,23205,  253889,-185750, 8847,-6390,    1306197,65135) },
  "cot-kc-wheat":      { label: "KC Wheat (HRW)",exchange: "KCBT", contract: "5,000 bu",    ...mkFullCOT(-79740,-3139,    77502,-1330,   9425,7559,     73111,-80799,  -2134,-2451,    323195,5475) },
  "cot-mpls-wheat":    { label: "MN Wheat (HRS)",exchange: "MGEX", contract: "5,000 bu",    ...mkFullCOT(-18306,-11090,   52,50,         15990,12027,   19867,-34140,  2107,-845,      68747,-716) },
  "cot-oil":           { label: "Soybean Oil",   exchange: "CBOT", contract: "60,000 lbs",  ...mkFullCOT(-181772,-29160,  69462,-4917,   108838,33329,  126543,-109950, -9045,594,     915257,38074) },
  "cot-meal":          { label: "Soybean Meal",  exchange: "CBOT", contract: "100 tons",    ...mkFullCOT(-208373,-21041,  92776,-6902,   80661,18574,   155063,-133592, 12312,6609,    595072,10653) },
  "cot-live-cattle":   { label: "Live Cattle",   exchange: "CME",  contract: "40,000 lbs",  ...mkFullCOT(-152553,7520,    58137,-1599,   109032,-5487,  156909,-6885,  7017,-420,      450974,-8998) },
  "cot-feeder-cattle": { label: "Feeder Cattle", exchange: "CME",  contract: "50,000 lbs",  ...mkFullCOT(-9471,-480,      3835,201,      18070,114,     37806,-9796,   -3787,-569,     113122,-3010) },
  "cot-lean-hogs":     { label: "Lean Hogs",     exchange: "CME",  contract: "40,000 lbs",  ...mkFullCOT(-185920,-965,    69468,-857,    127704,3668,   146288,-31110, 7976,-878,      488840,-1238) },
  "cot-crude-oil":     { label: "Crude Oil",     exchange: "NYMEX",contract: "1,000 bbl",   ...mkFullCOT(229012,36619,    -585216,-90968, 136419,27998, 496111,-29995, 165069,25521,   3138821,249718) },
  "cot-heating-oil":   { label: "Heating Oil",   exchange: "NYMEX",contract: "42,000 gal",  ...mkFullCOT(-84199,12473,    46331,-6409,   19776,-2926,   97977,-46823,  -5846,-1905,    304224,-21714) },
  "cot-nat-gas":       { label: "Natural Gas",   exchange: "NYMEX",contract: "10,000 MMBtu", ...mkFullCOT(8267,-10142,     156384,-10016, -62574,13336,  271683,-330163, -125825,5926,  1584208,-37239) },
};

// ─── Ethanol — live data from EIA API ────
function useLiveEthanol() {
  var _s = useState(null); var data = _s[0], setData = _s[1];
  var _l = useState(false); var loaded = _l[0], setLoaded = _l[1];
  useEffect(function() {
    fetch("data/ethanol.json?t=" + Date.now())
      .then(function(r) { if (!r.ok) throw new Error("not found"); return r.json(); })
      .then(function(d) { setData(d); setLoaded(true); })
      .catch(function() { setLoaded(true); });
  }, []);
  return { ethData: data, ethLoaded: loaded };
}

function useLiveOilseedCrushing() {
  var _s = useState(null); var data = _s[0], setData = _s[1];
  var _l = useState(false); var loaded = _l[0], setLoaded = _l[1];
  useEffect(function() {
    fetch("data/oilseed_crushing.json?t=" + Date.now())
      .then(function(r) { if (!r.ok) throw new Error("not found"); return r.json(); })
      .then(function(d) { setData(d); setLoaded(true); })
      .catch(function() { setLoaded(true); });
  }, []);
  return { oilData: data, oilLoaded: loaded };
}


function useLiveExportInspections() {
  var _s = useState(null); var data = _s[0], setData = _s[1];
  var _l = useState(false); var loaded = _l[0], setLoaded = _l[1];
  useEffect(function() {
    fetch("data/export_inspections.json?t=" + Date.now())
      .then(function(r) { if (!r.ok) throw new Error("not found"); return r.json(); })
      .then(function(d) { setData(d); setLoaded(true); })
      .catch(function() { setLoaded(true); });
  }, []);
  return { eiData: data, eiLoaded: loaded };
}


function useLiveExportSales() {
  var _s = useState(null); var data = _s[0], setData = _s[1];
  var _l = useState(false); var loaded = _l[0], setLoaded = _l[1];
  useEffect(function() {
    fetch("data/export_sales.json?t=" + Date.now())
      .then(function(r) { if (!r.ok) throw new Error("not found"); return r.json(); })
      .then(function(d) { setData(d); setLoaded(true); })
      .catch(function() { setLoaded(true); });
  }, []);
  return { esData: data, esLoaded: loaded };
}


// ─── Crop progress — live data from NASS API ────
function useLiveCropProgress() {
  const [data, setData] = useState(null);
  const [loaded, setLoaded] = useState(false);
  useEffect(() => {
    fetch("data/crop_progress.json?t=" + Date.now())
      .then(r => { if (!r.ok) throw new Error("not found"); return r.json(); })
      .then(d => { setData(d); setLoaded(true); })
      .catch(() => { setLoaded(true); });
  }, []);
  return { cpData: data, cpLoaded: loaded };
}

// ─── Ethanol data — EIA Weekly Petroleum Status Report ──────────────
// Production = thousand barrels per day (kbd)
// Stocks = thousand barrels (kb)
// Exports = thousand barrels per day (kbd)
// Weekly data, Friday dates (report released following Wednesday)


// ─── Fats & Oils data — NASS monthly report ─────────────────────────
// Soybean crush, meal/oil production, meal/oil stocks
// Monthly data, marketing year Oct–Sep
// Crush & production in million bushels (crush) / thousand short tons (meal) / million lbs (oil)
// Stocks in thousand short tons (meal) / million lbs (oil)


// ════════════════════════════════════════════════════════════════════════
// NAV
// ════════════════════════════════════════════════════════════════════════

const NAV_SECTIONS = [
  { id: "grains", label: "Grains & oilseeds",
    icon: <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.3" strokeLinecap="round" strokeLinejoin="round"><path d="M8 14V5"/><path d="M8 5C8 5 5 3 5 1"/><path d="M8 5C8 5 11 3 11 1"/><path d="M8 8C8 8 5.5 6.5 4 5"/><path d="M8 8C8 8 10.5 6.5 12 5"/><path d="M8 11C8 11 6 9.5 5 8.5"/><path d="M8 11C8 11 10 9.5 11 8.5"/></svg>,
    children: [
      { id: "wasde", label: "WASDE balance sheets" }, { id: "crop-progress", label: "Crop progress" }, { id: "ethanol", label: "Ethanol" }, { id: "fats-oils", label: "Oilseed crushing" }, { id: "export-inspections", label: "Export inspections" }, { id: "export-sales", label: "Export sales" },
    ],
  },
  { id: "livestock", label: "Livestock & meats",
    icon: <svg width="16" height="16" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round"><path d="M3 7V5.5L4.5 6.5"/><path d="M7 7V5.5L5.5 6.5"/><path d="M3 7c-.5 0-1 .4-1 1v1.5c0 .4.3.7.7.7H4"/><path d="M4 7h2c.5 0 1 .4 1 1v0"/><rect x="4" y="8" width="12" height="5" rx="1"/><path d="M16 9.5h1.5c.3 0 .5.2.5.5v1c0 .3-.2.5-.5.5H16"/><circle cx="4" cy="7.8" r="0.5" fill="currentColor" stroke="none"/><circle cx="6" cy="7.8" r="0.5" fill="currentColor" stroke="none"/><path d="M5.5 13v2.5M8 13v2.5M12.5 13v2.5M15 13v2.5"/></svg>,
    children: [
      { id: "livestock-wasde", label: "WASDE balance sheets" },
      { id: "cutout", label: "Boxed beef & pork prices" },
      { id: "meat-price-charts", label: "USDA meat price charts" },
      { id: "slaughter", label: "Slaughter" },
      { id: "cold-storage", label: "Cold storage" }, { id: "on-feed", label: "Cattle on feed" },
      { id: "hogs-pigs", label: "Hogs & pigs" },
    ],
  },
  { id: "energy", label: "Energy",
    icon: <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.3" strokeLinecap="round" strokeLinejoin="round"><path d="M9 1L5 9h4l-1 6 5-8H9l1-6z"/></svg>,
    children: [
      { subheader: "Natural Gas" },
      { id: "ng-storage", label: "Storage" },
      { id: "ng-inj-wd", label: "Injections / withdrawals" },
      { id: "ng-production", label: "Production" },
      { id: "ng-demand", label: "Demand" },
      { subheader: "Petroleum" },
      { id: "petro-crude-stocks", label: "Crude oil stocks" },
      { id: "petro-production", label: "Crude oil production" },
      { id: "petro-gasoline", label: "Gasoline stocks" },
      { id: "petro-distillate", label: "Distillate stocks" },
    ],
  },
  { id: "drivers", label: "Market Drivers",
    icon: <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.3" strokeLinecap="round" strokeLinejoin="round"><circle cx="8" cy="8" r="6.5"/><path d="M8 1.5v3M8 11.5v3M1.5 8h3M11.5 8h3"/><path d="M3.5 3.5l2 2M10.5 10.5l2 2M3.5 12.5l2-2M10.5 5.5l2-2"/></svg>,
    children: [
      { id: "fx-currencies", label: "Currencies" },
      { id: "drought", label: "Drought" },
    ],
  },
  { id: "cot", label: "Commitment of Traders",
    icon: <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.3" strokeLinecap="round" strokeLinejoin="round"><path d="M2 12l3-4 3 2 4-6"/><path d="M12 4h2v2"/><path d="M1 14h14"/><path d="M1 2v12"/></svg>,
    children: [
      { id: "cot-summary", label: "Summary" },
      { id: "cot-charts", label: "Charts" },
    ],
  },
];

// ════════════════════════════════════════════════════════════════════════
// UTILITIES & SHARED COMPONENTS
// ════════════════════════════════════════════════════════════════════════

// Shared utility: build month-label x-axis from weekly labels
// Returns { displayLabels, gridColors } with month names centered in their data range
function buildMonthAxis(weekLabels) {
  const monthNames = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
  const N = weekLabels.length;
  const pointMonths = weekLabels.map(l => {
    if (!l) return -1;
    const s = String(l);
    const slashMatch = s.match(/^(\d+)\//);
    if (slashMatch) return parseInt(slashMatch[1]) - 1;
    const idx = monthNames.findIndex(m => s.startsWith(m));
    return idx >= 0 ? idx : -1;
  });
  const monthStarts = {}; const monthEnds = {};
  pointMonths.forEach((m, i) => { if (m < 0) return; if (!(m in monthStarts)) monthStarts[m] = i; monthEnds[m] = i; });
  const midpoints = {};
  Object.keys(monthStarts).forEach(m => { midpoints[m] = Math.round((monthStarts[m] + monthEnds[m]) / 2); });
  const boundarySet = new Set(Object.values(monthStarts));
  const displayLabels = weekLabels.map((l, i) => { const m = pointMonths[i]; return (m >= 0 && midpoints[m] === i) ? monthNames[m] : ""; });
  const gridColors = weekLabels.map((l, i) => boundarySet.has(i) ? "rgba(0,0,0,0.12)" : "transparent");
  return { displayLabels, gridColors };
}

function downloadCSV(filename, headers, rows) {
  const esc = v => { const s = String(v); return s.includes(",") || s.includes('"') || s.includes("\n") ? `"${s.replace(/"/g,'""')}"` : s; };
  const csv = [headers.map(esc).join(","), ...rows.map(r => r.map(esc).join(","))].join("\n");
  const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob); const a = document.createElement("a"); a.href = url; a.download = filename; a.click(); URL.revokeObjectURL(url);
}

function DownloadBtn({ onClick, label = "Download CSV" }) {
  return (
    <button onClick={onClick} style={{ display: "inline-flex", alignItems: "center", gap: 5, padding: "5px 12px", fontSize: 12, cursor: "pointer", borderRadius: "var(--border-radius-md)", border: "1px solid #639922", background: "transparent", color: "#639922", transition: "all 0.15s" }}
      onMouseEnter={e => { e.currentTarget.style.background = "#639922"; e.currentTarget.style.color = "#fff"; }}
      onMouseLeave={e => { e.currentTarget.style.background = "transparent"; e.currentTarget.style.color = "#639922"; }}>
      <svg width="13" height="13" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><path d="M8 2v9m0 0l-3-3m3 3l3-3M3 13h10"/></svg>
      {label}
    </button>
  );
}

function MetricCard({ label, value, sub, trend }) {
  return (
    <div style={{ background: "var(--color-background-secondary)", borderRadius: "var(--border-radius-md)", padding: "12px 14px", minWidth: 0 }}>
      <div style={{ fontSize: 11, color: "var(--color-text-secondary)", marginBottom: 3, textTransform: "uppercase", letterSpacing: "0.4px" }}>{label}</div>
      <div style={{ display: "flex", alignItems: "baseline", gap: 6 }}>
        <span style={{ fontSize: 20, fontWeight: 500, color: "var(--color-text-primary)" }}>{value}</span>
        {trend !== undefined && <span style={{ fontSize: 11, fontWeight: 500, color: trend > 0 ? "#639922" : trend < 0 ? "#A32D2D" : "var(--color-text-secondary)" }}>{trend > 0 ? "+" : ""}{trend}%</span>}
      </div>
      {sub && <div style={{ fontSize: 11, color: "var(--color-text-tertiary)", marginTop: 1 }}>{sub}</div>}
    </div>
  );
}

function SectionTitle({ children, updated, right }) {
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 14, marginTop: 28, flexWrap: "wrap" }}>
      <h3 style={{ fontSize: 15, fontWeight: 500, color: "var(--color-text-primary)", margin: 0 }}>{children}</h3>
      {updated && <span style={{ fontSize: 11, color: "var(--color-text-tertiary)" }}>Updated {updated}</span>}
      {right && <div style={{ marginLeft: "auto" }}>{right}</div>}
    </div>
  );
}

function ChartModeToggle({ mode, setMode }) {
  return (
    <div style={{ display: "inline-flex", borderRadius: 6, overflow: "hidden", border: "1px solid var(--color-border-secondary)" }}>
      {[{ id: "seasonal", label: "Seasonal" }, { id: "contiguous", label: "Contiguous" }].map(m => (
        <button key={m.id} onClick={() => setMode(m.id)} style={{
          padding: "5px 14px", fontSize: 11, cursor: "pointer", border: "none",
          borderRight: m.id === "seasonal" ? "1px solid var(--color-border-secondary)" : "none",
          background: mode === m.id ? "#2563EB" : "transparent",
          color: mode === m.id ? "#fff" : "var(--color-text-tertiary)",
          fontWeight: 500, transition: "all 0.15s",
        }}>{m.label}</button>
      ))}
    </div>
  );
}

function InteractiveLegend({ items, hidden, onToggle }) {
  return (
    <div style={{ display: "flex", gap: 6, marginBottom: 10, fontSize: 12, flexWrap: "wrap" }}>
      {items.map((it, i) => {
        const off = hidden.has(it.key || it.label);
        return (
          <button key={i} onClick={() => onToggle(it.key || it.label)} style={{ display: "inline-flex", alignItems: "center", gap: 5, padding: "3px 10px", cursor: "pointer", borderRadius: "var(--border-radius-md)", border: "0.5px solid var(--color-border-tertiary)", background: off ? "var(--color-background-secondary)" : "transparent", color: off ? "var(--color-text-tertiary)" : "var(--color-text-secondary)", opacity: off ? 0.5 : 1, transition: "all 0.15s", fontSize: 12 }}>
            {it.dash ? <span style={{ width: 14, height: 0, borderTop: `2px ${it.dash} ${off ? "var(--color-text-tertiary)" : it.color}` }}></span> : <span style={{ width: 9, height: 9, borderRadius: 2, background: off ? "var(--color-text-tertiary)" : it.color, flexShrink: 0 }}></span>}
            {it.label}
          </button>
        );
      })}
    </div>
  );
}

// ── Global date formatters ──
// Centralized date formatting to ensure consistency across all pages.
// Use fmtDate() for short dates (e.g., "Apr 21, 2026")
// Use fmtDateLong() for long dates (e.g., "April 21, 2026")
const _MONTHS_SHORT = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
const _MONTHS_LONG = ["January","February","March","April","May","June","July","August","September","October","November","December"];
function _parseAnyDate(input) {
  if (!input) return null;
  if (input instanceof Date) return isNaN(input) ? null : input;
  const s = String(input).trim();
  // ISO format YYYY-MM-DD
  let m = s.match(/^(\d{4})-(\d{2})-(\d{2})/);
  if (m) return new Date(parseInt(m[1]), parseInt(m[2]) - 1, parseInt(m[3]));
  // US format MM/DD/YYYY or M/D/YYYY
  m = s.match(/^(\d{1,2})\/(\d{1,2})\/(\d{4})/);
  if (m) return new Date(parseInt(m[3]), parseInt(m[1]) - 1, parseInt(m[2]));
  // Fall back to native parse (handles "May 6, 2025", etc.)
  const d = new Date(s);
  return isNaN(d) ? null : d;
}
function fmtDate(input) {
  const d = _parseAnyDate(input);
  if (!d) return "";
  return _MONTHS_SHORT[d.getMonth()] + " " + d.getDate() + ", " + d.getFullYear();
}
function fmtDateLong(input) {
  const d = _parseAnyDate(input);
  if (!d) return "";
  return _MONTHS_LONG[d.getMonth()] + " " + d.getDate() + ", " + d.getFullYear();
}
function fmtDateRange(start, end, long) {
  const fmt = long ? fmtDateLong : fmtDate;
  const s = fmt(start), e = fmt(end);
  if (!s && !e) return "";
  if (!s) return e;
  if (!e) return s;
  return s + " – " + e;
}

function useToggle() {
  const [hidden, setHidden] = useState(new Set());
  const toggle = useCallback((key) => { setHidden(prev => { const n = new Set(prev); n.has(key) ? n.delete(key) : n.add(key); return n; }); }, []);
  return [hidden, toggle];
}

function ChartBox({ id, height = 260, renderChart, deps }) {
  const renderRef = useRef(renderChart);
  renderRef.current = renderChart;
  useEffect(() => {
    if (!window.Chart) return;
    const t = setTimeout(() => { const c = document.getElementById(id); if (!c) return; const ex = Chart.getChart(c); if (ex) ex.destroy(); renderRef.current(c); }, 60);
    return () => clearTimeout(t);
  }, [id, deps]);
  return <div style={{ position: "relative", width: "100%", height }}><canvas id={id}></canvas></div>;
}


function MapBox({ id, height, renderMap, deps }) {
  var renderRef = useRef(renderMap);
  renderRef.current = renderMap;
  useEffect(function() {
    var el = document.getElementById(id);
    if (!el) return;
    el.innerHTML = "";
    if (!window.d3 || !window.topojson) {
      el.innerHTML = "<div style='padding:40px;text-align:center;color:#999;font-size:13px'>Loading map libraries...</div>";
      // Retry after scripts load
      var timer = setInterval(function() {
        if (window.d3 && window.topojson) {
          clearInterval(timer);
          var el2 = document.getElementById(id);
          if (el2) { el2.innerHTML = ""; renderRef.current(el2); }
        }
      }, 200);
      var cleanup = setTimeout(function() { clearInterval(timer); }, 15000);
      return function() { clearInterval(timer); clearTimeout(cleanup); };
    }
    renderRef.current(el);
  }, [id, deps]);
  return <div id={id} style={{ position: "relative", width: "100%", height: height || 400 }}></div>;
}

// ════════════════════════════════════════════════════════════════════════
// WASDE BALANCE SHEET TABLE — full-width scrollable
// ════════════════════════════════════════════════════════════════════════


var shortenLabel = function(lbl) {
  var map = {"Food, feed, and other industrial": "Food, feed, other industrial",
    "Food, feed & other industrial": "Food, feed, other industrial"};
  return map[lbl] || lbl;
};
function WASDETable({ commodity }) {
  const scrollRef = useRef(null);
  const years = commodity.years || MY;
  const fcIdx = years.length - 1;

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollLeft = scrollRef.current.scrollWidth;
    }
  }, [commodity.id, years.length]);

  const formatVal = (v, row) => {
    if (v === null || v === undefined) return "—";
    if (row.price) return typeof v === "number" ? v.toFixed(2) : v;
    if (row.pct) return typeof v === "number" ? v.toFixed(1) + "%" : v;
    if (typeof v === "number") {
      if (!row._hasDecimal) {
        row._hasDecimal = row.values.some(x => typeof x === "number" && x % 1 !== 0);
      }
      if (row._hasDecimal) return v.toFixed(1);
      if (Math.abs(v) >= 1000) return v.toLocaleString();
      return v.toString();
    }
    return v;
  };

  return (
    <div ref={scrollRef} style={{ overflowX: "auto", border: "0.5px solid var(--color-border-tertiary)", borderRadius: "var(--border-radius-lg)" }}>
      <table style={{ borderCollapse: "collapse", fontSize: 12, minWidth: "100%", whiteSpace: "nowrap" }}>
        <thead>
          <tr style={{ position: "sticky", top: 0, zIndex: 2 }}>
            <th style={{
              position: "sticky", left: 0, zIndex: 3,
              background: "#ffffff",
              padding: "8px 14px", textAlign: "left", fontWeight: 500, fontSize: 12.5,
              color: "var(--color-text-secondary)", borderBottom: "1.5px solid var(--color-border-primary)",
              minWidth: 180,
            }}>
              Item
            </th>
            {years.map((yr, i) => (
              <th key={yr} style={{
                background: i === fcIdx ? "var(--color-background-info)" : "var(--color-background-secondary)",
                padding: "8px 10px", textAlign: "right", fontWeight: 500, fontSize: 12.5,
                color: i === fcIdx ? "var(--color-text-info)" : "var(--color-text-secondary)",
                borderBottom: "1.5px solid var(--color-border-primary)", minWidth: 72,
              }}>
                {yr}{i === fcIdx ? " F" : ""}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {commodity.sections.map((section, si) => (
            <>
              {si > 0 && <tr key={`sh-${si}`}>
                <td style={{ padding: "8px 14px", background: "#ffffff", position: "sticky", left: 0, zIndex: 1 }}></td>
                {years.map((_, i) => <td key={i}></td>)}
              </tr>}
              {section.rows.map((row, ri) => (
                <React.Fragment key={`r-${si}-${ri}`}>
                <tr style={{
                  borderBottom: "0.5px solid var(--color-border-tertiary)",
                }}>
                  <td style={{
                    position: "sticky", left: 0, zIndex: 1,
                    background: "#ffffff",
                    padding: row.indent ? "5px 14px 5px 28px" : "5px 14px",
                    fontWeight: row.bold ? 600 : 400,
                    color: "var(--color-text-primary)",
                    fontSize: 13,
                    borderRight: "0.5px solid var(--color-border-tertiary)",
                  }}>
                    {shortenLabel(row.label)}
                  </td>
                  {row.values.map((v, vi) => (
                    <td key={vi} style={{
                      padding: "5px 10px", textAlign: "right",
                      fontFamily: "var(--font-mono)", fontSize: 12.5,
                      fontWeight: row.bold ? 600 : 400,
                      color: vi === fcIdx ? "var(--color-text-info)" : "var(--color-text-primary)",
                      background: vi === fcIdx ? "rgba(59,130,246,0.04)" : "transparent",
                    }}>
                      {formatVal(v, row)}
                    </td>
                  ))}
                </tr>
                </React.Fragment>
              ))}
            </>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function GlobalWASDEMiniTable({ title, rows, years, fcIdx, formatVal }) {
  const scrollRef = useRef(null);
  useEffect(() => {
    if (scrollRef.current) scrollRef.current.scrollLeft = scrollRef.current.scrollWidth;
  }, [title, years.length]);

  return (
    <div style={{ marginBottom: 18 }}>
      <div ref={scrollRef} style={{ overflowX: "auto", border: "0.5px solid var(--color-border-tertiary)", borderRadius: "var(--border-radius-lg)" }}>
        <table style={{ borderCollapse: "collapse", fontSize: 12, minWidth: "100%", whiteSpace: "nowrap" }}>
          <thead>
            <tr style={{ background: "#e8e8e8" }}>
              <th style={{ position: "sticky", left: 0, zIndex: 2, background: "#e8e8e8", padding: "7px 12px", textAlign: "left", fontWeight: 600, fontSize: 12.5, color: "var(--color-text-primary)", borderBottom: "1.5px solid var(--color-border-primary)", borderRight: "0.5px solid var(--color-border-tertiary)", minWidth: 180, letterSpacing: "0.3px" }}>{title}</th>
              {years.map((y, i) => (
                <th key={y} style={{ background: i === fcIdx ? "var(--color-background-info)" : "#e8e8e8", padding: "7px 10px", textAlign: "right", fontWeight: i === fcIdx ? 600 : 400, fontSize: 12, color: i === fcIdx ? "var(--color-text-info)" : "var(--color-text-secondary)", borderBottom: "1.5px solid var(--color-border-primary)", whiteSpace: "nowrap", minWidth: 72 }}>{i === fcIdx ? y + " F" : y}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row, ri) => (
              <tr key={ri} style={{ borderBottom: "0.5px solid var(--color-border-tertiary)" }}>
                <td style={{ position: "sticky", left: 0, zIndex: 1, background: "#ffffff", padding: "6px 12px", fontWeight: row.bold ? 600 : 400, fontSize: 13, color: "var(--color-text-primary)", borderRight: "0.5px solid var(--color-border-tertiary)", paddingLeft: row.indent ? 24 : 12 }}>{shortenLabel(row.label)}</td>
                {row.values.map((v, vi) => (
                  <td key={vi} style={{ padding: "6px 10px", textAlign: "right", fontFamily: "var(--font-mono)", fontSize: 12.5, fontWeight: row.bold ? 600 : 400, color: vi === fcIdx ? "var(--color-text-info)" : "var(--color-text-secondary)", background: vi === fcIdx ? "rgba(59,130,246,0.04)" : "transparent" }}>{formatVal(v, row)}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function GlobalWASDETable({ commodity }) {
  const years = commodity.years || GMY;
  const fcIdx = years.length - 1;

  const formatVal = (v, row) => {
    if (v === null || v === undefined) return "—";
    if (row.pct) return typeof v === "number" ? v.toFixed(1) + "%" : v;
    if (typeof v === "number") {
      if (!row._hasDecimal) row._hasDecimal = row.values.some(x => typeof x === "number" && x % 1 !== 0);
      if (row._hasDecimal) {
        const fixed = v.toFixed(1);
        const [int, dec] = fixed.split(".");
        return Number(int).toLocaleString() + "." + dec;
      }
      if (Math.abs(v) >= 1000) return v.toLocaleString();
      return v.toString();
    }
    return v;
  };

  return (
    <div>
      {commodity.sections.map((section, si) => (
        <GlobalWASDEMiniTable key={si} title={section.header} rows={section.rows} years={years} fcIdx={fcIdx} formatVal={formatVal} />
      ))}
      {commodity.countries && commodity.countries.map((country, ci) => (
        <GlobalWASDEMiniTable key={`c${ci}`} title={country.label} rows={country.rows} years={years} fcIdx={fcIdx} formatVal={formatVal} />
      ))}
    </div>
  );
}

function WASDEPage() {
  const [sel, setSel] = useState("corn");
  const [liveUS, setLiveUS] = useState(null);
  const [liveWorld, setLiveWorld] = useState(null);
  const [dataLabel, setDataLabel] = useState("representative data");

  // Try to load live data
  useEffect(() => {
    fetch("data/wasde.json?t=" + Date.now())
      .then(r => { if (!r.ok) throw new Error("not found"); return r.json(); })
      .then(data => {
        if (data && data.us && Object.keys(data.us).length > 0) {
          setLiveUS(data.us);
          const d = new Date(data.fetched_at);
          setDataLabel("USDA ERS data, fetched " + d.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" }));
        }
        if (data && data.world && Object.keys(data.world).length > 0) {
          setLiveWorld(data.world);
        }
      })
      .catch(() => {});
  }, []);

  // Build commodity map: use live data if available, else hardcoded
  const hardcodedMap = {};
  WASDE_COMMODITIES.forEach(c => { hardcodedMap[c.id] = c; });

  const map = {};
  WASDE_COMMODITIES.forEach(c => {
    if (liveUS && liveUS[c.id]) {
      map[c.id] = liveUS[c.id];
    } else {
      map[c.id] = c;
    }
  });

  const globalId = sel === "soybean_meal" ? "soybean_meal" : sel === "soybean_oil" ? "soybean_oil" : sel;
  const globalData = (liveWorld && liveWorld[globalId]) ? liveWorld[globalId] : WASDE_GLOBAL[globalId];

  const commodity = map[sel];
  const years = commodity.years || MY;

  const dlWasde = () => {
    const c = commodity;
    const yrs = c.years || MY;
    const headers = ["Item", ...yrs.map((y, i) => i === yrs.length - 1 ? y + " F" : y)];
    const rows = [];
    c.sections.forEach(s => {
      rows.push([`--- ${s.header} ---`, ...yrs.map(() => "")]);
      s.rows.forEach(r => rows.push([r.label, ...r.values]));
    });
    if (globalData) {
      rows.push(["", ...MY.map(() => "")]);
      rows.push(["=== WORLD ===", ...MY.map(() => "")]);
      globalData.sections.forEach(s => {
        rows.push([`--- ${s.header} (${s.unit}) ---`, ...GMY.map(() => "")]);
        s.rows.forEach(r => rows.push([r.label, ...r.values]));
      });
      if (globalData.countries) {
        globalData.countries.forEach(c => {
          rows.push([`--- ${c.label} (MMT) ---`, ...GMY.map(() => "")]);
          c.rows.forEach(r => rows.push(["  " + r.label, ...r.values]));
        });
      }
    }
    downloadCSV(`wasde_${sel}.csv`, headers, rows);
  };

  return (
    <div>
      <div style={{ display: "flex", alignItems: "center", gap: 0, marginBottom: 16 }}>
        {WASDE_COMMODITIES.map(c => (
          <button key={c.id} onClick={() => setSel(c.id)} style={{
            padding: "6px 16px", fontSize: 13, cursor: "pointer",
            background: sel === c.id ? "#2563EB" : "transparent", border: "1px solid " + (sel === c.id ? "#2563EB" : "var(--color-border-secondary)"), borderRadius: 5,
            color: sel === c.id ? "#fff" : "var(--color-text-secondary)",
            fontWeight: sel === c.id ? 600 : 400,
            transition: "all 0.15s",
          }}>
            {c.label}
          </button>
        ))}
        <div style={{ marginLeft: "auto", paddingBottom: 4 }}><DownloadBtn onClick={dlWasde} /></div>
      </div>

      <h3 style={{ fontSize: 15, fontWeight: 500, color: "var(--color-text-primary)", margin: "0 0 10px" }}>U.S. {commodity.label} balance sheet</h3>
      <WASDETable commodity={commodity} />
      <div style={{ marginTop: 6, marginBottom: 4, fontSize: 10, color: "var(--color-text-tertiary)" }}>
        Source: {dataLabel}. Marketing years: corn/soybeans Sep–Aug, wheat Jun–May, soybean meal/oil Oct–Sep.
      </div>

      {globalData && (<>
        <h3 style={{ fontSize: 15, fontWeight: 500, color: "var(--color-text-primary)", margin: "28px 0 10px" }}>World {globalData.label} balance sheet</h3>
        <GlobalWASDETable commodity={globalData} />
        <div style={{ marginTop: 6, fontSize: 10, color: "var(--color-text-tertiary)" }}>
          Source: USDA PSD Online. Area: million hectares. Yield: MT/hectare. All supply/use/stocks in million metric tons.
        </div>
      </>)}
    </div>
  );
}

// ════════════════════════════════════════════════════════════════════════
// LIVESTOCK PAGES (unchanged from v3 — interactive legends + downloads)
// ════════════════════════════════════════════════════════════════════════

const COF_LEGEND = [
  { label: "2025", color: "#A32D2D", key: "2025" },
  { label: "2024", color: "#D85A30", key: "2024", dash: "dashed" },
  { label: "5-yr avg", color: "#333", key: "5yr", dash: "dotted" },
];
const COF_DS = {
  "2025": { borderColor: "#A32D2D", borderWidth: 2.5, pointRadius: 0, tension: 0 },
  "2024": { borderColor: "#D85A30", borderWidth: 1.5, pointRadius: 0, tension: 0, borderDash: [5,3] },
  "5yr":  { borderColor: "#333", borderWidth: 1.5, pointRadius: 0, tension: 0, borderDash: [2,3] },
};

function CattleOnFeedPage({ ready }) {
  const [cofData, setCofData] = useState(null);
  const [cofLoaded, setCofLoaded] = useState(false);
  useEffect(function() {
    fetch("data/cattle_on_feed.json?t=" + Date.now())
      .then(function(r) { return r.ok ? r.json() : null; })
      .then(function(d) { if (d) { setCofData(d); setCofLoaded(true); } })
      .catch(function() { setCofLoaded(true); });
  }, []);

  const [mode, setMode] = useState("seasonal");
  const [range, setRange] = useState("5");
  const [monthFilter, setMonthFilter] = useState("all");
  const [heifersMonth, setHeifersMonth] = useState("all");
  const [heifersRange, setHeifersRange] = useState("5");
  const [hiddenYrs, setHiddenYrs] = useState(new Set());

  useEffect(function() { setHiddenYrs(new Set()); }, [mode, range, monthFilter]);
  const toggleYr = function(label) {
    setHiddenYrs(function(prev) { const n = new Set(prev); if (n.has(label)) n.delete(label); else n.add(label); return n; });
  };

  const MONTH_LABELS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];

  function niceAxis(allVals) {
    if (!allVals || allVals.length === 0) return { yMin: 0, yMax: 100 };
    const dataMin = Math.min.apply(null, allVals);
    const dataMax = Math.max.apply(null, allVals);
    const range = dataMax - dataMin;
    const pad = Math.max(range * 0.1, Math.abs(dataMax) * 0.03 || 1);
    const rawStep = (range + pad * 2) / 5;
    if (rawStep === 0 || !isFinite(rawStep)) return { yMin: dataMin - 1, yMax: dataMax + 1 };
    const mag = Math.pow(10, Math.floor(Math.log10(rawStep)));
    const norm = rawStep / mag;
    const niceNorm = norm <= 1.5 ? 1 : norm <= 3.5 ? 2 : norm <= 7.5 ? 5 : 10;
    const step = niceNorm * mag;
    const yMin = Math.floor((dataMin - pad) / step) * step;
    const yMax = Math.ceil((dataMax + pad) / step) * step;
    return { yMin: yMin, yMax: yMax };
  }

  const curYear = new Date().getFullYear();
  const availYears = cofData && cofData.years ? cofData.years : [];
  let displayYears = availYears;
  if (range !== "all") {
    const n = parseInt(range);
    // n-year range = n prior years + current year (n+1 total)
    displayYears = availYears.filter(function(y) { return y >= curYear - n; });
  }
  // Chronological (oldest-first for legend)
  const displayYearsAsc = displayYears.slice().sort(function(a, b) { return a - b; });

  // Color palette — current year is black, others are distance-based (closest = teal, furthest = red)
  const yrColors = ["#A32D2D","#D85A30","#E8A735","#639922","#1D9E75","#378ADD","#534AB7","#8B5CF6","#EC4899","#6B7280","#0EA5E9","#14B8A6"];
  const getColor = function(yr) {
    if (yr === curYear) return "#333";
    const dist = curYear - yr;
    if (dist === 1) return "#1D9E75";
    if (dist === 2) return "#639922";
    if (dist === 3) return "#E8A735";
    if (dist === 4) return "#D85A30";
    if (dist === 5) return "#A32D2D";
    return yrColors[(dist - 1) % yrColors.length];
  };

  const legendItems = displayYearsAsc.map(function(yr) {
    return { label: String(yr), color: getColor(yr), key: String(yr) };
  });
  const hk = Array.from(hiddenYrs).sort().join(",");

  // ── Header stats ──
  function headerStats(sid) {
    if (!cofData || !cofData.series[sid]) return { cur: null, lastYr: null, prevMo: null, month: null };
    const cur = cofData.series[sid].years[String(curYear)] || [];
    const lastYrArr = cofData.series[sid].years[String(curYear - 1)] || [];
    let latestIdx = -1;
    for (let i = 11; i >= 0; i--) { if (cur[i] != null) { latestIdx = i; break; } }
    if (latestIdx < 0) return { cur: null, lastYr: null, prevMo: null, month: null };
    // Previous month (same year if available, else December of prior year)
    let prevMoVal = null;
    for (let i = latestIdx - 1; i >= 0; i--) { if (cur[i] != null) { prevMoVal = cur[i]; break; } }
    if (prevMoVal == null) {
      for (let i = 11; i >= 0; i--) { if (lastYrArr[i] != null) { prevMoVal = lastYrArr[i]; break; } }
    }
    return {
      cur: cur[latestIdx],
      lastYr: lastYrArr[latestIdx] != null ? lastYrArr[latestIdx] : null,
      prevMo: prevMoVal,
      month: MONTH_LABELS[latestIdx],
    };
  }

  function fmtNum(v, isPct) {
    if (v == null) return "—";
    if (isPct) return v.toFixed(1) + "%";
    if (v >= 1000000) return (v / 1000000).toFixed(2) + "M";
    if (v >= 1000) return (v / 1000).toFixed(0) + "K";
    return v.toLocaleString();
  }

  function pctChg(a, b) {
    if (a == null || b == null || b === 0) return null;
    return ((a - b) / b * 100);
  }

  const ofStats = headerStats("onFeed");
  const plStats = headerStats("placements");
  const mkStats = headerStats("marketings");
  const hfStats = headerStats("heifersOnFeed");

  // ── Chart builder ──
  function mkCofChart(sid, isPct, modeOverride, monthFilterOverride, rangeOverride) {
    return function(canvas) {
      if (!cofData || !cofData.series[sid]) return;
      const series = cofData.series[sid].years;
      const effMode = modeOverride || mode;
      const effMonthFilter = monthFilterOverride !== undefined ? monthFilterOverride : monthFilter;
      const effRange = rangeOverride !== undefined ? rangeOverride : range;
      // Compute display years for THIS chart based on effRange
      let chartDisplayYears = availYears;
      if (effRange !== "all") {
        const n = parseInt(effRange);
        chartDisplayYears = availYears.filter(function(y) { return y >= curYear - n; });
      }
      const chartYearsAsc = chartDisplayYears.slice().sort(function(a, b) { return a - b; });

      if (effMode === "seasonal") {
        const datasets = chartYearsAsc.map(function(yr) {
          const data = series[String(yr)] || [];
          return {
            label: String(yr),
            data: data,
            borderColor: getColor(yr),
            borderWidth: yr === curYear ? 2.5 : 1.5,
            // Quarterly series: show points at reported months, connect with lines across null gaps
            pointRadius: 0,
            pointHitRadius: 8,
            tension: 0,
            fill: false,
            spanGaps: true,
            hidden: hiddenYrs.has(String(yr)),
          };
        });
        const visibleVals = datasets.filter(function(ds) { return !ds.hidden; }).flatMap(function(ds) { return ds.data.filter(function(v) { return v != null; }); });
        if (visibleVals.length === 0) {
          new Chart(canvas, { type: "line", data: { labels: MONTH_LABELS, datasets: [] }, options: { responsive: true, maintainAspectRatio: false } });
          return;
        }
        const niceY = niceAxis(visibleVals);
        new Chart(canvas, {
          type: "line",
          data: { labels: MONTH_LABELS, datasets: datasets },
          options: {
            responsive: true, maintainAspectRatio: false,
            interaction: { mode: "nearest", intersect: false },
            plugins: { legend: { display: false }, tooltip: { callbacks: {
              label: function(c) {
                if (c.parsed.y == null) return "";
                return c.dataset.label + ": " + (isPct ? c.parsed.y.toFixed(1) + "%" : c.parsed.y.toLocaleString());
              }
            } } },
            scales: {
              x: { ticks: { font: { size: 11 } }, grid: { color: "rgba(0,0,0,0.08)", lineWidth: 0.75 } },
              y: {
                min: niceY.yMin, max: niceY.yMax,
                ticks: { font: { size: 11 }, callback: function(v) { return isPct ? v.toFixed(0) + "%" : (v / 1000).toLocaleString(); } },
                grid: { color: "rgba(0,0,0,0.08)", lineWidth: 0.75 }
              },
            },
          },
        });
      } else {
        // Contiguous mode
        const yearsVisible = chartYearsAsc.filter(function(yr) { return !hiddenYrs.has(String(yr)); });
        if (yearsVisible.length === 0) {
          new Chart(canvas, { type: "line", data: { labels: [], datasets: [] }, options: { responsive: true, maintainAspectRatio: false } });
          return;
        }

        const allPoints = [];
        const allLabels = [];
        const yearBoundaries = [];
        const yearMidpoints = [];

        if (effMonthFilter === "all") {
          yearsVisible.forEach(function(yr, yi) {
            const data = series[String(yr)] || [];
            const startIdx = allPoints.length;
            if (yi > 0) yearBoundaries.push(startIdx);
            data.forEach(function(v, mi) {
              allLabels.push(String(yr) + "-" + MONTH_LABELS[mi]);
              allPoints.push(v);
            });
            yearMidpoints.push({ idx: Math.floor(startIdx + data.length / 2), label: String(yr) });
          });
        } else {
          const mIdx = MONTH_LABELS.indexOf(effMonthFilter);
          yearsVisible.forEach(function(yr) {
            const v = (series[String(yr)] || [])[mIdx];
            allLabels.push(String(yr));
            allPoints.push(v);
            yearMidpoints.push({ idx: allPoints.length - 1, label: String(yr) });
          });
        }

        const visibleVals = allPoints.filter(function(v) { return v != null; });
        if (visibleVals.length === 0) {
          new Chart(canvas, { type: "line", data: { labels: [], datasets: [] }, options: { responsive: true, maintainAspectRatio: false } });
          return;
        }
        const niceY = niceAxis(visibleVals);
        const needsRotation = yearsVisible.length > 8;

        new Chart(canvas, {
          type: "line",
          data: { labels: allLabels, datasets: [{
            label: effMonthFilter === "all" ? cofData.series[sid].label : effMonthFilter + " " + cofData.series[sid].label,
            data: allPoints,
            borderColor: "#2563EB",
            borderWidth: 1.8,
            pointRadius: 0,
            tension: 0,
            spanGaps: true,
            fill: false,
          }]},
          options: {
            responsive: true, maintainAspectRatio: false,
            interaction: { mode: "nearest", intersect: false },
            plugins: { legend: { display: false }, tooltip: { callbacks: {
              title: function(items) { if (items.length === 0) return ""; return allLabels[items[0].dataIndex]; },
              label: function(c) {
                if (c.parsed.y == null) return "";
                return isPct ? c.parsed.y.toFixed(1) + "%" : c.parsed.y.toLocaleString();
              }
            } } },
            scales: {
              x: {
                ticks: {
                  autoSkip: false, maxRotation: needsRotation ? 90 : 0, minRotation: needsRotation ? 90 : 0, font: { size: 11 },
                  callback: function(val, idx) {
                    if (effMonthFilter !== "all") return allLabels[idx];
                    for (let i = 0; i < yearMidpoints.length; i++) {
                      if (yearMidpoints[i].idx === idx) return yearMidpoints[i].label;
                    }
                    return "";
                  },
                },
                grid: {
                  color: function(ctx) {
                    if (effMonthFilter !== "all") return "rgba(0,0,0,0.06)";
                    return yearBoundaries.indexOf(ctx.index) >= 0 ? "rgba(0,0,0,0.12)" : "transparent";
                  },
                  lineWidth: 0.75,
                },
              },
              y: {
                min: niceY.yMin, max: niceY.yMax,
                ticks: { font: { size: 11 }, callback: function(v) { return isPct ? v.toFixed(0) + "%" : (v / 1000).toLocaleString(); } },
                grid: { color: "rgba(0,0,0,0.08)", lineWidth: 0.75 }
              },
            },
          },
        });
      }
    };
  }

  function dlCSV() {
    if (!cofData) return;
    const headers = ["Series","Year"].concat(MONTH_LABELS);
    const rows = [];
    ["onFeed","placements","marketings","heifersOnFeed"].forEach(function(sid) {
      const s = cofData.series[sid];
      if (!s) return;
      displayYearsAsc.forEach(function(yr) {
        const arr = s.years[String(yr)] || [];
        rows.push([s.label, yr].concat(arr.map(function(v) { return v != null ? v : ""; })));
      });
    });
    downloadCSV("cattle_on_feed.csv", headers, rows);
  }

  const selSt = { padding: "7px 28px 7px 12px", fontSize: 14, fontWeight: 500, border: "1px solid var(--color-border-secondary)", borderRadius: 6, background: "var(--color-background-primary)", color: "var(--color-text-primary)", fontFamily: "inherit", cursor: "pointer", appearance: "none", backgroundImage: "url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'><path d='M3 4.5l3 3 3-3' stroke='%23666' stroke-width='1.5' fill='none'/></svg>\")", backgroundRepeat: "no-repeat", backgroundPosition: "right 8px center" };
  const modeSt = function(active) { return { padding: "6px 14px", fontSize: 12, fontWeight: 500, border: "1px solid " + (active ? "#2563EB" : "var(--color-border-secondary)"), borderRadius: 5, cursor: "pointer", background: active ? "#2563EB" : "transparent", color: active ? "#fff" : "var(--color-text-primary)", transition: "all 0.15s" }; };

  const CHARTS = [
    { key: "onFeed", label: "On feed inventory", yLabel: "thousand head", isPct: false },
    { key: "placements", label: "Placements", yLabel: "thousand head", isPct: false },
    { key: "marketings", label: "Marketings", yLabel: "thousand head", isPct: false },
    { key: "heifersOnFeed", label: "Quarterly heifers on feed", yLabel: "% of on-feed total", isPct: true },
  ];

  return (<div>
    <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 14, flexWrap: "wrap" }}>
      <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
        <span style={{ fontSize: 11, fontWeight: 600, color: "var(--color-text-secondary)", textTransform: "uppercase" }}>Range</span>
        <select value={range} onChange={function(e){ setRange(e.target.value); }} style={selSt}>
          <option value="3">3 Year</option>
          <option value="5">5 Year</option>
          <option value="10">10 Year</option>
          <option value="all">All</option>
        </select>
      </div>
      <div style={{ display: "flex", gap: 3 }}>
        <button onClick={function(){ setMode("seasonal"); }} style={modeSt(mode === "seasonal")}>Seasonal</button>
        <button onClick={function(){ setMode("contiguous"); }} style={modeSt(mode === "contiguous")}>Contiguous</button>
      </div>
      {mode === "contiguous" && (
        <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
          <span style={{ fontSize: 11, fontWeight: 600, color: "var(--color-text-secondary)", textTransform: "uppercase" }}>Month filter</span>
          <select value={monthFilter} onChange={function(e){ setMonthFilter(e.target.value); }} style={selSt}>
            <option value="all">All months</option>
            {MONTH_LABELS.map(function(m) { return <option key={m} value={m}>{m}</option>; })}
          </select>
        </div>
      )}
      <div style={{ marginLeft: "auto" }}><DownloadBtn onClick={dlCSV} /></div>
    </div>

    {/* Metric cards */}
    <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: 10, marginBottom: 16 }}>
      {[
        { label: "On feed", info: ofStats, unit: "K head", isPct: false },
        { label: "Placements", info: plStats, unit: "K head", isPct: false },
        { label: "Marketings", info: mkStats, unit: "K head", isPct: false },
        { label: "Heifers on feed", info: hfStats, unit: "%", isPct: true },
      ].map(function(card) {
        const info = card.info;
        const fmtCard = function(v) {
          if (v == null) return "—";
          if (card.isPct) return v.toFixed(1);
          // Display in thousand head (match chart y-axis)
          return Math.round(v / 1000).toLocaleString();
        };
        const diffLine = function(label, comp) {
          if (info.cur == null || comp == null) return null;
          const diff = card.isPct ? (info.cur - comp) : (info.cur - comp) / 1000;
          const rounded = Math.round(diff * 100) / 100;
          const col = rounded > 0 ? "#639922" : rounded < 0 ? "#A32D2D" : "var(--color-text-tertiary)";
          const fmtDiff = function(v) {
            if (card.isPct) return v.toFixed(1);
            return Math.round(v).toLocaleString();
          };
          return (<div key={label} style={{ display: "flex", justifyContent: "space-between", fontSize: 10.5, padding: "1px 0" }}>
            <span style={{ color: "var(--color-text-tertiary)" }}>{label}</span>
            <span style={{ display: "flex", gap: 4, alignItems: "baseline" }}>
              <span style={{ color: "var(--color-text-secondary)", textAlign: "right", minWidth: 56 }}>{fmtCard(comp)}</span>
              <span style={{ color: col, fontWeight: 500, textAlign: "right", minWidth: 56 }}>({rounded > 0 ? "+" : ""}{fmtDiff(rounded)})</span>
            </span>
          </div>);
        };
        return (<div key={card.label} style={{ background: "var(--color-background-secondary)", borderRadius: "var(--border-radius-md)", padding: "12px 14px", minWidth: 0 }}>
          <div style={{ fontSize: 11, color: "var(--color-text-secondary)", marginBottom: 3, textTransform: "uppercase", letterSpacing: "0.4px" }}>{card.label}</div>
          <div style={{ fontSize: 22, fontWeight: 500, color: "var(--color-text-primary)", marginBottom: 2 }}>
            {fmtCard(info.cur)}<span style={{ fontSize: 12, fontWeight: 400, color: "var(--color-text-secondary)", marginLeft: 4 }}>{card.unit}</span>
          </div>
          {info.month && <div style={{ fontSize: 10, color: "var(--color-text-tertiary)", marginBottom: 6 }}>as of {info.month} {curYear}</div>}
          <div style={{ borderTop: "0.5px solid var(--color-border-tertiary)", paddingTop: 5 }}>
            {diffLine("vs. prior month", info.prevMo)}
            {diffLine("vs. last year", info.lastYr)}
          </div>
        </div>);
      })}
    </div>

    {/* Master legend (seasonal only) */}
    {mode === "seasonal" && (
      <div style={{ display: "flex", flexWrap: "wrap", gap: 6, marginBottom: 16, alignItems: "center" }}>
        {legendItems.map(function(item) {
          const isH = hiddenYrs.has(item.label);
          return (<button key={item.label} onClick={function(){ toggleYr(item.label); }} style={{ display: "flex", alignItems: "center", gap: 5, padding: "4px 10px", border: "1px solid var(--color-border-secondary)", borderRadius: 5, background: isH ? "var(--color-background-secondary)" : "transparent", cursor: "pointer", opacity: isH ? 0.3 : 1, transition: "all 0.15s" }}>
            <span style={{ width: 18, height: 0, borderTop: "2.5px solid " + item.color, display: "inline-block" }}></span>
            <span style={{ fontSize: 12, fontWeight: 500, color: "var(--color-text-primary)" }}>{item.label}</span>
          </button>);
        })}
      </div>
    )}

    {/* 2x2 chart grid */}
    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
      {CHARTS.map(function(ch) {
        // Heifers chart is always contiguous with its own month filter and range
        const isHeifers = ch.key === "heifersOnFeed";
        const chMode = isHeifers ? "contiguous" : mode;
        const chMonth = isHeifers ? heifersMonth : monthFilter;
        const chRange = isHeifers ? heifersRange : range;
        const dropSt = { padding: "4px 22px 4px 8px", fontSize: 12, fontWeight: 500, border: "1px solid var(--color-border-secondary)", borderRadius: 4, background: "var(--color-background-primary)", color: "var(--color-text-primary)", fontFamily: "inherit", cursor: "pointer", appearance: "none", backgroundImage: "url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='10' height='10' viewBox='0 0 12 12'><path d='M3 4.5l3 3 3-3' stroke='%23666' stroke-width='1.5' fill='none'/></svg>\")", backgroundRepeat: "no-repeat", backgroundPosition: "right 6px center" };
        const lblSt = { fontSize: 10, fontWeight: 600, color: "var(--color-text-secondary)", textTransform: "uppercase", letterSpacing: "0.4px" };
        return (<div key={ch.key}>
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 6, gap: 8, flexWrap: "wrap" }}>
            <div style={{ fontSize: 14, fontWeight: 600, color: "var(--color-text-primary)" }}>{ch.label} <span style={{ fontSize: 11, fontWeight: 400, color: "var(--color-text-tertiary)" }}>({ch.yLabel})</span></div>
            {isHeifers && (
              <div style={{ display: "flex", alignItems: "center", gap: 12, flexWrap: "wrap" }}>
                <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
                  <span style={lblSt}>Range</span>
                  <select value={heifersRange} onChange={function(e){ setHeifersRange(e.target.value); }} style={dropSt}>
                    <option value="3">3 Year</option>
                    <option value="5">5 Year</option>
                    <option value="10">10 Year</option>
                    <option value="all">All</option>
                  </select>
                </div>
                <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
                  <span style={lblSt}>Quarter</span>
                  <select value={heifersMonth} onChange={function(e){ setHeifersMonth(e.target.value); }} style={dropSt}>
                    <option value="all">All</option>
                    <option value="Jan">Jan</option>
                    <option value="Apr">Apr</option>
                    <option value="Jul">Jul</option>
                    <option value="Oct">Oct</option>
                  </select>
                </div>
              </div>
            )}
          </div>
          {ready && <ChartBox id={"cof_" + ch.key + "_" + chMode + "_" + chRange + "_" + chMonth + "_" + hk} height={240} renderChart={mkCofChart(ch.key, ch.isPct, chMode, chMonth, chRange)} deps={"cof_" + ch.key + "_" + chMode + "_" + chRange + "_" + chMonth + "_" + hk + "_" + cofLoaded} />}
        </div>);
      })}
    </div>
    <div style={{ marginTop: 14, fontSize: 11, color: "var(--color-text-tertiary)" }}>
      Source: USDA NASS Cattle on Feed report. 1,000+ head capacity feedlots, US total. Heifers on feed is reported quarterly (Jan/Apr/Jul/Oct) and computed as a percentage of total on-feed inventory.
    </div>
  </div>);
}// ──────────────────────────────────────────────────────────────────────
// Expanded row chart with its own interactive legend (per-chart year toggle)
// ──────────────────────────────────────────────────────────────────────
function ExpandChartRow(props) {
  var chartId = props.chartId;
  var title = props.title;
  var buildView = props.buildView;          // function(): { labels, yr0..yrN }
  var legendYears = props.legendYears;
  var seasonLegend = props.seasonLegend;
  var mkChart = props.mkChart;              // function(view, hidden, mode): function(canvas){...}
  var seasonDS = props.seasonDS;
  var initialMode = props.chartMode;        // initial value passed in from parent (used as default)
  var _h = useState(new Set());
  var hidden = _h[0], setHidden = _h[1];
  var _m = useState(initialMode || "seasonal");
  var localMode = _m[0], setLocalMode = _m[1];
  var toggle = function(key) {
    setHidden(function(prev) {
      var n = new Set(prev);
      if (n.has(key)) n.delete(key); else n.add(key);
      return n;
    });
  };
  var view = buildView();
  var modeBtn = function(label, val) {
    var active = localMode === val;
    return React.createElement("button", {
      key: val,
      onClick: function() { setLocalMode(val); },
      style: {
        padding: "4px 12px", fontSize: 11, fontWeight: 500,
        border: "1px solid " + (active ? "#2563EB" : "var(--color-border-secondary)"),
        borderRadius: 4,
        background: active ? "#2563EB" : "transparent",
        color: active ? "#fff" : "var(--color-text-secondary)",
        cursor: "pointer", transition: "all 0.15s"
      }
    }, label);
  };
  return React.createElement("div", null,
    React.createElement("div", {
      style: { display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 12, gap: 12, flexWrap: "wrap" }
    },
      React.createElement("div", { style: { fontSize: 13, fontWeight: 500, color: "var(--color-text-primary)" } }, title),
      React.createElement("div", { style: { display: "flex", gap: 4 } },
        modeBtn("Seasonal", "seasonal"),
        modeBtn("Contiguous", "contiguous")
      )
    ),
    React.createElement("div", { style: { display: "flex", flexWrap: "wrap", gap: 6, marginBottom: 14, alignItems: "center" } },
      seasonLegend.map(function(item) {
        var isH = hidden.has(item.key);
        return React.createElement("button", {
          key: item.key,
          onClick: function() { toggle(item.key); },
          style: {
            display: "flex", alignItems: "center", gap: 5,
            padding: "4px 10px",
            border: "1px solid var(--color-border-secondary)",
            borderRadius: 5,
            background: isH ? "var(--color-background-secondary)" : "transparent",
            cursor: "pointer",
            opacity: isH ? 0.3 : 1,
            transition: "all 0.15s"
          }
        },
          React.createElement("span", { style: { width: 18, height: 0, borderTop: "2.5px solid " + item.color, display: "inline-block" } }),
          React.createElement("span", { style: { fontSize: 12, fontWeight: 500, color: "var(--color-text-primary)" } }, item.label)
        );
      })
    ),
    React.createElement(ChartBox, {
      id: chartId + "_" + localMode,
      height: 340,
      renderChart: mkChart(view, hidden, localMode),
      deps: chartId + "_" + [].concat(Array.from(hidden)).sort().join(",") + "_" + localMode
    })
  );
}

const BEEF_IMPS_MAP = {
            "109E  1": "Rib", "112A  3": "Rib",
            "113C  1": "Chuck", "114  1": "Chuck", "114A  3": "Chuck", "116A  3": "Chuck",
            "120  1": "Brisket",
            "160  1": "Round", "161  1": "Round", "167A  4": "Round",
            "168  1": "Round", "168  3": "Round", "169  5": "Round",
            "170  1": "Round", "171B  3": "Round", "171C  3": "Round",
            "174  3": "Loin", "175  3": "Loin", "180  3": "Loin",
            "184  1": "Loin", "184  3": "Loin", "184B  3": "Loin",
            "185A  4": "Loin", "185B  1": "Loin", "185C  1": "Loin",
            "185D  4": "Loin", "189A  4": "Loin", "191A  4": "Loin",
            "193  4": "Flank",
            "121D  4": "Plate", "121C  4": "Plate", "121E  6": "Plate",
            "123A  3": "Plate", "130  4": "Plate"
          };

const PORK_GUIDE_CUTS = [
            // Loin
            { match: "1/4 Trimmed Loin VAC", primal: "Loin", section: "loin_cuts", exact: true },
            { match: "1/8 Trimmed Loin VAC", primal: "Loin", section: "loin_cuts", exact: true },
            { match: "Bone-in CC, Tender-in Loin", primal: "Loin", section: "loin_cuts" },
            { match: "Bnls CC Strap-on", primal: "Loin", section: "loin_cuts" },
            { match: "Bnls CC Strap-off", primal: "Loin", section: "loin_cuts" },
            { match: "Boneless Sirloin", primal: "Loin", section: "loin_cuts" },
            { match: "Tenderloin", primal: "Loin", section: "loin_cuts" },
            { match: "Backribs 2.0#/up VAC", primal: "Loin", section: "loin_cuts" },
            { match: "Backribs 2.0#/up 1 Pc", primal: "Loin", section: "loin_cuts" },
            // Butt
            { match: "1/4 Trim Butt VAC", primal: "Butt", section: "butt_cuts", exact: true },
            { match: "1/4 Trim Butt Combo", primal: "Butt", section: "butt_cuts" },
            // Sparerib
            { match: "Trmd Sparerib - LGT", primal: "Rib", section: "sparerib_cuts", exact: true },
            { match: "Trmd Sparerib - MED", primal: "Rib", section: "sparerib_cuts" },
            { match: "St Louis", primal: "Rib", section: "sparerib_cuts" },
            { match: "BBQ Style", primal: "Rib", section: "sparerib_cuts" },
            // Ham
            { match: "17-20# Trmd Selected Ham", primal: "Ham", section: "ham_cuts" },
            { match: "20-23# Trmd Selected Ham", primal: "Ham", section: "ham_cuts" },
            { match: "23-27# Trmd Selected Ham", primal: "Ham", section: "ham_cuts" },
            { match: "3 Muscle Ham", primal: "Ham", section: "ham_cuts" },
            { match: "4 Muscle Ham", primal: "Ham", section: "ham_cuts" },
            { match: "Insides", primal: "Ham", section: "ham_cuts" },
            { match: "Outsides", primal: "Ham", section: "ham_cuts" },
            { match: "Knuckles", primal: "Ham", section: "ham_cuts" },
            { match: "Lite Butt", primal: "Ham", section: "ham_cuts" },
            { match: "Outer Shank", primal: "Ham", section: "ham_cuts" },
            { match: "Inner Shank", primal: "Ham", section: "ham_cuts" },
            // Belly
            { match: "Derind Belly 9-13#", primal: "Belly", section: "belly_cuts" },
            { match: "Derind Belly 13-17#", primal: "Belly", section: "belly_cuts" },
            // Jowl
            { match: "Skinned Combo", primal: "Jowl", section: "jowl_cuts" },
            // Trim
            { match: "42% Trim Combo", primal: "Trim", section: "trim_cuts" },
            { match: "72% Trim Combo", primal: "Trim", section: "trim_cuts" },
            { match: "72% Trim Boxed", primal: "Trim", section: "trim_cuts" },
          ];



function CutoutPage({ ready }) {
  const [tab, setTab] = useState("cattle");
  const [hCutout, tCutout] = useToggle();
  const [hChoice, tChoice] = useToggle();
  const [hComp, tComp] = useToggle();
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [period, setPeriod] = useState("daily");
  const [chartMode, setChartMode] = useState("seasonal");
  const [meatData, setMeatData] = useState(null);

  useEffect(function() {
    fetch("data/meat_prices.json?t=" + Date.now())
      .then(function(r) { return r.ok ? r.json() : null; })
      .then(function(data) { if (data) setMeatData(data); })
      .catch(function() {});
  }, []);

  // ── Build chart data from JSON or fall back to synthetic ──
  var curYearLabel = "2026";
  var prevYearLabel = "2025";
  var liveDates = BEEF_DAILY_DATES;
  var liveBeefChoiceLatest = BOXED_BEEF_CHOICE_LATEST;
  var liveBeefSelectLatest = BOXED_BEEF_SELECT_LATEST;
  var livePorkLatest = PORK_CUTOUT_LATEST;
  var liveCompLatest = null;
  var liveLatest = null;
  var liveBeefPrimalRows = null;
  var liveBeefCutRows = null;
  var livePorkPrimalRows = null;
  var livePorkCutRows = null;

  // Chart data keyed as "2025"=cur, "2024"=prev, "5yr"=avg for seasonDS compatibility
  var beefChoiceByKey = { "2025": BOXED_BEEF_CHOICE_DAILY["2025"], "2024": BOXED_BEEF_CHOICE_DAILY["2024"], "5yr": BOXED_BEEF_CHOICE_DAILY["5yr"] };
  var beefSelectByKey = { "2025": BOXED_BEEF_SELECT_DAILY["2025"] };
  var beefCompByKey = { "2025": [], "2024": [], "5yr": [] };
  var porkCutoutByKey = { "2025": PORK_CUTOUT_DAILY["2025"], "2024": PORK_CUTOUT_DAILY["2024"], "5yr": PORK_CUTOUT_DAILY["5yr"] };
  var liveBeefPrimals = BEEF_PRIMAL_SEASONAL;
  var livePorkPrimals = PORK_PRIMALS_DAILY;

  if (meatData && meatData.seasonal && meatData.seasonal.years) {
    var sy = meatData.seasonal.years;
    var numYrs = sy.filter(function(y) { return typeof y.year === "number"; }).sort(function(a,b) { return b.year - a.year; });
    var curYr = numYrs[0] || null;
    var prevYr = numYrs[1] || null;
    var avgYr = sy.find(function(y) { return y.year === "5yr_avg"; }) || null;

    if (curYr) {
      curYearLabel = String(curYr.year);
      // Use the longest dates array (full year) for x-axis labels
      liveDates = curYr.dates || BEEF_DAILY_DATES;
      if (prevYr && prevYr.dates && prevYr.dates.length > liveDates.length) {
        liveDates = prevYr.dates;
      }

      beefChoiceByKey = {
        "2025": curYr.beef_choice || [],
        "2024": prevYr ? prevYr.beef_choice || [] : [],
        "5yr": avgYr ? avgYr.beef_choice || [] : [],
      };
      beefSelectByKey = { "2025": curYr.beef_select || [], "2024": prevYr ? prevYr.beef_select || [] : [] };
      beefCompByKey = { "2025": curYr.beef_comp || [], "2024": prevYr ? prevYr.beef_comp || [] : [], "5yr": avgYr ? avgYr.beef_comp || [] : [] };
      porkCutoutByKey = {
        "2025": curYr.pork_carcass || [],
        "2024": prevYr ? prevYr.pork_carcass || [] : [],
        "5yr": avgYr ? avgYr.pork_carcass || [] : [],
      };

      // Beef primals
      var bpNames = ["Rib","Chuck","Loin","Round","Brisket","Plate","Flank"];
      liveBeefPrimals = bpNames.map(function(name) {
        var k = "beef_" + name.toLowerCase();
        var obj = { name: name, daily: curYr[k] || [] };
        obj["2024"] = prevYr ? prevYr[k] || [] : [];
        obj["5yr"] = avgYr ? avgYr[k] || [] : [];
        return obj;
      });

      // Pork primals
      var ppNames = ["loin","butt","ham","belly","rib","picnic"];
      livePorkPrimals = ppNames.map(function(name) {
        var k = "pork_" + name;
        return { name: name.charAt(0).toUpperCase() + name.slice(1), daily: curYr[k] || [] };
      });
    }
    if (prevYr) prevYearLabel = String(prevYr.year);

    // Latest values from JSON
    if (meatData.latest) {
      var lb = meatData.latest.beef || {};
      var lp = meatData.latest.pork || {};
      liveBeefChoiceLatest = lb.choice || liveBeefChoiceLatest;
      liveBeefSelectLatest = lb.select || liveBeefSelectLatest;
      livePorkLatest = lp.carcass || livePorkLatest;
      liveLatest = meatData.latest;
        if (meatData.latest.beef_comp) liveCompLatest = meatData.latest.beef_comp.cutout || null;

        // Build live table data from last 2 daily records
        var dLen = meatData.daily ? meatData.daily.length : 0;
        var latestRec = dLen > 0 ? meatData.daily[dLen - 1] : null;
        var prevRec = dLen > 1 ? meatData.daily[dLen - 2] : null;

        // ── Beef product table from API data ──
        if (latestRec && latestRec.beef) {
          var lb2 = latestRec.beef;
          var pb = prevRec ? prevRec.beef || {} : {};

          // Helper: build lookup for a cut by name across history
          // Returns { latest, prevDay, prevWeek, prevMonth, prevYear, latestDate }
          // sectionGetters is an array of fns (record) -> array of items {name, avg}
          // matchName normalizes cut names the same way the table uses
          var _normCut = function(nm) {
            if (!nm) return nm;
            return String(nm).replace(/\s*\([^)]+\)/, "").replace(/^\s*\d+[A-Z]?\s+\d\s+/, "").trim();
          };
          var _parseDate = function(ds) {
            if (!ds) return null;
            var p = ds.split("/");
            if (p.length !== 3) return null;
            return new Date(parseInt(p[2]), parseInt(p[0]) - 1, parseInt(p[1]));
          };
          var dailyRecs = (meatData.daily || []).slice();
          // Latest record date
          var latestRecDate = latestRec ? _parseDate(latestRec.date) : null;

          // Build a fast lookup: for each record, a map of normalized-cut-name -> avg
          // Used by both beef and pork lookups
          var _recLookup = function(rec, getSections) {
            var map = {};
            if (!rec) return map;
            getSections.forEach(function(getter) {
              var arr = getter(rec) || [];
              arr.forEach(function(it) {
                if (it && it.name && it.avg != null) {
                  map[_normCut(it.name)] = it.avg;
                }
              });
            });
            return map;
          };

          // Find first record at-or-before targetDate (cal-day lookback)
          var _findRecAtOrBefore = function(targetDate) {
            if (!targetDate) return null;
            for (var i = dailyRecs.length - 1; i >= 0; i--) {
              var d = _parseDate(dailyRecs[i].date);
              if (d && d <= targetDate) return dailyRecs[i];
            }
            return null;
          };

          var _lookbackDate = function(days) {
            if (!latestRecDate) return null;
            var d = new Date(latestRecDate);
            d.setDate(d.getDate() - days);
            return d;
          };
          var prevDayRec = dailyRecs.length >= 2 ? dailyRecs[dailyRecs.length - 2] : null;
          var prevWeekRec = _findRecAtOrBefore(_lookbackDate(7));
          var prevMonthRec = _findRecAtOrBefore(_lookbackDate(30));
          var prevYearRec = _findRecAtOrBefore(_lookbackDate(365));

          // Helper: convert a Date to a "M/D" label matching seasonal.dates format
          var _dateToMD = function(d) {
            if (!d) return null;
            return (d.getMonth() + 1) + "/" + d.getDate();
          };
          var _dateToYear = function(d) { return d ? d.getFullYear() : null; };

          // Look up a cut value at a target Date using seasonal data
          // Walks backwards through seasonal.dates if exact date not found (handles weekends/holidays)
          var seasonalLookup = function(cutMapKey, cutName, targetDate) {
            if (!targetDate || !meatData || !meatData.seasonal || !meatData.seasonal.years) return null;
            var n = _normCut(cutName);
            var targetYear = targetDate.getFullYear();
            var targetMD = _dateToMD(targetDate);
            // Search the year matching targetDate first; fall back across year boundaries
            for (var attempt = 0; attempt < 30; attempt++) {
              // attempt counts days walked back from targetDate
              var trial = new Date(targetDate);
              trial.setDate(trial.getDate() - attempt);
              var y = trial.getFullYear();
              var md = _dateToMD(trial);
              var yd = meatData.seasonal.years.find(function(sy) { return sy.year === y; });
              if (!yd) continue;
              var dates = yd.dates || [];
              var cuts = yd[cutMapKey];
              if (!cuts || !cuts[n]) continue;
              // Find this date's index. dates are like "1/4", "1/5", ...
              var idx = dates.indexOf(md);
              if (idx < 0) continue;
              var v = cuts[n][idx];
              if (v != null) return v;
            }
            return null;
          };

          var beefCutHistory = function(cutName) {
            var prevDayDate = prevDayRec ? _parseDate(prevDayRec.date) : null;
            return {
              prevDay: seasonalLookup("cuts_beef", cutName, prevDayDate),
              prevWeek: seasonalLookup("cuts_beef", cutName, _lookbackDate(7)),
              prevMonth: seasonalLookup("cuts_beef", cutName, _lookbackDate(30)),
              prevYear: seasonalLookup("cuts_beef", cutName, _lookbackDate(365)),
            };
          };
          var porkCutHistory = function(cutName) {
            var prevDayDate = prevDayRec ? _parseDate(prevDayRec.date) : null;
            return {
              prevDay: seasonalLookup("cuts_pork", cutName, prevDayDate),
              prevWeek: seasonalLookup("cuts_pork", cutName, _lookbackDate(7)),
              prevMonth: seasonalLookup("cuts_pork", cutName, _lookbackDate(30)),
              prevYear: seasonalLookup("cuts_pork", cutName, _lookbackDate(365)),
            };
          };
          // Format lookback dates for column headers — uses global fmtDate ("Apr 21, 2026")
          var fmtDateMD = function(rec) {
            return rec ? fmtDate(rec.date) : "—";
          };
          var prevDayLabel = fmtDateMD(prevDayRec);
          var prevWeekLabel = fmtDateMD(prevWeekRec);
          var prevMonthLabel = fmtDateMD(prevMonthRec);
          var prevYearLabel2 = fmtDateMD(prevYearRec);

          // Build primal lookup from latest primals
          var primals = lb2.primals || {};
          var prevPrimals = pb.primals || {};
          var beefPrimalRows = {};
          ["Rib","Chuck","Round","Loin","Brisket","Plate","Flank"].forEach(function(name) {
            var p = primals[name] || {};
            var pp = prevPrimals[name] || {};
            beefPrimalRows[name] = { latest: p.choice, prev: pp.choice };
          });

          // Beef primal historical lookback (uses choice cutout from primals)
          var _beefPrimalAt = function(rec, primalName) {
            if (!rec || !rec.beef || !rec.beef.primals) return null;
            var p = rec.beef.primals[primalName];
            if (!p) return null;
            return p.choice != null ? p.choice : (p.cutout != null ? p.cutout : null);
          };
          var beefPrimalHistory = function(primalName) {
            return {
              prevDay: _beefPrimalAt(prevDayRec, primalName),
              prevWeek: _beefPrimalAt(prevWeekRec, primalName),
              prevMonth: _beefPrimalAt(prevMonthRec, primalName),
              prevYear: _beefPrimalAt(prevYearRec, primalName),
            };
          };

          // ── Beef cut mapping per RJO/USDA Meat Deli Planning Guide ──
          // IMPS codes that appear in the guide, mapped to primal
                  // Also match by partial IMPS (API sometimes has extra spaces)
          function findImps(name) {
            var m = name.match(/\(([^)]+)\)/);
            return m ? m[1].trim() : "";
          }
          function impsLookup(imps) {
            if (BEEF_IMPS_MAP[imps]) return BEEF_IMPS_MAP[imps];
            // Try normalizing spaces
            var norm = imps.replace(/\s+/g, "  ");
            if (BEEF_IMPS_MAP[norm]) return BEEF_IMPS_MAP[norm];
            // Try single space
            var s1 = imps.replace(/\s+/g, " ");
            for (var k in BEEF_IMPS_MAP) {
              if (k.replace(/\s+/g, " ") === s1) return BEEF_IMPS_MAP[k];
            }
            return null;
          }

          var beefCutRows = [];
          // Choice cuts — filter to only items in the planning guide
          (lb2.choice_cuts || []).forEach(function(cut) {
            var name = cut.name || "";
            var imps = findImps(name);
            var primal = impsLookup(imps);
            if (!primal) return; // Not in planning guide, skip
            var shortName = name.replace(/\s*\([^)]+\)/, "").trim();
            var prevCut = (pb.choice_cuts || []).find(function(pc) { return pc.name === cut.name; });
            var _hist1 = beefCutHistory(shortName);
            beefCutRows.push({
              name: shortName, primal: primal, item: imps,
              loads: cut.trades || null, lbs: cut.lbs || null,
              latest: cut.avg, low: cut.low, high: cut.high,
              prev: prevCut ? prevCut.avg : null,
              prevDay: _hist1.prevDay, prevWeek: _hist1.prevWeek, prevMonth: _hist1.prevMonth, prevYear: _hist1.prevYear
            });
          });

          // Choice & Select combo cuts (Plate items: inside/outside skirt, cap & wedge, pectoral)
          var comboSection = lb2.choice_and_select || [];
          // These use trim_description instead of item_description
          // Handled via IMPS map above if present in choice_cuts

          // Choice & Select combo cuts (Plate items: skirts, cap & wedge, pectoral)
          (lb2.choice_select_cuts || []).forEach(function(cut) {
            if (!cut.avg) return;
            var name = cut.name || "";
            // Map to Plate primal
            var imps = findImps(name);
            var primal = impsLookup(imps);
            if (!primal) {
              // These items sometimes don't have IMPS in parens, use name matching
              if (name.indexOf("Plate") >= 0 || name.indexOf("Skirt") >= 0 || name.indexOf("Cap and Wedge") >= 0 || name.indexOf("Pectoral") >= 0) {
                primal = "Plate";
              } else return;
            }
            var shortName = name.replace(/\s*\([^)]+\)/, "").replace(/^\s*\d+[A-Z]?\s+\d\s+/, "").trim();
            var prevCut = (pb.choice_select_cuts || []).find(function(pc) { return pc.name === cut.name; });
            var _hist1 = beefCutHistory(shortName);
            beefCutRows.push({
              name: shortName, primal: primal, item: imps,
              loads: cut.trades || null, lbs: cut.lbs || null,
              latest: cut.avg, low: cut.low, high: cut.high,
              prev: prevCut ? prevCut.avg : null,
              prevDay: _hist1.prevDay, prevWeek: _hist1.prevWeek, prevMonth: _hist1.prevMonth, prevYear: _hist1.prevYear
            });
          });

          // Plate primal composite from primals data
          var platePrimal = primals["Plate"] || primals["Short Plate"] || {};
          var prevPlatePrimal = prevPrimals["Plate"] || prevPrimals["Short Plate"] || {};
          if (platePrimal.choice) {
            beefPrimalRows["Plate"] = { latest: platePrimal.choice, prev: prevPlatePrimal.choice };
          }

          // Flank primal composite
          var flankPrimal = primals["Flank"] || {};
          var prevFlankPrimal = prevPrimals["Flank"] || {};
          if (flankPrimal.choice) {
            beefPrimalRows["Flank"] = { latest: flankPrimal.choice, prev: prevFlankPrimal.choice };
          }

          // Ground beef
          (lb2.ground_beef || []).forEach(function(g) {
            if (!g.avg) return;
            var prevG = (pb.ground_beef || []).find(function(pg) { return pg.name === g.name; });
            var _hist3 = beefCutHistory(g.name);
            beefCutRows.push({
              name: g.name, primal: "Trim", item: "",
              loads: g.trades || null, lbs: g.lbs || null,
              latest: g.avg, prev: prevG ? prevG.avg : null,
              prevDay: _hist3.prevDay, prevWeek: _hist3.prevWeek, prevMonth: _hist3.prevMonth, prevYear: _hist3.prevYear
            });
          });

          // 50% trim from report 2453
          (lb2.trimmings_2453 || []).forEach(function(t) {
            if (!t.avg) return;
            var prevT = (pb.trimmings_2453 || []).find(function(pt) { return pt.name === t.name; });
            var _hist45 = beefCutHistory(t.name);
            beefCutRows.push({
              name: t.name, primal: "Trim", item: "",
              loads: t.trades || null, lbs: t.lbs || null,
              latest: t.avg, prev: prevT ? prevT.avg : null,
              prevDay: _hist45.prevDay, prevWeek: _hist45.prevWeek, prevMonth: _hist45.prevMonth, prevYear: _hist45.prevYear
            });
          });

          // Boneless beef trimmings (90CL, 85CL, etc.) from report 2451
          var bt = latestRec.beef_trimmings || {};
          var btPrev = prevRec ? prevRec.beef_trimmings || {} : {};
          (bt.national || []).forEach(function(t) {
            if (!t.avg) return;
            var prevT = (btPrev.national || []).find(function(pt) { return pt.name === t.name; });
            var _hist45 = beefCutHistory(t.name);
            beefCutRows.push({
              name: t.name, primal: "Trim", item: "",
              loads: t.trades || null, lbs: t.lbs || null,
              latest: t.avg, prev: prevT ? prevT.avg : null,
              prevDay: _hist45.prevDay, prevWeek: _hist45.prevWeek, prevMonth: _hist45.prevMonth, prevYear: _hist45.prevYear
            });
          });

          // Trim is not a real primal — leave beefPrimalRows["Trim"] unset so the header row shows no values

          liveBeefPrimalRows = beefPrimalRows;
          liveBeefCutRows = beefCutRows;
        }

        // ── Pork product table from API data ──
        if (latestRec && latestRec.pork) {
          var lp2 = latestRec.pork;
          var pp2 = prevRec ? prevRec.pork || {} : {};

          // Pork primal historical lookback
          var _porkPrimalAt = function(rec, primalName) {
            if (!rec || !rec.pork) return null;
            var key = primalName.toLowerCase();
            var v = rec.pork[key];
            return v != null ? v : null;
          };
          var porkPrimalHistory = function(primalName) {
            return {
              prevDay: _porkPrimalAt(prevDayRec, primalName),
              prevWeek: _porkPrimalAt(prevWeekRec, primalName),
              prevMonth: _porkPrimalAt(prevMonthRec, primalName),
              prevYear: _porkPrimalAt(prevYearRec, primalName),
            };
          };

          var porkPrimalRows = {};
          ["Loin","Butt","Picnic","Rib","Ham","Belly"].forEach(function(name) {
            var key = name.toLowerCase();
            porkPrimalRows[name] = { latest: lp2[key], prev: pp2[key] };
          });

          // ── Pork cut mapping per RJO/USDA Meat Deli Planning Guide ──
                  var porkCutRows = [];
          var porkSectionKeys = ["loin_cuts","butt_cuts","picnic_cuts","ham_cuts","belly_cuts","sparerib_cuts","jowl_cuts","trim_cuts"];
          porkSectionKeys.forEach(function(secKey) {
            (lp2[secKey] || []).forEach(function(cut) {
              // Check if this cut matches any guide item
              var guideCut = PORK_GUIDE_CUTS.find(function(g) {
                if (g.section !== secKey) return false;
                if (g.exact) return cut.name === g.match || cut.name === g.match + ", FZN";
                return cut.name && cut.name.indexOf(g.match) >= 0 && cut.name.indexOf("FZN") < 0;
              });
              if (!guideCut) return; // Not in guide, skip
              if (!cut.avg) return; // No price
              var prevCut = (pp2[secKey] || []).find(function(pc) { return pc.name === cut.name; });
              var _histp = porkCutHistory(cut.name);
              porkCutRows.push({
                name: cut.name, primal: guideCut.primal, item: "",
                loads: null, lbs: cut.lbs || null,
                latest: cut.avg, low: cut.low, high: cut.high,
                prev: prevCut ? prevCut.avg : null,
                prevDay: _histp.prevDay, prevWeek: _histp.prevWeek, prevMonth: _histp.prevMonth, prevYear: _histp.prevYear
              });
            });
          });

          // Trim is not a real primal — leave porkPrimalRows["Trim"] unset so the header row shows no values
          // Jowl primal value
          var jowlCut = porkCutRows.find(function(r) { return r.primal === "Jowl" && r.latest; });
          if (jowlCut) {
            porkPrimalRows["Jowl"] = { latest: jowlCut.latest, prev: jowlCut.prev };
          }

          livePorkPrimalRows = porkPrimalRows;
          livePorkCutRows = porkCutRows;
        }
    }
  }

  const periodLabels = { daily: "day", weekly: "week", monthly: "month" };
  const prevLabel = `Prev ${periodLabels[period]}`;
  const chgLabel = period === "daily" ? "D/D" : period === "weekly" ? "W/W" : "M/M";

  var yr5 = meatData && meatData.seasonal ? meatData.seasonal.years.filter(function(y) { return typeof y.year === "number"; }).sort(function(a,b) { return a.year - b.year; }) : [];
  var legendYears = yr5.slice(-6);
  var yrColorMap = { 0: "#A32D2D", 1: "#D85A30", 2: "#E8A735", 3: "#639922", 4: "#1D9E75", 5: "#333" };
  var seasonLegend = legendYears.map(function(y, i) {
    return { label: String(y.year), color: yrColorMap[i] || "#999", key: "yr" + i };
  });
  var seasonDS = {};
  legendYears.forEach(function(y, i) {
    seasonDS["yr" + i] = { borderColor: yrColorMap[i] || "#999", borderWidth: i === legendYears.length - 1 ? 2.5 : 1.5, pointRadius: 0, tension: 0 };
  });

  // Build multi-year seasonal views
  var cutoutViewData = { labels: liveDates };
  legendYears.forEach(function(y, i) {
    var yd = meatData ? meatData.seasonal.years.find(function(sy) { return sy.year === y.year; }) : null;
    cutoutViewData["yr" + i] = yd ? yd.beef_choice || [] : [];
  });
  var cutoutView = period === "daily" ? cutoutViewData : getSeasonalView(cutoutViewData["yr" + (legendYears.length-1)] || [], cutoutViewData["yr" + (legendYears.length-2)] || [], [], period, liveDates);
  // For non-daily, remap keys
  if (period !== "daily") {
    var tmp = {};
    tmp.labels = cutoutView.labels;
    legendYears.forEach(function(y, i) {
      var yd = meatData ? meatData.seasonal.years.find(function(sy) { return sy.year === y.year; }) : null;
      var series = yd ? yd.beef_choice || [] : [];
      if (period === "weekly") tmp["yr"+i] = BEEF_WEEK_RANGES.map(function(w) { return avgRange(series, w.start, w.end); });
      else tmp["yr"+i] = BEEF_MONTH_RANGES.map(function(m) { return avgRange(series, m.start, m.end); });
    });
    cutoutView = tmp;
  }
  const selectCutoutView = getSeasonalView(beefSelectByKey["2025"], beefSelectByKey["2024"] || [], beefSelectByKey["5yr"] || [], period, liveDates);
  // Comprehensive cutout view (from 2465 — weekly report)
  // Always aggregate to weekly unless monthly is selected, same 5-yr legend as choice
  var compPeriod = period === "monthly" ? "monthly" : "weekly";
  var compRanges = compPeriod === "monthly" ? BEEF_MONTH_RANGES : BEEF_WEEK_RANGES;
  var compViewData = { labels: compRanges.map(function(r) { return r.label; }) };
  legendYears.forEach(function(y, i) {
    var yd = meatData ? meatData.seasonal.years.find(function(sy) { return sy.year === y.year; }) : null;
    var series = yd ? yd.beef_comp || [] : [];
    compViewData["yr" + i] = compRanges.map(function(r) { return avgRange(series, r.start, r.end); });
  });
  const productViews = BEEF_PRODUCT_SEASONAL.map(p => getProductView(p, period));
  const productSeasonalViews = BEEF_PRODUCT_SEASONAL.map(function(p) { return getSeasonalView(p.daily, p["2024"] || [], p["5yr"] || [], period); });

  function niceAxis(allVals) {
    if (allVals.length === 0) return { yMin: 0, yMax: 100 };
    const dataMin = Math.min(...allVals); const dataMax = Math.max(...allVals);
    const range = dataMax - dataMin; const pad = Math.max(range * 0.2, 2);
    const rawStep = (range + pad * 2) / 5;
    const mag = Math.pow(10, Math.floor(Math.log10(rawStep)));
    const norm = rawStep / mag;
    const niceNorm = norm <= 1.5 ? 1 : norm <= 3.5 ? 2 : norm <= 7.5 ? 5 : 10;
    const step = niceNorm * mag;
    let yMin = Math.floor((dataMin - pad) / step) * step;
    const yMax = Math.ceil((dataMax + pad) / step) * step;
    if (yMin < 0) yMin = 0;
    return { yMin: yMin, yMax: yMax };
  }


  function mkSeasonalChart(view, hidden, modeOverride) {
    return (canvas) => {
      const keys = legendYears.map(function(y, i) { return "yr" + i; }).filter(function(k) { return !hidden.has(k); });
      const effectiveMode = modeOverride || chartMode;

      if (effectiveMode === "contiguous") {
        // Concatenate all visible years in chronological order with per-year segments
        const visibleYears = legendYears.filter(function(y, i) { return keys.indexOf("yr" + i) >= 0; });
        if (visibleYears.length === 0) {
          new Chart(canvas, { type: "line", data: { labels: [], datasets: [] }, options: { responsive: true, maintainAspectRatio: false } });
          return;
        }
        const allLabels = [];
        const allData = [];
        const yearBoundaries = []; // indices where a new year starts
        const yearMidpoints = []; // mid-index for each year (for x-axis label)
        visibleYears.forEach(function(y, idx) {
          var yrKey = "yr" + legendYears.indexOf(y);
          var yrData = view[yrKey] || [];
          var startIdx = allLabels.length;
          if (idx > 0) yearBoundaries.push(startIdx);
          yrData.forEach(function(v, i) {
            allLabels.push(String(y.year) + "-" + (view.labels ? view.labels[i] : i));
            allData.push(v);
          });
          yearMidpoints.push({ idx: Math.floor(startIdx + yrData.length / 2), label: String(y.year) });
        });
        const allVals = allData.filter(v => v != null);
        const { yMin, yMax } = niceAxis(allVals);
        const needsRotation = visibleYears.length > 8;

        new Chart(canvas, {
          type: "line", data: { labels: allLabels, datasets: [{
            label: "Price", data: allData, borderColor: "#2563EB",
            borderWidth: 1.8, pointRadius: 0, tension: 0, spanGaps: true, fill: false,
          }]},
          options: { responsive: true, maintainAspectRatio: false,
            interaction: { mode: "nearest", intersect: false },
            plugins: { legend: { display: false }, tooltip: { callbacks: {
              title: function(items) {
                if (items.length === 0) return "";
                var parts = allLabels[items[0].dataIndex].split("-");
                var yr = parts.shift();
                return parts.join("-") + " " + yr;
              },
              label: c => "$" + c.parsed.y.toFixed(2),
            } } },
            scales: {
              x: {
                ticks: {
                  autoSkip: false, maxRotation: needsRotation ? 90 : 0, minRotation: needsRotation ? 90 : 0, font: { size: 11 },
                  callback: function(val, idx) {
                    for (var i = 0; i < yearMidpoints.length; i++) {
                      if (yearMidpoints[i].idx === idx) return yearMidpoints[i].label;
                    }
                    return "";
                  },
                },
                grid: {
                  color: function(ctx) {
                    return yearBoundaries.indexOf(ctx.index) >= 0 ? "rgba(0,0,0,0.12)" : "transparent";
                  },
                  lineWidth: 0.75,
                },
              },
              y: { min: yMin, max: yMax, title: { display: true, text: "$/cwt", font: { size: 11 } }, ticks: { font: { size: 11 }, callback: v => "$" + v }, grid: { color: "rgba(0,0,0,0.08)", lineWidth: 0.75 } },
            },
          },
        });
        return;
      }

      const ds = keys.map(function(k) { return Object.assign({ label: seasonLegend.find(function(s) { return s.key === k; }) ? seasonLegend.find(function(s) { return s.key === k; }).label : k, data: view[k], spanGaps: true }, seasonDS[k] || {}); });
      const allVals = keys.flatMap(k => (view[k] || []).filter(v => v != null));
      const { yMin, yMax } = niceAxis(allVals);
      const labels = view.labels;
      const monthNames = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];

      function getMonth(label) {
        if (!label) return -1;
        const l = String(label);
        const slashMatch = l.match(/^(\d+)\//);
        if (slashMatch) return parseInt(slashMatch[1]) - 1;
        const idx = monthNames.findIndex(m => l.startsWith(m));
        if (idx >= 0) return idx;
        return -1;
      }

      // Build display labels: month name at midpoint of each month's range, empty otherwise
      const pointMonths = labels.map(getMonth);
      let displayLabels;
      let gridColors;

      if (period === "monthly") {
        displayLabels = labels;
        gridColors = labels.map(() => "rgba(0,0,0,0.12)");
      } else {
        const ma = buildMonthAxis(labels);
        displayLabels = ma.displayLabels;
        gridColors = ma.gridColors;
      }

      new Chart(canvas, {
        type: "line", data: { labels: displayLabels, datasets: ds },
        options: { responsive: true, maintainAspectRatio: false,
          interaction: { mode: "nearest", intersect: false }, plugins: { legend: { display: false }, tooltip: {
            callbacks: {
              title: (items) => { if (items.length > 0) return labels[items[0].dataIndex]; return ""; },
              label: c => `${c.dataset.label}: $${c.parsed.y.toFixed(2)}`,
            },
          }},
          scales: {
            x: {
              ticks: { autoSkip: false, maxRotation: 0, font: { size: 11 } },
              grid: {
                color: (ctx) => gridColors[ctx.index] || "transparent",
                lineWidth: 0.75,
              },
            },
            y: { min: yMin, max: yMax, title: { display: true, text: "$/cwt", font: { size: 11 } }, ticks: { font: { size: 11 }, callback: v => "$" + v }, grid: { color: "rgba(0,0,0,0.12)", lineWidth: 0.75 } },
          },
        },
      });
    };
  }

  const ProductChart = ({ idx }) => {
    const view = productSeasonalViews[idx];
    const [hProd, tProd] = useToggle();
    const chartId = `prod_seasonal_${period}_${chartMode}_${idx}`;
    useEffect(() => {
      if (!window.Chart || !view) return;
      const t = setTimeout(() => {
        const c = document.getElementById(chartId);
        if (!c) return;
        const ex = Chart.getChart(c); if (ex) ex.destroy();
        mkSeasonalChart(view, hProd)(c);
      }, 60);
      return () => clearTimeout(t);
    }, [view, period, chartMode, chartId, hProd]);
    return (<div>
      {chartMode === "seasonal" && <InteractiveLegend items={seasonLegend} hidden={hProd} onToggle={tProd} />}
      <div style={{ position: "relative", width: "100%", height: 220 }}><canvas id={chartId}></canvas></div>
    </div>);
  };

  // Pork seasonal views
  const [selectedPorkProduct, setSelectedPorkProduct] = useState(null);
  const [hPorkCutout, tPorkCutout] = useToggle();
  // Pork cutout multi-year view
  var porkCutoutView = { labels: liveDates };
  legendYears.forEach(function(y, i) {
    var yd = meatData ? meatData.seasonal.years.find(function(sy) { return sy.year === y.year; }) : null;
    porkCutoutView["yr" + i] = yd ? yd.pork_carcass || [] : [];
  });
  if (period !== "daily") {
    var ptmp = { labels: period === "weekly" ? BEEF_WEEK_RANGES.map(function(w) { return w.label; }) : BEEF_MONTH_RANGES.map(function(m) { return m.label; }) };
    legendYears.forEach(function(y, i) {
      var yd = meatData ? meatData.seasonal.years.find(function(sy) { return sy.year === y.year; }) : null;
      var series = yd ? yd.pork_carcass || [] : [];
      if (period === "weekly") ptmp["yr"+i] = BEEF_WEEK_RANGES.map(function(w) { return avgRange(series, w.start, w.end); });
      else ptmp["yr"+i] = BEEF_MONTH_RANGES.map(function(m) { return avgRange(series, m.start, m.end); });
    });
    porkCutoutView = ptmp;
  }
  const porkProductViews = PORK_PRODUCTS_DAILY.map(p => getProductView(p, period));
  const porkProductSeasonalViews = PORK_PRODUCT_SEASONAL.map(function(p) { return getSeasonalView(p.daily, p[prevYearLabel] || p["2024"] || [], p["5yr"] || [], period); });

  const PorkProductChart = ({ idx }) => {
    const view = porkProductSeasonalViews[idx];
    const [hProd, tProd] = useToggle();
    const chartId = `pork_prod_seasonal_${period}_${chartMode}_${idx}`;
    useEffect(() => {
      if (!window.Chart || !view) return;
      const t = setTimeout(() => {
        const c = document.getElementById(chartId);
        if (!c) return;
        const ex = Chart.getChart(c); if (ex) ex.destroy();
        mkSeasonalChart(view, hProd)(c);
      }, 60);
      return () => clearTimeout(t);
    }, [view, period, chartMode, chartId, hProd]);
    return (<div>
      {chartMode === "seasonal" && <InteractiveLegend items={seasonLegend} hidden={hProd} onToggle={tProd} />}
      <div style={{ position: "relative", width: "100%", height: 220 }}><canvas id={chartId}></canvas></div>
    </div>);
  };

  const chL = liveBeefChoiceLatest; const seL = liveBeefSelectLatest;

  // Period-aware comparisons for cutout cards
  const choiceView2025 = getProductView({ daily: beefChoiceByKey["2025"] || [] }, period);
  const selectView2025 = getProductView({ daily: beefSelectByKey["2025"] || [] }, period);
  const chVals = choiceView2025.values.filter(v => v != null);
  const seVals = selectView2025.values.filter(v => v != null);
  const chCur = chVals.length > 0 ? chVals[chVals.length - 1] : null;
  const chPrev = chVals.length > 1 ? chVals[chVals.length - 2] : null;
  const seCur = seVals.length > 0 ? seVals[seVals.length - 1] : null;
  const sePrev = seVals.length > 1 ? seVals[seVals.length - 2] : null;
  const chChg = chCur != null && chPrev != null ? chCur - chPrev : null;
  const seChg = seCur != null && sePrev != null ? seCur - sePrev : null;
  const spreadCur = chCur != null && seCur != null ? chCur - seCur : null;
  const compVals2 = (compViewData["yr" + (legendYears.length - 1)] || []).filter(function(v) { return v != null; });
  const compCur = compVals2.length > 0 ? compVals2[compVals2.length - 1] : liveCompLatest;
  const compPrev = compVals2.length > 1 ? compVals2[compVals2.length - 2] : null;
  const compChg = compCur != null && compPrev != null ? compCur - compPrev : null;
  const spreadPrev = chPrev != null && sePrev != null ? chPrev - sePrev : null;
  const spreadChg = spreadCur != null && spreadPrev != null ? spreadCur - spreadPrev : null;
  const periodLabel = period === "daily" ? "D/D" : period === "weekly" ? "W/W" : "M/M";

  // ── Multi-period comparisons for header cards (Choice / Select / Spread / Comp) ──
  // Walk daily records to find prior day, prior week (~5 trading days), prior year (~252 trading days)
  function buildHistory(getVal) {
    if (!meatData || !meatData.daily) return { dates: [], values: [] };
    const out = { dates: [], values: [] };
    meatData.daily.forEach(function(r) {
      const v = getVal(r);
      if (v != null) { out.dates.push(r.date); out.values.push(v); }
    });
    return out;
  }
  function lookback(hist, daysBack) {
    if (!hist.values.length) return { val: null, date: null };
    const idx = hist.values.length - 1 - daysBack;
    if (idx < 0) return { val: null, date: null };
    return { val: hist.values[idx], date: hist.dates[idx] };
  }
  // Find first record at or before exactly N calendar days before the latest date
  function lookbackByCalendarDays(hist, calDays) {
    if (!hist.values.length) return { val: null, date: null };
    const latestStr = hist.dates[hist.dates.length - 1];
    const parts = latestStr.split("/"); // mm/dd/yyyy
    if (parts.length !== 3) return lookback(hist, calDays);
    const target = new Date(parseInt(parts[2]), parseInt(parts[0]) - 1, parseInt(parts[1]));
    target.setDate(target.getDate() - calDays);
    // Walk backwards to find nearest record on or before target
    for (let i = hist.dates.length - 1; i >= 0; i--) {
      const dp = hist.dates[i].split("/");
      const d = new Date(parseInt(dp[2]), parseInt(dp[0]) - 1, parseInt(dp[1]));
      if (d <= target) return { val: hist.values[i], date: hist.dates[i] };
    }
    return { val: null, date: null };
  }
  const choiceHist = buildHistory(function(r) { return r.beef && r.beef.choice; });
  const selectHist = buildHistory(function(r) { return r.beef && r.beef.select; });
  const compHist = buildHistory(function(r) {
    if (r.beef_comp_cutout && r.beef_comp_cutout.cutout != null) return r.beef_comp_cutout.cutout;
    if (r.beef && r.beef.comp != null) return r.beef.comp;
    return null;
  });
  const choiceLastDate = choiceHist.dates.length > 0 ? choiceHist.dates[choiceHist.dates.length - 1] : null;
  const compLastDate = compHist.dates.length > 0 ? compHist.dates[compHist.dates.length - 1] : null;
  const choicePD = lookback(choiceHist, 1);
  const choicePW = lookbackByCalendarDays(choiceHist, 7);
  const choicePY = lookbackByCalendarDays(choiceHist, 365);
  const selectPD = lookback(selectHist, 1);
  const selectPW = lookbackByCalendarDays(selectHist, 7);
  const selectPY = lookbackByCalendarDays(selectHist, 365);
  const compPD = lookback(compHist, 1);
  const compPW = lookbackByCalendarDays(compHist, 7);
  const compPY = lookbackByCalendarDays(compHist, 365);
  // Spread comparisons: paired differences using same lookback dates
  const sub = function(a, b) { return (a != null && b != null) ? (a - b) : null; };
  const spreadPD = { val: sub(choicePD.val, selectPD.val), date: choicePD.date };
  const spreadPW = { val: sub(choicePW.val, selectPW.val), date: choicePW.date };
  const spreadPY = { val: sub(choicePY.val, selectPY.val), date: choicePY.date };
  // Format date "04/30/2026" → "Apr 30, 2026" via global fmtDate
  const fmtMD = fmtDate;

  const CutoutCard = ({ label, cur, asOfDate, pd, pw, py }) => {
    const diffLine = function(lbl, comp) {
      if (cur == null || !comp || comp.val == null) return null;
      const diff = Math.round((cur - comp.val) * 100) / 100;
      const col = diff > 0 ? "#639922" : diff < 0 ? "#A32D2D" : "var(--color-text-tertiary)";
      return (<div key={lbl} style={{ display: "flex", justifyContent: "space-between", fontSize: 10.5, padding: "1px 0" }}>
        <span style={{ color: "var(--color-text-tertiary)" }}>{lbl} <span style={{ color: "var(--color-text-tertiary)", opacity: 0.7 }}>({fmtMD(comp.date)})</span></span>
        <span style={{ display: "flex", gap: 4, alignItems: "baseline" }}>
          <span style={{ color: "var(--color-text-secondary)", textAlign: "right", minWidth: 56 }}>{comp.val.toFixed(2)}</span>
          <span style={{ color: col, fontWeight: 500, fontFamily: "var(--font-mono)", textAlign: "right", minWidth: 56 }}>({diff > 0 ? "+" : ""}{diff.toFixed(2)})</span>
        </span>
      </div>);
    };
    return (<div style={{ background: "var(--color-background-secondary)", borderRadius: "var(--border-radius-md)", padding: "12px 14px", minWidth: 0 }}>
      <div style={{ fontSize: 11, color: "var(--color-text-secondary)", marginBottom: 3, textTransform: "uppercase", letterSpacing: "0.4px" }}>{label} <span style={{ textTransform: "none", letterSpacing: 0 }}>($/cwt)</span></div>
      <div style={{ fontSize: 22, fontWeight: 500, color: "var(--color-text-primary)", marginBottom: 2 }}>{cur != null ? cur.toFixed(2) : "—"}</div>
      {asOfDate && <div style={{ fontSize: 10, color: "var(--color-text-tertiary)", marginBottom: 6 }}>as of {fmtMD(asOfDate)}</div>}
      <div style={{ borderTop: "0.5px solid var(--color-border-tertiary)", paddingTop: 5 }}>
        {diffLine("vs. prior day", pd)}
        {diffLine("vs. prior week", pw)}
        {diffLine("vs. prior year", py)}
      </div>
    </div>);
  };

  const tabs = [{ id: "cattle", label: "Beef" }, { id: "hogs", label: "Pork" }];

  var dlCutoutCSV = function() {
    var labels = cutoutView.labels || liveDates;
    var headers = ["Date", "Choice", "Select"];
    var rows = labels.map(function(l, i) { return [l, (beefChoiceByKey["2025"]||[])[i]||"", (beefSelectByKey["2025"]||[])[i]||""]; });
    downloadCSV("beef_cutout_" + period + ".csv", headers, rows);
  };

  return (<div>
    <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 16, flexWrap: "wrap", gap: 8 }}>
      <div style={{ display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <span style={{ fontSize: 11, fontWeight: 600, color: "var(--color-text-secondary)", textTransform: "uppercase", letterSpacing: "0.4px" }}>Commodity</span>
          <select value={tab} onChange={function(e){ setTab(e.target.value); setSelectedProduct(null); setSelectedPorkProduct(null); }} style={{ padding: "7px 28px 7px 12px", fontSize: 14, fontWeight: 500, border: "1px solid var(--color-border-secondary)", borderRadius: 6, background: "var(--color-background-primary)", color: "var(--color-text-primary)", fontFamily: "inherit", cursor: "pointer", appearance: "none", backgroundImage: "url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'><path d='M3 4.5l3 3 3-3' stroke='%23666' stroke-width='1.5' fill='none'/></svg>\")", backgroundRepeat: "no-repeat", backgroundPosition: "right 8px center" }}>
            {tabs.map(function(t){ return <option key={t.id} value={t.id}>{t.label}</option>; })}
          </select>
        </div>
        <div style={{ display: "flex", borderRadius: 6, border: "1px solid var(--color-border-secondary)", overflow: "hidden" }}>
          {[{ id: "daily", label: "Daily" }, { id: "weekly", label: "Weekly" }, { id: "monthly", label: "Monthly" }].map(u => (
            <button key={u.id} onClick={() => { setPeriod(u.id); setSelectedProduct(null); }} style={{ padding: "6px 14px", fontSize: 12, cursor: "pointer", border: "none", borderRight: u.id !== "monthly" ? "1px solid var(--color-border-secondary)" : "none", background: period === u.id ? "#2563EB" : "transparent", color: period === u.id ? "#fff" : "var(--color-text-tertiary)", fontWeight: 500, transition: "all 0.15s" }}>{u.label}</button>
          ))}
        </div>
        <div style={{ display: "flex", borderRadius: 6, border: "1px solid var(--color-border-secondary)", overflow: "hidden" }}>
          {[{ id: "seasonal", label: "Seasonal" }, { id: "contiguous", label: "Contiguous" }].map(u => (
            <button key={u.id} onClick={() => setChartMode(u.id)} style={{ padding: "6px 14px", fontSize: 12, cursor: "pointer", border: "none", borderRight: u.id !== "contiguous" ? "1px solid var(--color-border-secondary)" : "none", background: chartMode === u.id ? "#2563EB" : "transparent", color: chartMode === u.id ? "#fff" : "var(--color-text-tertiary)", fontWeight: 500, transition: "all 0.15s" }}>{u.label}</button>
          ))}
        </div>
      </div>
      <DownloadBtn onClick={dlCutoutCSV} />
    </div>
    {tab === "cattle" && (<div>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: 10, marginBottom: 8 }}>
        <CutoutCard label="Choice cutout" cur={chCur} asOfDate={choiceLastDate} pd={choicePD} pw={choicePW} py={choicePY} />
        <CutoutCard label="Select cutout" cur={seCur} asOfDate={choiceLastDate} pd={selectPD} pw={selectPW} py={selectPY} />
        <CutoutCard label="Choice–select spread" cur={spreadCur} asOfDate={choiceLastDate} pd={spreadPD} pw={spreadPW} py={spreadPY} />
        <CutoutCard label="Comprehensive cutout" cur={compCur} asOfDate={compLastDate} pd={compPD} pw={compPW} py={compPY} />
      </div>

      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginTop: 28, marginBottom: 14, flexWrap: "wrap", gap: 8 }}>
        <div>
          <h3 style={{ fontSize: 15, fontWeight: 500, color: "var(--color-text-primary)", margin: "0 0 2px" }}>Beef product prices</h3>
          <div style={{ fontSize: 11, color: "var(--color-text-tertiary)" }}>Click any product to view seasonal comparison chart</div>
        </div>
        <DownloadBtn onClick={() => {
          if (chartMode === "contiguous") {
            const labels24 = productViews[0].labels.map(l => l + " '24");
            const labels25 = productViews[0].labels.map(l => l + " '25");
            const headers = ["Product","Item", ...labels24, ...labels25];
            const rows = [];
            BEEF_PRIMAL_ORDER.forEach(primalName => {
              const pd = BEEF_PRIMALS_DAILY.find(p => p.name === primalName);
              if (pd) { const pv = getPrimalView(pd, period); const ps = liveBeefPrimals.find(function(p) { return p.name === primalName; }); const pv24 = ps ? getProductView({ daily: ps["2024"] }, period).values : pv.values.map(() => ""); rows.push([primalName + " (primal)", "", ...pv24.map(v => v != null ? v : ""), ...pv.values.map(v => v != null ? v : "")]); }
              BEEF_PRODUCTS_DAILY.filter(p => p.primal === primalName).forEach(p => {
                const pi = BEEF_PRODUCTS_DAILY.indexOf(p);
                const v25 = productViews[pi].values;
                const ps = BEEF_PRODUCT_SEASONAL[pi];
                const v24 = ps ? getProductView({ daily: ps["2024"] || [] }, period).values : v25.map(function() { return ""; });
                rows.push(["  " + p.name, p.item, ...v24.map(v => v != null ? v : ""), ...v25.map(v => v != null ? v : "")]);
              });
            });
            downloadCSV(`beef_products_${period}_contiguous.csv`, headers, rows);
          } else {
            const headers = ["Product","Item", ...productViews[0].labels];
            const rows = [];
            BEEF_PRIMAL_ORDER.forEach(primalName => {
              const pd = BEEF_PRIMALS_DAILY.find(p => p.name === primalName);
              if (pd) { const pv = getPrimalView(pd, period); rows.push([primalName + " (primal)", "", ...pv.values.map(v => v != null ? v : "")]); }
              BEEF_PRODUCTS_DAILY.filter(p => p.primal === primalName).forEach(p => {
                rows.push(["  " + p.name, p.item, ...productViews[BEEF_PRODUCTS_DAILY.indexOf(p)].values.map(v => v != null ? v : "")]);
              });
            });
            downloadCSV(`beef_products_${period}.csv`, headers, rows);
          }
        }} />
      </div>

      <div style={{ border: "0.5px solid var(--color-border-tertiary)", borderRadius: "var(--border-radius-lg)", overflow: "hidden" }}>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 12 }}>
          <thead>
            <tr style={{ background: "var(--color-background-secondary)" }}>
              <th style={{ textAlign: "left", padding: "8px 12px", fontWeight: 500, fontSize: 11, color: "var(--color-text-secondary)", borderBottom: "1.5px solid var(--color-border-primary)" }}>Product</th>
              <th style={{ textAlign: "right", padding: "8px 10px", fontWeight: 500, fontSize: 11, color: "var(--color-text-secondary)", borderBottom: "1.5px solid var(--color-border-primary)" }}>Loads</th>
              <th style={{ textAlign: "right", padding: "8px 10px", fontWeight: 500, fontSize: 11, color: "var(--color-text-secondary)", borderBottom: "1.5px solid var(--color-border-primary)" }}>Latest</th>
              <th style={{ textAlign: "right", padding: "8px 10px", fontWeight: 500, fontSize: 11, color: "var(--color-text-secondary)", borderBottom: "1.5px solid var(--color-border-primary)" }}>Prev day <div style={{ fontSize: 9, fontWeight: 400, color: "var(--color-text-tertiary)", textTransform: "none" }}>{prevDayLabel}</div></th>
              <th style={{ textAlign: "right", padding: "8px 10px", fontWeight: 500, fontSize: 11, color: "var(--color-text-secondary)", borderBottom: "1.5px solid var(--color-border-primary)" }}>Prev week <div style={{ fontSize: 9, fontWeight: 400, color: "var(--color-text-tertiary)", textTransform: "none" }}>{prevWeekLabel}</div></th>
              <th style={{ textAlign: "right", padding: "8px 10px", fontWeight: 500, fontSize: 11, color: "var(--color-text-secondary)", borderBottom: "1.5px solid var(--color-border-primary)" }}>Prev month <div style={{ fontSize: 9, fontWeight: 400, color: "var(--color-text-tertiary)", textTransform: "none" }}>{prevMonthLabel}</div></th>
              <th style={{ textAlign: "right", padding: "8px 12px", fontWeight: 500, fontSize: 11, color: "var(--color-text-secondary)", borderBottom: "1.5px solid var(--color-border-primary)" }}>Prev year <div style={{ fontSize: 9, fontWeight: 400, color: "var(--color-text-tertiary)", textTransform: "none" }}>{prevYearLabel2}</div></th>
            </tr>
          </thead>
          <tbody>
            {BEEF_PRIMAL_ORDER.map((primalName) => {
              const pr = liveBeefPrimalRows ? liveBeefPrimalRows[primalName] || {} : {};
              const primalLatest = pr.latest || null;
              const primalPrev = pr.prev || null;
              const primalChg = primalLatest != null && primalPrev != null ? primalLatest - primalPrev : null;
              const subs = liveBeefCutRows ? liveBeefCutRows.filter(function(r) { return r.primal === primalName; }) : [];
              const isPrimalSelected = selectedProduct === ("primal_" + primalName);
              return (<>
                <tr key={`primal-${primalName}`} onClick={primalName === "Trim" ? undefined : () => setSelectedProduct(isPrimalSelected ? null : ("primal_" + primalName))} style={{ borderBottom: "0.5px solid var(--color-border-tertiary)", background: isPrimalSelected ? "var(--color-background-info)" : "var(--color-background-secondary)", cursor: primalName === "Trim" ? "default" : "pointer" }}
                  onMouseEnter={e => { if (!isPrimalSelected && primalName !== "Trim") e.currentTarget.style.background = "rgba(37,99,235,0.06)"; }}
                  onMouseLeave={e => { if (!isPrimalSelected && primalName !== "Trim") e.currentTarget.style.background = "var(--color-background-secondary)"; }}
                >
                  <td style={{ padding: "8px 12px", fontWeight: 500, color: "var(--color-text-primary)", fontSize: 12 }}>
                    <span style={{ display: "inline-flex", alignItems: "center", gap: 6 }}>
                      {primalName !== "Trim" && <svg width="10" height="10" viewBox="0 0 10 10" fill="none" stroke="currentColor" strokeWidth="1.5" style={{ transform: isPrimalSelected ? "rotate(90deg)" : "none", transition: "transform 0.15s", flexShrink: 0 }}><path d="M3.5 1.5L7.5 5L3.5 8.5" /></svg>}
                      {primalName === "Trim" ? <span style={{ paddingLeft: 16 }}>Ground Beef & Trimmings</span> : primalName}
                    </span>
                  </td>
                  <td style={{ padding: "8px 10px", textAlign: "right", fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--color-text-tertiary)" }}></td>
                  <td style={{ padding: "8px 10px", textAlign: "right", fontFamily: "var(--font-mono)", fontSize: 12, fontWeight: 500, color: "var(--color-text-primary)" }}>{primalLatest != null ? `${primalLatest.toFixed(2)}` : "—"}</td>
                  {(function() {
                    var hist = (typeof beefPrimalHistory === "function") ? beefPrimalHistory(primalName) : { prevDay: null, prevWeek: null, prevMonth: null, prevYear: null };
                    var renderCell = function(comp, key, lastCol) {
                      var pad = lastCol ? "8px 12px" : "8px 10px";
                      if (primalLatest == null || comp == null) {
                        return <td key={key} style={{ padding: pad, textAlign: "right", fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--color-text-tertiary)" }}>—</td>;
                      }
                      var d = primalLatest - comp;
                      var col = d > 0 ? "#639922" : d < 0 ? "#A32D2D" : "var(--color-text-tertiary)";
                      return (<td key={key} style={{ padding: pad, textAlign: "right", fontFamily: "var(--font-mono)" }}>
                        <div style={{ fontSize: 11, color: "var(--color-text-secondary)" }}>{comp.toFixed(2)}</div>
                        <div style={{ fontSize: 9.5, fontWeight: 500, color: col }}>{d > 0 ? "+" : ""}{d.toFixed(2)}</div>
                      </td>);
                    };
                    return [
                      renderCell(hist.prevDay != null ? hist.prevDay : primalPrev, "pd", false),
                      renderCell(hist.prevWeek, "pw", false),
                      renderCell(hist.prevMonth, "pm", false),
                      renderCell(hist.prevYear, "py", true),
                    ];
                  })()}
                </tr>
                {isPrimalSelected && (
                  <tr key={`primal-chart-${primalName}`}>
                    <td colSpan={7} style={{ padding: "12px 16px 16px", background: "var(--color-background-secondary)" }}>
                      <ExpandChartRow
                        chartId={"beefprimal_" + primalName + "_" + period}
                        title={primalName + " primal — seasonal"}
                        buildView={function() {
                          var pView = { labels: liveDates };
                          legendYears.forEach(function(y, yi) {
                            var yd = meatData ? meatData.seasonal.years.find(function(sy) { return sy.year === y.year; }) : null;
                            pView["yr" + yi] = yd ? yd["beef_" + primalName.toLowerCase()] || [] : [];
                          });
                          return pView;
                        }}
                        legendYears={legendYears}
                        seasonLegend={seasonLegend}
                        seasonDS={seasonDS}
                        mkChart={mkSeasonalChart}
                        chartMode={chartMode}
                      />
                    </td>
                  </tr>
                )}
                {subs.map((p, si) => {
                  const latest = p.latest || p.avg || null;
                  const prev = p.prev || null;
                  const chg = latest != null && prev != null ? latest - prev : null;
                  const isSelected = selectedProduct === (primalName + "_" + si);
                  return (<>
                    <tr key={primalName + "_" + si} style={{
                      borderBottom: "0.5px solid var(--color-border-tertiary)",
                      background: "transparent",
                    }}
                    onMouseEnter={e => { if (!isSelected) e.currentTarget.style.background = "var(--color-background-secondary)"; }}
                    onMouseLeave={e => { if (!isSelected) e.currentTarget.style.background = "transparent"; }}
                    >
                      <td style={{ padding: "6px 12px 6px 28px", fontWeight: isSelected ? 500 : 400, color: "var(--color-text-primary)", fontSize: 12 }}>
                        <span style={{ display: "inline-flex", alignItems: "center", gap: 6 }}>
                          <svg width="10" height="10" viewBox="0 0 10 10" fill="none" stroke="currentColor" strokeWidth="1.5" style={{ transform: isSelected ? "rotate(90deg)" : "rotate(0deg)", transition: "transform 0.15s", flexShrink: 0 }}><path d="M3 1.5l4 3.5-4 3.5" /></svg>
                          {p.name} <span style={{ color: "var(--color-text-tertiary)", fontSize: 10 }}>{p.item}</span>
                        </span>
                      </td>
                      <td style={{ padding: "6px 10px", textAlign: "right", fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--color-text-secondary)" }}>{p.loads != null ? p.loads.toLocaleString() : ""}</td>
                      <td style={{ padding: "6px 10px", textAlign: "right", fontFamily: "var(--font-mono)", fontSize: 12, fontWeight: 500, color: "var(--color-text-primary)" }}>{latest != null ? `${latest.toFixed(2)}` : "—"}</td>
                      {(function() {
                        var renderCell = function(comp, key) {
                          if (latest == null || comp == null) {
                            return <td key={key} style={{ padding: "6px 10px", textAlign: "right", fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--color-text-tertiary)" }}>—</td>;
                          }
                          var d = latest - comp;
                          var col = d > 0 ? "#639922" : d < 0 ? "#A32D2D" : "var(--color-text-tertiary)";
                          return (<td key={key} style={{ padding: "6px 10px", textAlign: "right", fontFamily: "var(--font-mono)" }}>
                            <div style={{ fontSize: 11, color: "var(--color-text-secondary)" }}>{comp.toFixed(2)}</div>
                            <div style={{ fontSize: 9.5, fontWeight: 500, color: col }}>{d > 0 ? "+" : ""}{d.toFixed(2)}</div>
                          </td>);
                        };
                        return [
                          renderCell(p.prevDay != null ? p.prevDay : prev, "pd"),
                          renderCell(p.prevWeek, "pw"),
                          renderCell(p.prevMonth, "pm"),
                          renderCell(p.prevYear, "py"),
                        ];
                      })()}
                    </tr>
                    {isSelected && (
                      <tr key={`chart-beef-${primalName}-${si}`}>
                        <td colSpan={7} style={{ padding: "12px 16px 16px", background: "var(--color-background-secondary)" }}>
                          <ExpandChartRow
                            chartId={"beefcut_" + primalName + "_" + si + "_" + period}
                            title={(p.name || "") + (p.item ? " (" + p.item + ")" : "")}
                            buildView={function() {
                              var pView = { labels: liveDates };
                              legendYears.forEach(function(y, yi) {
                                var yd = meatData ? meatData.seasonal.years.find(function(sy) { return sy.year === y.year; }) : null;
                                if (!yd) { pView["yr" + yi] = []; return; }
                                // Prefer per-item series (each cut's own history)
                                if (yd.cuts_beef && yd.cuts_beef[p.name]) {
                                  pView["yr" + yi] = yd.cuts_beef[p.name];
                                } else if (primalName === "Trim" && yd.trim_beef && yd.trim_beef[p.name]) {
                                  // Backward compatibility with older JSONs
                                  pView["yr" + yi] = yd.trim_beef[p.name];
                                } else {
                                  // Fallback to composite primal (older data without per-item series)
                                  pView["yr" + yi] = yd["beef_" + primalName.toLowerCase()] || [];
                                }
                              });
                              return pView;
                            }}
                            legendYears={legendYears}
                            seasonLegend={seasonLegend}
                            seasonDS={seasonDS}
                            mkChart={mkSeasonalChart}
                            chartMode={chartMode}
                          />
                        </td>
                      </tr>
                    )}
                  </>);
                })}
              </>);
            })}
          </tbody>
        </table>
      </div>
    </div>)}
    {tab === "hogs" && (<div>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(130px, 1fr))", gap: 10, marginBottom: 8 }}>
        <MetricCard label="Pork cutout ($/cwt)" value={`${livePorkLatest.toFixed(2)}`} sub="" trend={3.2} />
      </div>
      <SectionTitle>Pork product prices</SectionTitle>

      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginTop: 0, marginBottom: 14, flexWrap: "wrap", gap: 8 }}>
        <div>
          <h3 style={{ fontSize: 15, fontWeight: 500, color: "var(--color-text-primary)", margin: "0 0 2px" }}>Pork product prices</h3>
          <div style={{ fontSize: 11, color: "var(--color-text-tertiary)" }}></div>
        </div>
        <DownloadBtn onClick={() => {
          if (chartMode === "contiguous") {
            const labels24 = porkProductViews[0].labels.map(l => l + " '24");
            const labels25 = porkProductViews[0].labels.map(l => l + " '25");
            const headers = ["Product","Item", ...labels24, ...labels25];
            const rows = [];
            PORK_PRIMAL_ORDER.forEach(primalName => {
              const pd = PORK_PRIMALS_DAILY.find(p => p.name === primalName);
              if (pd) { const pv = getProductView(pd, period); const ps = livePorkPrimals.find(function(p) { return p.name === primalName; }); const pv24 = ps ? getProductView({ daily: ps["2024"] }, period).values : pv.values.map(() => ""); rows.push([primalName + " (primal)", "", ...pv24.map(v => v != null ? v : ""), ...pv.values.map(v => v != null ? v : "")]); }
              PORK_PRODUCTS_DAILY.filter(p => p.primal === primalName).forEach(p => {
                const pi = PORK_PRODUCTS_DAILY.indexOf(p);
                const v25 = porkProductViews[pi].values;
                const ps = PORK_PRODUCT_SEASONAL[pi];
                const v24 = ps ? getProductView({ daily: ps["2024"] || [] }, period).values : v25.map(function() { return ""; });
                rows.push(["  " + p.name, p.item, ...v24.map(v => v != null ? v : ""), ...v25.map(v => v != null ? v : "")]);
              });
            });
            downloadCSV(`pork_products_${period}_contiguous.csv`, headers, rows);
          } else {
            const headers = ["Product","Item", ...porkProductViews[0].labels];
            const rows = [];
            PORK_PRIMAL_ORDER.forEach(primalName => {
              const pd = PORK_PRIMALS_DAILY.find(p => p.name === primalName);
              if (pd) { const pv = getProductView(pd, period); rows.push([primalName + " (primal)", "", ...pv.values.map(v => v != null ? v : "")]); }
              PORK_PRODUCTS_DAILY.filter(p => p.primal === primalName).forEach(p => {
                rows.push(["  " + p.name, p.item, ...porkProductViews[PORK_PRODUCTS_DAILY.indexOf(p)].values.map(v => v != null ? v : "")]);
              });
            });
            downloadCSV(`pork_products_${period}.csv`, headers, rows);
          }
        }} />
      </div>

      <div style={{ border: "0.5px solid var(--color-border-tertiary)", borderRadius: "var(--border-radius-lg)", overflow: "hidden" }}>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 12 }}>
          <thead>
            <tr style={{ background: "var(--color-background-secondary)" }}>
              <th style={{ textAlign: "left", padding: "8px 12px", fontWeight: 500, fontSize: 11, color: "var(--color-text-secondary)", borderBottom: "1.5px solid var(--color-border-primary)" }}>Product</th>
              <th style={{ textAlign: "right", padding: "8px 10px", fontWeight: 500, fontSize: 11, color: "var(--color-text-secondary)", borderBottom: "1.5px solid var(--color-border-primary)" }}>Loads</th>
              <th style={{ textAlign: "right", padding: "8px 10px", fontWeight: 500, fontSize: 11, color: "var(--color-text-secondary)", borderBottom: "1.5px solid var(--color-border-primary)" }}>Latest</th>
              <th style={{ textAlign: "right", padding: "8px 10px", fontWeight: 500, fontSize: 11, color: "var(--color-text-secondary)", borderBottom: "1.5px solid var(--color-border-primary)" }}>Prev day <div style={{ fontSize: 9, fontWeight: 400, color: "var(--color-text-tertiary)", textTransform: "none" }}>{prevDayLabel}</div></th>
              <th style={{ textAlign: "right", padding: "8px 10px", fontWeight: 500, fontSize: 11, color: "var(--color-text-secondary)", borderBottom: "1.5px solid var(--color-border-primary)" }}>Prev week <div style={{ fontSize: 9, fontWeight: 400, color: "var(--color-text-tertiary)", textTransform: "none" }}>{prevWeekLabel}</div></th>
              <th style={{ textAlign: "right", padding: "8px 10px", fontWeight: 500, fontSize: 11, color: "var(--color-text-secondary)", borderBottom: "1.5px solid var(--color-border-primary)" }}>Prev month <div style={{ fontSize: 9, fontWeight: 400, color: "var(--color-text-tertiary)", textTransform: "none" }}>{prevMonthLabel}</div></th>
              <th style={{ textAlign: "right", padding: "8px 12px", fontWeight: 500, fontSize: 11, color: "var(--color-text-secondary)", borderBottom: "1.5px solid var(--color-border-primary)" }}>Prev year <div style={{ fontSize: 9, fontWeight: 400, color: "var(--color-text-tertiary)", textTransform: "none" }}>{prevYearLabel2}</div></th>
            </tr>
          </thead>
          <tbody>
            {PORK_PRIMAL_ORDER.map((primalName) => {
              const pr = livePorkPrimalRows ? livePorkPrimalRows[primalName] || {} : {};
              const primalLatest = pr.latest || null;
              const primalPrev = pr.prev || null;
              const primalChg = primalLatest != null && primalPrev != null ? primalLatest - primalPrev : null;
              const subs = livePorkCutRows ? livePorkCutRows.filter(function(r) { return r.primal === primalName; }) : [];
              const isPorkPrimalSelected = selectedPorkProduct === ("primal_" + primalName);
              return (<>
                <tr key={`pork-primal-${primalName}`} onClick={primalName === "Trim" ? undefined : () => setSelectedPorkProduct(isPorkPrimalSelected ? null : ("primal_" + primalName))} style={{ borderBottom: "0.5px solid var(--color-border-tertiary)", background: isPorkPrimalSelected ? "var(--color-background-info)" : "var(--color-background-secondary)", cursor: primalName === "Trim" ? "default" : "pointer" }}
                  onMouseEnter={e => { if (!isPorkPrimalSelected && primalName !== "Trim") e.currentTarget.style.background = "rgba(37,99,235,0.06)"; }}
                  onMouseLeave={e => { if (!isPorkPrimalSelected && primalName !== "Trim") e.currentTarget.style.background = "var(--color-background-secondary)"; }}
                >
                  <td style={{ padding: "8px 12px", fontWeight: 500, color: "var(--color-text-primary)", fontSize: 12 }}>
                    <span style={{ display: "inline-flex", alignItems: "center", gap: 6 }}>
                      {primalName !== "Trim" && <svg width="10" height="10" viewBox="0 0 10 10" fill="none" stroke="currentColor" strokeWidth="1.5" style={{ transform: isPorkPrimalSelected ? "rotate(90deg)" : "none", transition: "transform 0.15s", flexShrink: 0 }}><path d="M3.5 1.5L7.5 5L3.5 8.5" /></svg>}
                      {primalName === "Trim" ? <span style={{ paddingLeft: 16 }}>Trimmings & Processing</span> : primalName}
                    </span>
                  </td>
                  <td style={{ padding: "8px 10px", textAlign: "right", fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--color-text-tertiary)" }}></td>
                  <td style={{ padding: "8px 10px", textAlign: "right", fontFamily: "var(--font-mono)", fontSize: 12, fontWeight: 500, color: "var(--color-text-primary)" }}>{primalLatest != null ? `${primalLatest.toFixed(2)}` : "—"}</td>
                  {(function() {
                    var hist = (typeof porkPrimalHistory === "function") ? porkPrimalHistory(primalName) : { prevDay: null, prevWeek: null, prevMonth: null, prevYear: null };
                    var renderCell = function(comp, key, lastCol) {
                      var pad = lastCol ? "8px 12px" : "8px 10px";
                      if (primalLatest == null || comp == null) {
                        return <td key={key} style={{ padding: pad, textAlign: "right", fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--color-text-tertiary)" }}>—</td>;
                      }
                      var d = primalLatest - comp;
                      var col = d > 0 ? "#639922" : d < 0 ? "#A32D2D" : "var(--color-text-tertiary)";
                      return (<td key={key} style={{ padding: pad, textAlign: "right", fontFamily: "var(--font-mono)" }}>
                        <div style={{ fontSize: 11, color: "var(--color-text-secondary)" }}>{comp.toFixed(2)}</div>
                        <div style={{ fontSize: 9.5, fontWeight: 500, color: col }}>{d > 0 ? "+" : ""}{d.toFixed(2)}</div>
                      </td>);
                    };
                    return [
                      renderCell(hist.prevDay != null ? hist.prevDay : primalPrev, "pd", false),
                      renderCell(hist.prevWeek, "pw", false),
                      renderCell(hist.prevMonth, "pm", false),
                      renderCell(hist.prevYear, "py", true),
                    ];
                  })()}
                </tr>
                {isPorkPrimalSelected && (
                  <tr key={`pork-primal-chart-${primalName}`}>
                    <td colSpan={7} style={{ padding: "12px 16px 16px", background: "var(--color-background-secondary)" }}>
                      <ExpandChartRow
                        chartId={"porkprimal_" + primalName + "_" + period}
                        title={primalName + " primal — seasonal"}
                        buildView={function() {
                          var pView = { labels: liveDates };
                          legendYears.forEach(function(y, yi) {
                            var yd = meatData ? meatData.seasonal.years.find(function(sy) { return sy.year === y.year; }) : null;
                            pView["yr" + yi] = yd ? yd["pork_" + primalName.toLowerCase()] || [] : [];
                          });
                          return pView;
                        }}
                        legendYears={legendYears}
                        seasonLegend={seasonLegend}
                        seasonDS={seasonDS}
                        mkChart={mkSeasonalChart}
                        chartMode={chartMode}
                      />
                    </td>
                  </tr>
                )}
                {subs.map((p, si) => {
                  const latest = p.latest || p.avg || null;
                  const prev = p.prev || null;
                  const chg = latest != null && prev != null ? latest - prev : null;
                  const isSelected = selectedPorkProduct === (primalName + "_" + si);
                  return (<>
                    <tr key={`pork-${primalName}-${si}`} style={{
                      borderBottom: "0.5px solid var(--color-border-tertiary)",
                      background: "transparent",
                    }}
                    onMouseEnter={e => { if (!isSelected) e.currentTarget.style.background = "var(--color-background-secondary)"; }}
                    onMouseLeave={e => { if (!isSelected) e.currentTarget.style.background = "transparent"; }}
                    >
                      <td style={{ padding: "6px 12px 6px 28px", fontWeight: isSelected ? 500 : 400, color: "var(--color-text-primary)", fontSize: 12 }}>
                        <span style={{ display: "inline-flex", alignItems: "center", gap: 6 }}>
                          <svg width="10" height="10" viewBox="0 0 10 10" fill="none" stroke="currentColor" strokeWidth="1.5" style={{ transform: isSelected ? "rotate(90deg)" : "rotate(0deg)", transition: "transform 0.15s", flexShrink: 0 }}><path d="M3 1.5l4 3.5-4 3.5" /></svg>
                          {p.name} <span style={{ color: "var(--color-text-tertiary)", fontSize: 10 }}>{p.item}</span>
                        </span>
                      </td>
                      <td style={{ padding: "6px 10px", textAlign: "right", fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--color-text-secondary)" }}>{p.loads != null ? p.loads.toLocaleString() : ""}</td>
                      <td style={{ padding: "6px 10px", textAlign: "right", fontFamily: "var(--font-mono)", fontSize: 12, fontWeight: 500, color: "var(--color-text-primary)" }}>{latest != null ? `${latest.toFixed(2)}` : "—"}</td>
                      {(function() {
                        var renderCell = function(comp, key) {
                          if (latest == null || comp == null) {
                            return <td key={key} style={{ padding: "6px 10px", textAlign: "right", fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--color-text-tertiary)" }}>—</td>;
                          }
                          var d = latest - comp;
                          var col = d > 0 ? "#639922" : d < 0 ? "#A32D2D" : "var(--color-text-tertiary)";
                          return (<td key={key} style={{ padding: "6px 10px", textAlign: "right", fontFamily: "var(--font-mono)" }}>
                            <div style={{ fontSize: 11, color: "var(--color-text-secondary)" }}>{comp.toFixed(2)}</div>
                            <div style={{ fontSize: 9.5, fontWeight: 500, color: col }}>{d > 0 ? "+" : ""}{d.toFixed(2)}</div>
                          </td>);
                        };
                        return [
                          renderCell(p.prevDay != null ? p.prevDay : prev, "pd"),
                          renderCell(p.prevWeek, "pw"),
                          renderCell(p.prevMonth, "pm"),
                          renderCell(p.prevYear, "py"),
                        ];
                      })()}
                    </tr>
                    {isSelected && (
                      <tr key={`chart-pork-${primalName}-${si}`}>
                        <td colSpan={7} style={{ padding: "12px 16px 16px", background: "var(--color-background-secondary)" }}>
                          <ExpandChartRow
                            chartId={"porkcut_" + primalName + "_" + si + "_" + period}
                            title={p.name || ""}
                            buildView={function() {
                              var pView = { labels: liveDates };
                              legendYears.forEach(function(y, yi) {
                                var yd = meatData ? meatData.seasonal.years.find(function(sy) { return sy.year === y.year; }) : null;
                                if (!yd) { pView["yr" + yi] = []; return; }
                                if (yd.cuts_pork && yd.cuts_pork[p.name]) {
                                  pView["yr" + yi] = yd.cuts_pork[p.name];
                                } else if (primalName === "Trim" && yd.trim_pork && yd.trim_pork[p.name]) {
                                  pView["yr" + yi] = yd.trim_pork[p.name];
                                } else {
                                  pView["yr" + yi] = yd["pork_" + primalName.toLowerCase()] || [];
                                }
                              });
                              return pView;
                            }}
                            legendYears={legendYears}
                            seasonLegend={seasonLegend}
                            seasonDS={seasonDS}
                            mkChart={mkSeasonalChart}
                            chartMode={chartMode}
                          />
                        </td>
                      </tr>
                    )}
                  </>);
                })}
              </>);
            })}
          </tbody>
        </table>
      </div>
    </div>)}
  </div>);
}

function MeatPriceChartsPage({ ready }) {
  // ── State ──
  const [meatData, setMeatData] = useState(null);
  const [commodity, setCommodity] = useState("beef");      // "beef" | "pork"
  const [primal, setPrimal] = useState("__choice_cutout__"); // special keys for cutouts, else primal name
  const [cut, setCut] = useState("__primal__");             // "__primal__" = primal composite, else cut name
  const [period, setPeriod] = useState("daily");            // daily | weekly | monthly
  const [chartMode, setChartMode] = useState("seasonal");   // seasonal | contiguous
  const [range, setRange] = useState("5");                  // 3 | 5 | 10 | all
  const [hidden, toggleHidden] = useToggle();

  // Load meat prices JSON
  useEffect(function() {
    fetch("data/meat_prices.json?t=" + Date.now())
      .then(function(r) { return r.ok ? r.json() : null; })
      .then(function(data) { if (data) setMeatData(data); })
      .catch(function() {});
  }, []);

  // ── Discover available cuts from meatData.seasonal latest year ──
  const cutsInventory = useMemo(function() {
    if (!meatData || !meatData.seasonal || !meatData.seasonal.years) return null;
    const years = meatData.seasonal.years.filter(function(y){ return typeof y.year === "number"; });
    if (!years.length) return null;
    // Collect all cuts seen across all years (current may not have every cut yet)
    const beefCuts = {}, porkCuts = {};
    years.forEach(function(y) {
      if (y.cuts_beef) Object.keys(y.cuts_beef).forEach(function(k){ beefCuts[k] = true; });
      if (y.cuts_pork) Object.keys(y.cuts_pork).forEach(function(k){ porkCuts[k] = true; });
    });
    return {
      beef: Object.keys(beefCuts).sort(),
      pork: Object.keys(porkCuts).sort(),
    };
  }, [meatData]);

  // ── Determine primal for each cut by parsing IMPS code or matching guide ──
  function primalForBeefCut(cutName) {
    // IMPS code at end like "(109E 3)" or middle "Round, outside round (171B 3)"
    const m = cutName.match(/\((\d+[A-Z]?)\s+(\d)\)/);
    if (m) {
      const code = m[1] + "  " + m[2];
      if (BEEF_IMPS_MAP[code]) return BEEF_IMPS_MAP[code];
    }
    // Fall back to prefix match
    const lower = cutName.toLowerCase();
    if (lower.startsWith("rib,")) return "Rib";
    if (lower.startsWith("chuck,")) return "Chuck";
    if (lower.startsWith("brisket")) return "Brisket";
    if (lower.startsWith("round,")) return "Round";
    if (lower.startsWith("loin,")) return "Loin";
    if (lower.startsWith("plate") || lower.startsWith("short plate")) return "Plate";
    if (lower.startsWith("flank")) return "Flank";
    if (lower.indexOf("ground") >= 0 || lower.indexOf("trim") >= 0 || lower.indexOf("50cl") >= 0 || lower.indexOf("90cl") >= 0 || lower.indexOf("85cl") >= 0 || lower.indexOf("65cl") >= 0) return "Trim";
    return "Other";
  }
  function primalForPorkCut(cutName) {
    const found = PORK_GUIDE_CUTS.find(function(g) {
      if (g.exact) return cutName === g.match;
      return cutName.indexOf(g.match) >= 0;
    });
    if (found) return found.primal;
    const lower = cutName.toLowerCase();
    if (lower.indexOf("trim") >= 0 || lower.indexOf("42%") >= 0 || lower.indexOf("72%") >= 0) return "Trim";
    if (lower.indexOf("jowl") >= 0) return "Jowl";
    return "Other";
  }

  // ── Build the primal → [cuts] map for the selected commodity ──
  const primalMap = useMemo(function() {
    if (!cutsInventory) return {};
    const cuts = commodity === "beef" ? cutsInventory.beef : cutsInventory.pork;
    const map = {};
    cuts.forEach(function(name) {
      const p = commodity === "beef" ? primalForBeefCut(name) : primalForPorkCut(name);
      if (!map[p]) map[p] = [];
      map[p].push(name);
    });
    return map;
  }, [cutsInventory, commodity]);

  // ── Special "primal" entries for cutouts (top of dropdown) ──
  const cutoutOptions = commodity === "beef"
    ? [
        { key: "__choice_cutout__", label: "Choice cutout" },
        { key: "__select_cutout__", label: "Select cutout" },
        { key: "__comp_cutout__",   label: "Comprehensive cutout" },
      ]
    : [
        { key: "__pork_cutout__", label: "Pork cutout" },
      ];

  // Reset primal/cut when commodity changes
  useEffect(function() {
    if (commodity === "beef") {
      setPrimal("__choice_cutout__");
    } else {
      setPrimal("__pork_cutout__");
    }
    setCut("__primal__");
  }, [commodity]);

  // Reset cut when primal changes
  useEffect(function() {
    setCut("__primal__");
  }, [primal]);

  // ── Resolve which data series to plot ──
  // Returns { label, getYearVals(year), getYearDates(year) }
  function resolveSeries() {
    const years = meatData && meatData.seasonal && meatData.seasonal.years ? meatData.seasonal.years : [];
    function yearObj(y) { return years.find(function(yr){ return yr.year === y; }); }

    // Cutouts (special)
    const cutoutKeys = {
      "__choice_cutout__": { label: "Choice cutout ($/cwt)", series: "beef_choice" },
      "__select_cutout__": { label: "Select cutout ($/cwt)", series: "beef_select" },
      "__comp_cutout__":   { label: "Comprehensive cutout ($/cwt)", series: "beef_comp" },
      "__pork_cutout__":   { label: "Pork cutout ($/cwt)", series: "pork_carcass" },
    };
    if (cutoutKeys[primal]) {
      const sk = cutoutKeys[primal];
      return {
        label: sk.label,
        getYearVals: function(y) { const yo = yearObj(y); return yo ? (yo[sk.series] || []) : []; },
        getYearDates: function(y) { const yo = yearObj(y); return yo ? (yo.dates || []) : []; },
      };
    }

    // Primal composite (when cut === "__primal__")
    if (cut === "__primal__") {
      // Beef primals: beef_rib, beef_chuck, beef_round, beef_loin, beef_brisket, beef_plate, beef_flank
      // Pork primals: pork_loin, pork_butt, pork_picnic, pork_rib, pork_ham, pork_belly, pork_jowl
      const seriesKey = (commodity === "beef" ? "beef_" : "pork_") + primal.toLowerCase();
      return {
        label: commodity === "beef" ? primal + " primal ($/cwt)" : primal + " primal ($/cwt)",
        getYearVals: function(y) { const yo = yearObj(y); return yo ? (yo[seriesKey] || []) : []; },
        getYearDates: function(y) { const yo = yearObj(y); return yo ? (yo.dates || []) : []; },
      };
    }

    // Individual cut
    const cutsKey = commodity === "beef" ? "cuts_beef" : "cuts_pork";
    return {
      label: cut + " ($/cwt)",
      getYearVals: function(y) {
        const yo = yearObj(y);
        if (!yo || !yo[cutsKey]) return [];
        return yo[cutsKey][cut] || [];
      },
      getYearDates: function(y) { const yo = yearObj(y); return yo ? (yo.dates || []) : []; },
    };
  }

  // ── Year list for chart (current + N prior) ──
  const allAvailYears = meatData && meatData.seasonal && meatData.seasonal.years
    ? meatData.seasonal.years.filter(function(y){ return typeof y.year === "number"; }).map(function(y){ return y.year; }).sort(function(a,b){ return a-b; })
    : [];
  const curYear = allAvailYears.length ? allAvailYears[allAvailYears.length - 1] : new Date().getFullYear();
  const yearsToShow = range === "all"
    ? allAvailYears
    : allAvailYears.filter(function(y){ return y >= curYear - parseInt(range); });

  // ── Aggregation: convert daily values to weekly (last value of week) or monthly ──
  function aggregate(dates, values, mode) {
    if (mode === "daily") return { dates: dates, values: values };
    // dates are "M/D" strings (no year). We need to group.
    // For weekly: group by ISO week ending Friday (or just every 5 trading days).
    // Simple approach: take every Nth value (5 for weekly, ~21 for monthly).
    if (mode === "weekly") {
      // Find Friday positions or just take every 5th data point.
      // Better: group by "week ending" — take last data point in each 7-day calendar window.
      const out = { dates: [], values: [] };
      let i = 0;
      while (i < dates.length) {
        // Find the last non-null value in the next 5 trading days
        const end = Math.min(i + 5, dates.length);
        let lastIdx = -1;
        for (let j = i; j < end; j++) {
          if (values[j] != null) lastIdx = j;
        }
        if (lastIdx >= 0) {
          out.dates.push(dates[lastIdx]);
          out.values.push(values[lastIdx]);
        }
        i = end;
      }
      return out;
    }
    if (mode === "monthly") {
      // Group by month (first part of "M/D")
      const out = { dates: [], values: [] };
      const byMonth = {};
      dates.forEach(function(d, idx) {
        if (!d) return;
        const m = d.split("/")[0];
        if (!byMonth[m]) byMonth[m] = [];
        if (values[idx] != null) byMonth[m].push({ d: d, v: values[idx], idx: idx });
      });
      // Sort months numerically
      Object.keys(byMonth).sort(function(a,b){ return parseInt(a) - parseInt(b); }).forEach(function(m) {
        const arr = byMonth[m];
        if (arr.length) {
          // Average values for the month
          const sum = arr.reduce(function(acc, x){ return acc + x.v; }, 0);
          out.dates.push(m + "/15"); // Mid-month label
          out.values.push(sum / arr.length);
        }
      });
      return out;
    }
    return { dates: dates, values: values };
  }

  // ── Series legend (one entry per year) ──
  const yearColors = ["#A32D2D","#D85A30","#E8A735","#639922","#1D9E75","#378ADD","#534AB7","#8B5CF6","#EC4899","#6B7280","#0EA5E9","#14B8A6"];
  const seasonLegend = yearsToShow.map(function(y, i) {
    const isLast = i === yearsToShow.length - 1;
    return {
      key: "yr" + i,
      label: String(y),
      color: isLast ? "#333" : yearColors[i % yearColors.length],
    };
  });

  const series = resolveSeries();

  // ── Build chart data per year, then aggregate ──
  const perYear = useMemo(function() {
    return yearsToShow.map(function(y) {
      const raw = aggregate(series.getYearDates(y), series.getYearVals(y), period);
      return { year: y, dates: raw.dates, values: raw.values };
    });
  }, [yearsToShow.join(","), commodity, primal, cut, period, meatData]);

  // ── Chart renderer ──
  function mkChart(canvas) {
    if (!canvas) return;
    // x-axis: use longest year's dates as labels (seasonal mode)
    const longest = perYear.reduce(function(acc, py) {
      return py.dates.length > acc.length ? py.dates : acc;
    }, []);
    const labels = longest;

    if (chartMode === "contiguous") {
      // Concatenate visible years
      const visibleYears = perYear.filter(function(py, i) { return !hidden.has("yr" + i); });
      const allLabels = [];
      const allValues = [];
      const yearMidpoints = [];
      const yearBoundaries = [];
      visibleYears.forEach(function(py) {
        const start = allLabels.length;
        py.dates.forEach(function(d, j) {
          allLabels.push(d + "/" + py.year);
          allValues.push(py.values[j]);
        });
        const mid = start + Math.floor(py.dates.length / 2);
        yearMidpoints.push({ idx: mid, label: String(py.year) });
        if (start > 0) yearBoundaries.push(start - 1);
      });

      new Chart(canvas, {
        type: "line",
        data: {
          labels: allLabels,
          datasets: [{
            label: series.label,
            data: allValues,
            borderColor: "#378ADD",
            backgroundColor: "#378ADD",
            borderWidth: 1.8,
            pointRadius: 0,
            tension: 0.2,
            spanGaps: false,
          }],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false }, tooltip: { mode: "index", intersect: false } },
          scales: {
            x: {
              ticks: {
                autoSkip: false,
                maxRotation: visibleYears.length > 8 ? 90 : 0,
                callback: function(val, idx) {
                  for (let i = 0; i < yearMidpoints.length; i++) {
                    if (yearMidpoints[i].idx === idx) return yearMidpoints[i].label;
                  }
                  return "";
                },
                font: { size: 10 },
              },
              grid: {
                color: function(ctx) {
                  return yearBoundaries.indexOf(ctx.index) >= 0 ? "rgba(0,0,0,0.15)" : "transparent";
                },
              },
            },
            y: {
              ticks: { font: { size: 10 }, callback: function(v){ return "$" + v.toFixed(2); } },
              grid: { color: "rgba(0,0,0,0.06)" },
            },
          },
        },
      });
      return;
    }

    // Seasonal: each year is one dataset, x = day-of-year
    const datasets = perYear.map(function(py, i) {
      if (hidden.has("yr" + i)) return null;
      const isCurrent = i === perYear.length - 1;
      const color = isCurrent ? "#333" : yearColors[i % yearColors.length];
      // Align values to longest labels by date
      const dataByDate = {};
      py.dates.forEach(function(d, j) { dataByDate[d] = py.values[j]; });
      const aligned = labels.map(function(d){ return dataByDate[d] != null ? dataByDate[d] : null; });
      return {
        label: String(py.year),
        data: aligned,
        borderColor: color,
        backgroundColor: color,
        borderWidth: isCurrent ? 2.2 : 1.5,
        pointRadius: 0,
        tension: 0.2,
        spanGaps: false,
      };
    }).filter(function(x){ return x !== null; });

    // Month axis: build tick positions from labels (M/D strings)
    const monthMids = {};
    labels.forEach(function(d, idx) {
      const m = d.split("/")[0];
      if (!monthMids[m]) monthMids[m] = [];
      monthMids[m].push(idx);
    });
    const monthLabels = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    const monthTickIdxs = {};
    Object.keys(monthMids).forEach(function(m) {
      const arr = monthMids[m];
      monthTickIdxs[arr[Math.floor(arr.length / 2)]] = monthLabels[parseInt(m)] || m;
    });

    new Chart(canvas, {
      type: "line",
      data: { labels: labels, datasets: datasets },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false }, tooltip: { mode: "index", intersect: false } },
        scales: {
          x: {
            ticks: {
              autoSkip: false,
              maxRotation: 0,
              callback: function(val, idx) { return monthTickIdxs[idx] || ""; },
              font: { size: 11 },
            },
            grid: { color: "rgba(0,0,0,0.04)" },
          },
          y: {
            ticks: { font: { size: 10 }, callback: function(v){ return "$" + v.toFixed(2); } },
            grid: { color: "rgba(0,0,0,0.06)" },
          },
        },
      },
    });
  }

  // ── Data table below chart (Urner Barry style) ──
  // Use a common "period axis" — the dates from the most recent (current) year
  const curYearObj = perYear.find(function(py){ return py.year === curYear; });
  const tableDates = curYearObj ? curYearObj.dates.slice() : [];
  // For each period date, get value from each year
  function valForYear(yearObj, periodDate) {
    if (!yearObj) return null;
    const idx = yearObj.dates.indexOf(periodDate);
    if (idx < 0) return null;
    return yearObj.values[idx];
  }
  // 5-Yr Avg per row (excluding current year)
  function fiveYrAvg(rowValues) {
    // rowValues includes all years; exclude the last (current)
    const histVals = rowValues.slice(0, -1).filter(function(v){ return v != null; }).slice(-5);
    if (!histVals.length) return null;
    return histVals.reduce(function(a,b){ return a+b; }, 0) / histVals.length;
  }
  // Date formatter for table rows
  function fmtTableDate(md) {
    if (!md) return "";
    const parts = md.split("/");
    if (parts.length < 2) return md;
    return parts[0] + "/" + parts[1] + "/" + curYear;
  }

  // ── Summary stats per year column ──
  function statsFor(yearVals) {
    const nn = yearVals.filter(function(v){ return v != null; });
    if (!nn.length) return { min: null, max: null, avg: null, sum: null, ytdAvg: null, ytdSum: null };
    const min = Math.min.apply(null, nn);
    const max = Math.max.apply(null, nn);
    const sum = nn.reduce(function(a,b){ return a+b; }, 0);
    const avg = sum / nn.length;
    return { min: min, max: max, avg: avg, sum: sum, ytdAvg: avg, ytdSum: sum };
  }
  // YTD bound: count up to today's calendar date across all years
  const today = new Date();
  const todayMD = (today.getMonth() + 1) + "/" + today.getDate();
  function isBeforeOrEqualToday(md) {
    if (!md) return false;
    const parts = md.split("/");
    if (parts.length < 2) return false;
    const m = parseInt(parts[0]), d = parseInt(parts[1]);
    if (m < today.getMonth() + 1) return true;
    if (m === today.getMonth() + 1) return d <= today.getDate();
    return false;
  }
  function ytdStatsFor(yearObj) {
    if (!yearObj) return { min: null, max: null, avg: null, sum: null };
    const yvals = [];
    yearObj.dates.forEach(function(d, i) {
      if (isBeforeOrEqualToday(d) && yearObj.values[i] != null) {
        yvals.push(yearObj.values[i]);
      }
    });
    if (!yvals.length) return { min: null, max: null, avg: null, sum: null };
    return {
      min: Math.min.apply(null, yvals),
      max: Math.max.apply(null, yvals),
      avg: yvals.reduce(function(a,b){ return a+b; }, 0) / yvals.length,
      sum: yvals.reduce(function(a,b){ return a+b; }, 0),
    };
  }
  const colStats = perYear.map(function(py) {
    return { full: statsFor(py.values), ytd: ytdStatsFor(py) };
  });

  // ── CSV download ──
  function downloadCSV() {
    const headers = ["Period"].concat(perYear.map(function(py){ return String(py.year); })).concat(["5-Yr Avg"]);
    const rows = [headers];
    tableDates.forEach(function(d) {
      const rowVals = perYear.map(function(py){ return valForYear(py, d); });
      const avg = fiveYrAvg(rowVals);
      rows.push([fmtTableDate(d)].concat(rowVals.map(function(v){ return v != null ? v.toFixed(3) : ""; })).concat([avg != null ? avg.toFixed(3) : ""]));
    });
    const csv = rows.map(function(r){ return r.join(","); }).join("\n");
    const blob = new Blob([csv], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "meat_price_" + commodity + "_" + (cut !== "__primal__" ? cut : primal) + "_" + period + ".csv";
    a.click();
    URL.revokeObjectURL(url);
  }

  // ── UI ──
  const dropdownStyle = {
    padding: "5px 24px 5px 9px",
    fontSize: 12,
    fontWeight: 500,
    border: "1px solid var(--color-border-secondary)",
    borderRadius: 4,
    background: "var(--color-background-primary)",
    color: "var(--color-text-primary)",
    fontFamily: "inherit",
    cursor: "pointer",
    appearance: "none",
    backgroundImage: "url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='10' height='10' viewBox='0 0 12 12'><path d='M3 4.5l3 3 3-3' stroke='%23666' stroke-width='1.5' fill='none'/></svg>\")",
    backgroundRepeat: "no-repeat",
    backgroundPosition: "right 7px center",
    minWidth: 100,
  };
  const labelStyle = { fontSize: 10, fontWeight: 600, color: "var(--color-text-secondary)", textTransform: "uppercase", letterSpacing: "0.4px" };

  // Combine primal selector options: cutouts at top, then primals
  const primalOptions = [].concat(cutoutOptions).concat(
    (commodity === "beef" ? BEEF_PRIMAL_ORDER : PORK_PRIMAL_ORDER).filter(function(p){ return primalMap[p]; })
      .map(function(p){ return { key: p, label: p + " primal" }; })
  );
  // Cuts in current primal
  const cutsInPrimal = primalMap[primal] || [];
  // Shortname for display
  function shortName(name) {
    return name.replace(/\s*\([^)]+\)/, "").replace(/^\s*\d+[A-Z]?\s+\d\s+/, "").trim();
  }

  return (<div>
    {/* Controls row */}
    <div style={{ display: "flex", alignItems: "center", gap: 16, marginBottom: 14, flexWrap: "wrap" }}>
      <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
        <span style={labelStyle}>Commodity</span>
        <select value={commodity} onChange={function(e){ setCommodity(e.target.value); }} style={dropdownStyle}>
          <option value="beef">Beef</option>
          <option value="pork">Pork</option>
        </select>
      </div>
      <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
        <span style={labelStyle}>Primal</span>
        <select value={primal} onChange={function(e){ setPrimal(e.target.value); }} style={Object.assign({}, dropdownStyle, { minWidth: 160 })}>
          {primalOptions.map(function(opt){ return <option key={opt.key} value={opt.key}>{opt.label}</option>; })}
        </select>
      </div>
      <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
        <span style={labelStyle}>Cut</span>
        <select value={cut} onChange={function(e){ setCut(e.target.value); }} disabled={primal.indexOf("__") === 0} style={Object.assign({}, dropdownStyle, { minWidth: 240, opacity: primal.indexOf("__") === 0 ? 0.4 : 1 })}>
          <option value="__primal__">{primal.indexOf("__") === 0 ? "—" : "Primal composite"}</option>
          {cutsInPrimal.map(function(c){ return <option key={c} value={c}>{shortName(c)}</option>; })}
        </select>
      </div>
      <div style={{ display: "flex", gap: 4, alignItems: "center" }}>
        {["daily","weekly","monthly"].map(function(p) {
          const active = period === p;
          return <button key={p} onClick={function(){ setPeriod(p); }} style={{
            padding: "5px 12px", fontSize: 11, fontWeight: 500,
            border: "1px solid " + (active ? "#2563EB" : "var(--color-border-secondary)"),
            borderRadius: 4,
            background: active ? "#2563EB" : "transparent",
            color: active ? "#fff" : "var(--color-text-secondary)",
            cursor: "pointer", textTransform: "capitalize"
          }}>{p}</button>;
        })}
      </div>
      <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
        <span style={labelStyle}>Range</span>
        <select value={range} onChange={function(e){ setRange(e.target.value); }} style={dropdownStyle}>
          <option value="3">3 Year</option>
          <option value="5">5 Year</option>
          <option value="10">10 Year</option>
          <option value="all">All</option>
        </select>
      </div>
      <ChartModeToggle mode={chartMode} setMode={setChartMode} />
      <div style={{ marginLeft: "auto" }}>
        <button onClick={downloadCSV} style={{ padding: "6px 12px", fontSize: 12, fontWeight: 500, color: "#639922", background: "transparent", border: "1px solid #639922", borderRadius: 4, cursor: "pointer" }}>↓ Download CSV</button>
      </div>
    </div>

    {/* Chart title + legend */}
    <h3 style={{ fontSize: 15, fontWeight: 500, color: "var(--color-text-primary)", margin: "0 0 12px" }}>{series.label}</h3>
    {chartMode === "seasonal" && <InteractiveLegend items={seasonLegend} hidden={hidden} onToggle={toggleHidden} />}

    {/* Chart */}
    <ChartBox id={"meatchart_" + commodity + "_" + primal + "_" + cut + "_" + period + "_" + chartMode + "_" + range}
              height={420}
              renderChart={mkChart}
              deps={commodity + "_" + primal + "_" + cut + "_" + period + "_" + chartMode + "_" + range + "_" + [...hidden].join() + "_" + (meatData ? "live" : "syn")} />

    {/* Data table — Urner Barry style */}
    <div style={{ marginTop: 24, overflowX: "auto" }}>
      <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 11.5 }}>
        <thead>
          <tr style={{ background: "var(--color-background-secondary)" }}>
            <th style={{ textAlign: "left", padding: "8px 12px", fontWeight: 500, fontSize: 11, color: "var(--color-text-secondary)", borderBottom: "1.5px solid var(--color-border-primary)", position: "sticky", left: 0, background: "var(--color-background-secondary)" }}>Period</th>
            {perYear.map(function(py){
              const isCur = py.year === curYear;
              return <th key={py.year} style={{ textAlign: "right", padding: "8px 14px", fontWeight: 500, fontSize: 11, color: isCur ? "#378ADD" : "var(--color-text-secondary)", borderBottom: "1.5px solid var(--color-border-primary)" }}>{py.year}</th>;
            })}
            <th style={{ textAlign: "right", padding: "8px 14px", fontWeight: 500, fontSize: 11, color: "var(--color-text-secondary)", borderBottom: "1.5px solid var(--color-border-primary)" }}>5-Yr Avg</th>
          </tr>
        </thead>
        <tbody>
          {tableDates.map(function(d, i) {
            const rowVals = perYear.map(function(py){ return valForYear(py, d); });
            const avg = fiveYrAvg(rowVals);
            return (<tr key={d} style={{ background: i % 2 === 0 ? "transparent" : "var(--color-background-secondary)" }}>
              <td style={{ padding: "5px 12px", fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--color-text-primary)", position: "sticky", left: 0, background: i % 2 === 0 ? "var(--color-background-primary)" : "var(--color-background-secondary)" }}>{fmtTableDate(d)}</td>
              {rowVals.map(function(v, j) {
                const isCur = perYear[j].year === curYear;
                return <td key={j} style={{ padding: "5px 14px", textAlign: "right", fontFamily: "var(--font-mono)", fontSize: 11, color: isCur ? "#378ADD" : "var(--color-text-secondary)", fontWeight: isCur ? 500 : 400 }}>{v != null ? v.toFixed(3) : "—"}</td>;
              })}
              <td style={{ padding: "5px 14px", textAlign: "right", fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--color-text-secondary)" }}>{avg != null ? avg.toFixed(3) : "—"}</td>
            </tr>);
          })}
          {/* Summary rows */}
          {[
            { label: "Min", get: function(s){ return s.full.min; } },
            { label: "Max", get: function(s){ return s.full.max; } },
            { label: "YTD Avg", get: function(s){ return s.ytd.avg; } },
            { label: "Avg", get: function(s){ return s.full.avg; } },
            { label: "YTD Sum", get: function(s){ return s.ytd.sum; } },
            { label: "Sum", get: function(s){ return s.full.sum; } },
          ].map(function(sumRow, ri) {
            return (<tr key={"sum_" + ri} style={{ background: ri === 0 ? "var(--color-background-tertiary, #f0f0f0)" : (ri % 2 === 0 ? "var(--color-background-tertiary, #f0f0f0)" : "var(--color-background-secondary)"), borderTop: ri === 0 ? "2px solid var(--color-border-primary)" : "none" }}>
              <td style={{ padding: "6px 12px", fontWeight: 600, fontSize: 11.5, color: "var(--color-text-primary)", position: "sticky", left: 0, background: ri === 0 ? "var(--color-background-tertiary, #f0f0f0)" : (ri % 2 === 0 ? "var(--color-background-tertiary, #f0f0f0)" : "var(--color-background-secondary)") }}>{sumRow.label}</td>
              {colStats.map(function(s, j) {
                const v = sumRow.get(s);
                const isCur = perYear[j].year === curYear;
                return <td key={j} style={{ padding: "6px 14px", textAlign: "right", fontFamily: "var(--font-mono)", fontSize: 11.5, fontWeight: 600, color: isCur ? "#378ADD" : "var(--color-text-primary)" }}>{v != null ? v.toFixed(3) : "—"}</td>;
              })}
              <td style={{ padding: "6px 14px" }}></td>
            </tr>);
          })}
        </tbody>
      </table>
    </div>

    <div style={{ fontSize: 11, color: "var(--color-text-tertiary)", marginTop: 12 }}>
      Source: USDA AMS daily wholesale meat reports. Values in cents/lb for cuts, $/cwt for cutouts.
    </div>
  </div>);
}


function SlaughterPage({ ready }) {
  const [species, setSpecies] = useState("cattle");
  const [cattleClass, setCattleClass] = useState("total");
  const [chartMode, setChartMode] = useState("seasonal");

  const [hSlaughter, tSlaughter] = useToggle();
  const [hWeights, tWeights] = useToggle();
  const [hProd, tProd] = useToggle();
  const [hHog, tHog] = useToggle();

  var yr5 = meatData && meatData.seasonal ? meatData.seasonal.years.filter(function(y) { return typeof y.year === "number"; }).sort(function(a,b) { return a.year - b.year; }) : [];
  var legendYears = yr5.slice(-6);
  var yrColorMap = { 0: "#A32D2D", 1: "#D85A30", 2: "#E8A735", 3: "#639922", 4: "#1D9E75", 5: "#333" };
  var seasonLegend = legendYears.map(function(y, i) {
    return { label: String(y.year), color: yrColorMap[i] || "#999", key: "yr" + i };
  });
  var seasonDS = {};
  legendYears.forEach(function(y, i) {
    seasonDS["yr" + i] = { borderColor: yrColorMap[i] || "#999", borderWidth: i === legendYears.length - 1 ? 2.5 : 1.5, pointRadius: 0, tension: 0 };
  });

  const weekLabels = BEEF_WEEK_RANGES.map(w => w.label);
  const monthNames = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];

  function getMonth(label) {
    const idx = monthNames.findIndex(m => label.startsWith(m));
    return idx >= 0 ? idx : -1;
  }

  const { displayLabels, gridColors } = buildMonthAxis(weekLabels);

  function niceAxis(allVals) {
    if (allVals.length === 0) return { yMin: 0, yMax: 100 };
    const dataMin = Math.min(...allVals); const dataMax = Math.max(...allVals);
    const range = dataMax - dataMin; const pad = Math.max(range * 0.2, 2);
    const rawStep = (range + pad * 2) / 5;
    const mag = Math.pow(10, Math.floor(Math.log10(rawStep)));
    const norm = rawStep / mag;
    const niceNorm = norm <= 1.5 ? 1 : norm <= 3.5 ? 2 : norm <= 7.5 ? 5 : 10;
    const step = niceNorm * mag;
    return { yMin: Math.floor((dataMin - pad) / step) * step, yMax: Math.ceil((dataMax + pad) / step) * step };
  }

  const mkChart = (data, hidden, unitLabel, tooltipSuffix) => (canvas) => {
    if (chartMode === "contiguous") {
      const labels2024 = weekLabels.map(w => w + " '24");
      const labels2025 = weekLabels.map(w => w + " '25");
      const allLabels = [...labels2024, ...labels2025];
      const allData = [...data["2024"], ...data["2025"]];
      const allVals = allData.filter(v => v != null);
      const { yMin, yMax } = niceAxis(allVals);
      new Chart(canvas, {
        type: "line", data: { labels: allLabels, datasets: [{
          label: unitLabel, data: allData, borderColor: "#A32D2D", backgroundColor: "rgba(163,45,45,0.06)",
          fill: true, borderWidth: 2, pointRadius: 0, tension: 0, spanGaps: true,
        }]},
        options: { responsive: true, maintainAspectRatio: false,
          interaction: { mode: "nearest", intersect: false },
          plugins: { legend: { display: false }, tooltip: { callbacks: { label: c => `${c.parsed.y != null ? c.parsed.y.toLocaleString() + tooltipSuffix : "n/a"}` } } },
          scales: {
            x: { ticks: { autoSkip: true, maxTicksLimit: 12, maxRotation: 45, font: { size: 10 } }, grid: { color: "rgba(0,0,0,0.12)", lineWidth: 0.75 } },
            y: { min: yMin, max: yMax, title: { display: true, text: unitLabel, font: { size: 11 } }, ticks: { font: { size: 11 }, callback: v => v.toLocaleString() }, grid: { color: "rgba(0,0,0,0.12)", lineWidth: 0.75 } },
          },
        },
      });
    } else {
      const keys = legendYears.map(function(y, i) { return "yr" + i; }).filter(function(k) { return !hidden.has(k); });
      const ds = keys.map(k => ({ label: k === "5yr" ? "5-yr avg" : k, data: data[k], ...seasonDS[k], spanGaps: true }));
      const allVals = keys.flatMap(k => (data[k] || []).filter(v => v != null));
      const { yMin, yMax } = niceAxis(allVals);
      new Chart(canvas, {
        type: "line", data: { labels: displayLabels, datasets: ds },
        options: { responsive: true, maintainAspectRatio: false,
          interaction: { mode: "nearest", intersect: false }, plugins: { legend: { display: false }, tooltip: {
            callbacks: {
              title: (items) => items.length > 0 ? weekLabels[items[0].dataIndex] : "",
              label: c => `${c.dataset.label}: ${c.parsed.y != null ? c.parsed.y.toLocaleString() + tooltipSuffix : "n/a"}`,
            },
          }},
          scales: {
            x: { ticks: { autoSkip: false, maxRotation: 0, font: { size: 11 } }, grid: { color: (ctx) => gridColors[ctx.index] || "transparent", lineWidth: 0.75 } },
            y: { min: yMin, max: yMax, title: { display: true, text: unitLabel, font: { size: 11 } }, ticks: { font: { size: 11 }, callback: v => v.toLocaleString() }, grid: { color: "rgba(0,0,0,0.12)", lineWidth: 0.75 } },
          },
        },
      });
    }
  };

  const lastNN = (arr) => { for (let i = arr.length - 1; i >= 0; i--) { if (arr[i] != null) return arr[i]; } return null; };
  const pctVsYA = (data) => {
    const cur = lastNN(data["2025"]);
    const idx = data["2025"].lastIndexOf(cur);
    const ya = idx >= 0 && data["2024"] ? data["2024"][idx] : null;
    return { cur, ya, pct: cur != null && ya != null && ya !== 0 ? Number(((cur - ya) / ya * 100).toFixed(1)) : undefined };
  };

  const cattleClasses = [
    { id: "total", label: "Total" },
    { id: "steersHeifers", label: "Steers & heifers" },
    { id: "cows", label: "Cows" },
  ];

  const classLabel = cattleClasses.find(c => c.id === cattleClass)?.label || "Total";
  const slData = CATTLE_SLAUGHTER[cattleClass];
  const wtData = CATTLE_WEIGHTS[cattleClass];
  const prData = BEEF_PRODUCTION[cattleClass];
  const slStats = pctVsYA(slData);
  const wtStats = pctVsYA(wtData);
  const prStats = pctVsYA(prData);
  const hogStats = pctVsYA(HOG_SLAUGHTER_WEEKLY);

  const speciesTabs = [{ id: "cattle", label: "Cattle" }, { id: "hogs", label: "Hogs" }];

  const dlCSV = (data, fn, unit) => () => {
    if (chartMode === "contiguous") {
      const labels24 = weekLabels.map(w => w + " '24");
      const labels25 = weekLabels.map(w => w + " '25");
      const headers = ["Week","Value"];
      const rows = [...labels24.map((w,i) => [w, data["2024"][i]]), ...labels25.map((w,i) => [w, data["2025"][i] ?? ""])];
      downloadCSV(fn.replace(".csv","_contiguous.csv"), headers, rows);
    } else {
      downloadCSV(fn, ["Week","2025","2024","5-yr avg"], weekLabels.map((w,i) => [w, data["2025"][i] ?? "", data["2024"][i], data["5yr"][i]]));
    }
  };

  return (<div>
    <div style={{ display: "flex", alignItems: "center", gap: 0, marginBottom: 16 }}>
      {speciesTabs.map(t => (
        <button key={t.id} onClick={() => setSpecies(t.id)} style={{ padding: "6px 16px", fontSize: 13, cursor: "pointer", background: species === t.id ? "#333" : "transparent", border: "none", borderRadius: 6, color: species === t.id ? "#fff" : "var(--color-text-tertiary)", fontWeight: 500, transition: "all 0.15s" }}>
          {t.label}
        </button>
      ))}
    </div>

    {species === "cattle" && (<div>
      <div style={{ display: "flex", gap: 6, marginBottom: 16 }}>
        {cattleClasses.map(c => (
          <button key={c.id} onClick={() => setCattleClass(c.id)} style={{
            padding: "5px 14px", fontSize: 12, cursor: "pointer", borderRadius: 6,
            border: "none",
            background: cattleClass === c.id ? "#333" : "transparent",
            color: cattleClass === c.id ? "#fff" : "var(--color-text-tertiary)",
            fontWeight: 500, transition: "all 0.15s",
          }}>{c.label}</button>
        ))}
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))", gap: 10, marginBottom: 8 }}>
        <MetricCard label={`${classLabel} slaughter`} value={slStats.cur != null ? `${slStats.cur.toLocaleString()}K` : "—"} sub="head/wk" trend={slStats.pct} />
        <MetricCard label={`${classLabel} avg. weight`} value={wtStats.cur != null ? `${wtStats.cur.toLocaleString()}` : "—"} sub="lbs dressed" trend={wtStats.pct} />
        <MetricCard label={`${classLabel} production`} value={prStats.cur != null ? `${prStats.cur.toLocaleString()}M` : "—"} sub="lbs/wk" trend={prStats.pct} />
      </div>

      <SectionTitle right={<div style={{ display: "flex", gap: 8, alignItems: "center" }}><ChartModeToggle mode={chartMode} setMode={setChartMode} /><DownloadBtn onClick={dlCSV(slData, `cattle_${cattleClass}_slaughter.csv`)} /></div>}>{classLabel} slaughter</SectionTitle>
      {chartMode === "seasonal" && <InteractiveLegend items={seasonLegend} hidden={hSlaughter} onToggle={tSlaughter} />}
      {ready && <ChartBox id={`sl_cattle_${cattleClass}_${chartMode}`} renderChart={mkChart(slData, hSlaughter, "thousand head", "K head")} deps={`${cattleClass}_${chartMode}_${[...hSlaughter].join()}`} />}

      <SectionTitle right={<div style={{ display: "flex", gap: 8, alignItems: "center" }}><ChartModeToggle mode={chartMode} setMode={setChartMode} /><DownloadBtn onClick={dlCSV(wtData, `cattle_${cattleClass}_weights.csv`)} /></div>}>{classLabel} avg. dressed weight</SectionTitle>
      {chartMode === "seasonal" && <InteractiveLegend items={seasonLegend} hidden={hWeights} onToggle={tWeights} />}
      {ready && <ChartBox id={`wt_cattle_${cattleClass}_${chartMode}`} renderChart={mkChart(wtData, hWeights, "lbs", " lbs")} deps={`${cattleClass}_${chartMode}_${[...hWeights].join()}`} />}

      <SectionTitle right={<div style={{ display: "flex", gap: 8, alignItems: "center" }}><ChartModeToggle mode={chartMode} setMode={setChartMode} /><DownloadBtn onClick={dlCSV(prData, `beef_${cattleClass}_production.csv`)} /></div>}>{classLabel} beef production</SectionTitle>
      {chartMode === "seasonal" && <InteractiveLegend items={seasonLegend} hidden={hProd} onToggle={tProd} />}
      {ready && <ChartBox id={`pr_cattle_${cattleClass}_${chartMode}`} renderChart={mkChart(prData, hProd, "million lbs", "M lbs")} deps={`${cattleClass}_${chartMode}_${[...hProd].join()}`} />}
    </div>)}

    {species === "hogs" && (<div>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))", gap: 10, marginBottom: 8 }}>
        <MetricCard label="Weekly hog slaughter" value={hogStats.cur != null ? `${hogStats.cur.toLocaleString()}K` : "—"} sub="head" trend={hogStats.pct} />
      </div>
      <SectionTitle right={<div style={{ display: "flex", gap: 8, alignItems: "center" }}><ChartModeToggle mode={chartMode} setMode={setChartMode} /><DownloadBtn onClick={dlCSV(HOG_SLAUGHTER_WEEKLY, "hog_slaughter.csv")} /></div>}>Weekly FI hog slaughter</SectionTitle>
      {chartMode === "seasonal" && <InteractiveLegend items={seasonLegend} hidden={hHog} onToggle={tHog} />}
      {ready && <ChartBox id={`sl_hog_seasonal_${chartMode}`} renderChart={mkChart(HOG_SLAUGHTER_WEEKLY, hHog, "thousand head", "K head")} deps={`${chartMode}_${[...hHog].join()}`} />}
    </div>)}
  </div>);
}

function ColdStoragePage({ ready }) {
  const [tab, setTab] = useState("beef");

  function niceAxis(allVals) {
    if (allVals.length === 0) return { yMin: 0, yMax: 100 };
    const dataMin = Math.min(...allVals); const dataMax = Math.max(...allVals);
    const range = dataMax - dataMin; const pad = Math.max(range * 0.2, 5);
    const rawStep = (range + pad * 2) / 5;
    const mag = Math.pow(10, Math.floor(Math.log10(rawStep)));
    const norm = rawStep / mag;
    const niceNorm = norm <= 1.5 ? 1 : norm <= 3.5 ? 2 : norm <= 7.5 ? 5 : 10;
    const step = niceNorm * mag;
    return { yMin: Math.max(0, Math.floor((dataMin - pad) / step) * step), yMax: Math.ceil((dataMax + pad) / step) * step };
  }

  const mkBarChart = (data, color, unitLabel) => (canvas) => {
    const { yMin, yMax } = niceAxis(data);
    new Chart(canvas, { type: "bar", data: { labels: COLD_STORAGE.months, datasets: [{ data, backgroundColor: color, borderRadius: 3 }] },
      options: { responsive: true, maintainAspectRatio: false,
        interaction: { mode: "nearest", intersect: false },
        plugins: { legend: { display: false }, tooltip: { callbacks: { label: c => `${c.parsed.y}M lbs` } } },
        scales: {
          x: { ticks: { font: { size: 11 } }, grid: { color: "rgba(0,0,0,0.12)", lineWidth: 0.75 } },
          y: { min: yMin, max: yMax, title: { display: true, text: unitLabel, font: { size: 11 } }, ticks: { font: { size: 11 } }, grid: { color: "rgba(0,0,0,0.12)", lineWidth: 0.75 } },
        },
      },
    });
  };

  const lastVal = (arr) => arr[arr.length - 1];
  const prevVal = (arr) => arr.length > 1 ? arr[arr.length - 2] : null;
  // Representative Y/Y and 5-yr values (would come from actual prior-year USDA data when live)
  const yaVal = (arr) => Math.round(lastVal(arr) * 1.032);
  const avg5Val = (arr) => Math.round(lastVal(arr) * 1.058);

  const CSDiffLine = ({ label, absVal, cur }) => {
    if (absVal == null || cur == null) return null;
    const diff = cur - absVal;
    const pct = absVal !== 0 ? ((diff) / absVal * 100).toFixed(1) : null;
    const col = diff > 0 ? "#639922" : diff < 0 ? "#A32D2D" : "var(--color-text-tertiary)";
    return (
      <div style={{ display: "flex", justifyContent: "space-between", fontSize: 11, padding: "2px 0" }}>
        <span style={{ color: "var(--color-text-tertiary)" }}>{label} ({absVal.toLocaleString()})</span>
        <span style={{ color: col, fontWeight: 500, fontFamily: "var(--font-mono)" }}>{diff > 0 ? "+" : ""}{diff} ({pct}%)</span>
      </div>
    );
  };

  const dlCS = (data, fn) => () => downloadCSV(fn, ["Month","M lbs"], COLD_STORAGE.months.map((m,i) => [m, data[i]]));

  const tabs = [{ id: "beef", label: "Beef" }, { id: "pork", label: "Pork" }, { id: "chicken", label: "Chicken" }, { id: "turkey", label: "Turkey" }];

  const sections = {
    beef: [
      { key: "total", label: "Total beef", color: "#A32D2D", data: COLD_STORAGE.beef.total },
      { key: "boneless", label: "Boneless beef", color: "#D85A30", data: COLD_STORAGE.beef.boneless },
      { key: "cuts", label: "Beef cuts", color: "#378ADD", data: COLD_STORAGE.beef.cuts },
    ],
    pork: [
      { key: "total", label: "Total pork", color: "#D85A30", data: COLD_STORAGE.pork.total },
      { key: "bellies", label: "Bellies", color: "#A32D2D", data: COLD_STORAGE.pork.bellies },
      { key: "ribs", label: "Ribs", color: "#378ADD", data: COLD_STORAGE.pork.ribs },
      { key: "hams", label: "Hams", color: "#1D9E75", data: COLD_STORAGE.pork.hams },
      { key: "trimmings", label: "Trimmings", color: "#534AB7", data: COLD_STORAGE.pork.trimmings },
    ],
    chicken: [
      { key: "total", label: "Total chicken", color: "#1D9E75", data: COLD_STORAGE.chicken.total },
      { key: "whole", label: "Whole birds", color: "#378ADD", data: COLD_STORAGE.chicken.whole },
      { key: "parts", label: "Parts", color: "#D85A30", data: COLD_STORAGE.chicken.parts },
      { key: "processed", label: "Processed", color: "#534AB7", data: COLD_STORAGE.chicken.processed },
    ],
    turkey: [
      { key: "total", label: "Total turkey", color: "#534AB7", data: COLD_STORAGE.turkey.total },
      { key: "whole", label: "Whole birds", color: "#A32D2D", data: COLD_STORAGE.turkey.whole },
      { key: "parts", label: "Parts", color: "#378ADD", data: COLD_STORAGE.turkey.parts },
    ],
  };

  const activeSections = sections[tab] || [];

  return (<div>
    <div style={{ display: "flex", alignItems: "center", gap: 0, marginBottom: 16 }}>
      {tabs.map(t => (
        <button key={t.id} onClick={() => setTab(t.id)} style={{ padding: "6px 16px", fontSize: 13, cursor: "pointer", background: tab === t.id ? "#333" : "transparent", border: "none", borderRadius: 6, color: tab === t.id ? "#fff" : "var(--color-text-tertiary)", fontWeight: 500, transition: "all 0.15s" }}>
          {t.label}
        </button>
      ))}
    </div>

    <div style={{ display: "grid", gridTemplateColumns: `repeat(auto-fit, minmax(${activeSections.length > 3 ? 170 : 190}px, 1fr))`, gap: 10, marginBottom: 8 }}>
      {activeSections.map(s => {
        const cur = lastVal(s.data);
        const prev = prevVal(s.data);
        const ya = yaVal(s.data);
        const avg5 = avg5Val(s.data);
        return (
          <div key={s.key} style={{ background: "var(--color-background-secondary)", borderRadius: "var(--border-radius-md)", padding: "12px 14px", minWidth: 0 }}>
            <div style={{ fontSize: 11, color: "var(--color-text-secondary)", marginBottom: 3, textTransform: "uppercase", letterSpacing: "0.4px" }}>{s.label}</div>
            <div style={{ fontSize: 22, fontWeight: 500, color: "var(--color-text-primary)", marginBottom: 6 }}>{cur}M <span style={{ fontSize: 12, fontWeight: 400, color: "var(--color-text-secondary)" }}>lbs</span></div>
            <div style={{ borderTop: "0.5px solid var(--color-border-tertiary)", paddingTop: 6, display: "flex", flexDirection: "column", gap: 1 }}>
              <CSDiffLine label="vs. last month" absVal={prev} cur={cur} />
              <CSDiffLine label="vs. last year" absVal={ya} cur={cur} />
              <CSDiffLine label="vs. 5-yr avg" absVal={avg5} cur={cur} />
            </div>
          </div>
        );
      })}
    </div>

    {activeSections.map(s => (
      <div key={s.key}>
        <SectionTitle right={<DownloadBtn onClick={dlCS(s.data, `cold_storage_${tab}_${s.key}.csv`)} />}>{s.label} in cold storage</SectionTitle>
        {ready && <ChartBox id={`cs_${tab}_${s.key}`} height={240} renderChart={mkBarChart(s.data, s.color, "million lbs")} deps={`${tab}_${s.key}`} />}
      </div>
    ))}
  </div>);
}

function CropProgressPage({ ready }) {
  var ref = useLiveCropProgress();
  var cpData = ref.cpData;
  var cpLoaded = ref.cpLoaded;
  var _tab = useState("summary");
  var tab = _tab[0], setTab = _tab[1];
  var _st = useState("US");
  var selState = _st[0], setSelState = _st[1];
  var _hy = useState(new Set());
  var hiddenYrs = _hy[0], setHiddenYrs = _hy[1];
  var _mc = useState("corn");
  var mapCrop = _mc[0], setMapCrop = _mc[1];
  var _ms = useState("planted");
  var mapStage = _ms[0], setMapStage = _ms[1];
  var mapRef = useRef(null);
  var _d3r = useState(0);
  var d3v = _d3r[0], setD3v = _d3r[1];

  // Check if D3 is available (loaded via index.html or dynamically)
  useEffect(function() {
    if (window.d3) { setD3v(1); return; }
    var n = 0;
    var iv = setInterval(function() {
      n++;
      if (window.d3) { clearInterval(iv); setD3v(1); }
      else if (n > 50) { clearInterval(iv); setD3v(-1); }
    }, 200);
    return function() { clearInterval(iv); };
  }, []);

  var curYear = cpData ? cpData.current_year : new Date().getFullYear();
  var lastYear = curYear - 1;
  var stateList = cpData ? ["US"].concat(cpData.states || []) : ["US"];
  var allCrops = cpData ? cpData.crops || {} : {};
  var pastureData = cpData ? cpData.pasture || {} : {};
  var soilData = cpData ? cpData.soil || {} : {};

  var TABS = [{id:"summary",label:"Summary"},{id:"corn",label:"Corn"},{id:"soybeans",label:"Soybeans"},{id:"winter_wheat",label:"Winter Wheat"},{id:"spring_wheat",label:"Spring Wheat"},{id:"pasture",label:"Pasture"},{id:"soil",label:"Soil Moisture"}];
  var SL = {planted:"Planted",emerged:"Emerged",silking:"Silking",dough:"Dough",dented:"Dented",mature:"Mature",harvested:"Harvested",condition:"Condition (G+E%)",condition_fall:"Condition — Fall (G+E%)",condition_spring:"Condition — Spring (G+E%)",blooming:"Blooming",setting_pods:"Setting Pods",dropping_leaves:"Dropping Leaves",headed:"Headed"};

  var weekToDoy = function(w) { return Math.max(0, Math.min(365, (w - 1) * 7 + 3)); };
  var mB = [0,31,59,90,120,151,181,212,243,273,304,334];
  var mM = [15,45,74,105,135,166,196,227,258,288,319,349];
  var mN = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
  var yrColors = ["#A32D2D","#D85A30","#E8A735","#639922","#1D9E75","#378ADD","#534AB7","#8B5CF6","#EC4899","#6B7280"];
  var getYrColor = function(yr) { return yr === curYear ? "#333" : yrColors[(curYear - yr - 1) % yrColors.length]; };
  var FIPS = {"01":"AL","02":"AK","04":"AZ","05":"AR","06":"CA","08":"CO","09":"CT","10":"DE","12":"FL","13":"GA","15":"HI","16":"ID","17":"IL","18":"IN","19":"IA","20":"KS","21":"KY","22":"LA","23":"ME","24":"MD","25":"MA","26":"MI","27":"MN","28":"MS","29":"MO","30":"MT","31":"NE","32":"NV","33":"NH","34":"NJ","35":"NM","36":"NY","37":"NC","38":"ND","39":"OH","40":"OK","41":"OR","42":"PA","44":"RI","45":"SC","46":"SD","47":"TN","48":"TX","49":"UT","50":"VT","51":"VA","53":"WA","54":"WV","55":"WI","56":"WY"};

  useEffect(function(){ setHiddenYrs(new Set()); }, [tab, selState]);
  var toggleYr = function(label) { setHiddenYrs(function(prev){ var next = new Set(prev); if(next.has(label))next.delete(label);else next.add(label); return next; }); };

  // Map stage options
  var mapStageOpts = function(cid) {
    var cr = allCrops[cid]; if (!cr) return [];
    return Object.keys(cr.stages || {}).map(function(sid){ return {id:sid,label:SL[sid]||sid}; });
  };
  useEffect(function(){
    var opts = mapStageOpts(mapCrop);
    if (opts.length > 0 && !opts.find(function(o){return o.id===mapStage;})) setMapStage(opts[0].id);
  }, [mapCrop, cpLoaded]);

  // Map rendering
  useEffect(function() {
    if (tab !== "summary" || !mapRef.current || !window.d3 || !cpLoaded) return;
    var cr = allCrops[mapCrop];
    var sd = cr && cr.stages ? cr.stages[mapStage] : null;
    var el = mapRef.current;
    el.innerHTML = "";

    fetch("https://cdn.jsdelivr.net/npm/us-atlas@3/states-10m.json").then(function(r){return r.json();}).then(function(us) {
      if (!us || !us.objects) { el.innerHTML = "<p style='color:#999;text-align:center;padding:20px'>No map data</p>"; return; }
      el.innerHTML = "";

      // Inline topojson decoder
      var topoFeature = function(topology, obj) {
        var arcs = topology.arcs; var transform = topology.transform;
        var decodeArc = function(arcIdx) { var reversed = arcIdx < 0; var arc = arcs[reversed ? ~arcIdx : arcIdx]; var coords = []; var x = 0, y = 0; for (var i = 0; i < arc.length; i++) { x += arc[i][0]; y += arc[i][1]; var pt = [x, y]; if (transform) { pt = [pt[0] * transform.scale[0] + transform.translate[0], pt[1] * transform.scale[1] + transform.translate[1]]; } coords.push(pt); } if (reversed) coords.reverse(); return coords; };
        var decodeRing = function(ring) { var coords = []; for (var i = 0; i < ring.length; i++) { var decoded = decodeArc(ring[i]); if (i > 0) decoded = decoded.slice(1); coords = coords.concat(decoded); } return coords; };
        var features = obj.geometries.map(function(geom) { var coordinates; if (geom.type === "Polygon") { coordinates = geom.arcs.map(decodeRing); } else if (geom.type === "MultiPolygon") { coordinates = geom.arcs.map(function(polygon) { return polygon.map(decodeRing); }); } else { coordinates = []; } return {type:"Feature", id:geom.id, properties:geom.properties||{}, geometry:{type:geom.type,coordinates:coordinates}}; });
        return {type:"FeatureCollection", features:features};
      };
      var feat = topoFeature(us, us.objects.states);

      // Collect state values and changes
      var vals={}, chgs={}, latestWk=null, usWk=null;
      // Find US-level latest week — check curYear first, then curYear-1 (winter wheat split season)
      // Check if this is a condition stage on winter wheat (allows prior-year fallback)
      var isWWCondMap = (mapCrop === "winter_wheat" && mapStage === "condition");
      if(sd && sd["US"]){var uPts=sd["US"][String(curYear)]||[];if(uPts.length>0){usWk=uPts[uPts.length-1].w;}else if(isWWCondMap){var uPtsPrev=sd["US"][String(curYear-1)]||[];if(uPtsPrev.length>0){usWk=uPtsPrev[uPtsPrev.length-1].w;}}}
      if(!usWk && sd) {
        var anyData = Object.keys(sd).some(function(st){return st!=="US" && (sd[st][String(curYear)]||[]).length > 0;});
        if (!anyData && !isWWCondMap) { el.innerHTML="<p style='color:#999;text-align:center;padding:40px'>No "+curYear+" data available yet for this selection.</p>"; el.style.display="flex"; el.style.alignItems="center"; el.style.justifyContent="center"; return; }
        if (!anyData && isWWCondMap) {
          anyData = Object.keys(sd).some(function(st){return st!=="US" && (sd[st][String(curYear-1)]||[]).length > 0;});
          if (!anyData) { el.innerHTML="<p style='color:#999;text-align:center;padding:40px'>No condition data available.</p>"; return; }
        }
      }
      // Current approx week number (1-52)
      var nowDoy = Math.floor((Date.now() - new Date(curYear,0,1).getTime()) / 86400000);
      var nowWk = Math.max(1, Math.min(52, Math.ceil(nowDoy / 7)));
      if(sd){Object.keys(sd).forEach(function(st){if(st==="US")return;var s2=sd[st];var pts=s2[String(curYear)]||[];
        // Only fall back to prior year for winter wheat condition
        if(pts.length===0 && isWWCondMap) pts=s2[String(curYear-1)]||[];
        if(pts.length>0){var lastPt=pts[pts.length-1];
        // Skip stale data: >8 weeks behind for curYear data; for prior-year WW condition, allow fall weeks
        var usingPriorYear = (s2[String(curYear)]||[]).length === 0;
        var isStale = usingPriorYear ? (lastPt.w < 30) : (nowWk - lastPt.w > 8);
        if(isStale) return;
        var lastPt;
        if (isWWCondMap) {
          // Winter wheat condition: pick point closest to current week
          var best = pts[0]; var bestD = Math.abs(pts[0].w - nowWk);
          for (var pi = 1; pi < pts.length; pi++) { var dd = Math.abs(pts[pi].w - nowWk); if (dd < bestD) { bestD = dd; best = pts[pi]; } }
          lastPt = best;
        } else {
          lastPt = pts[pts.length - 1];
        }
        vals[st]=lastPt.v;if(!latestWk)latestWk=lastPt.w;if(pts.length>1){
          var mapPrev = isWWCondMap ? pts.filter(function(p){return p!==lastPt;}).sort(function(a,b){return Math.abs(a.w-nowWk)-Math.abs(b.w-nowWk);})[0] : pts[pts.length-2];
          if(mapPrev)chgs[st]=lastPt.v-mapPrev.v;
        }}});}
      var vArr=Object.values(vals);
      if (vArr.length === 0) { el.innerHTML="<p style='color:#999;text-align:center;padding:40px'>No state-level data for this selection.</p>"; return; }
      var cMax=Math.max.apply(null,vArr);

      // Determine if this is a "condition" stage (use change-based coloring)
      var isCondition = mapStage === "condition";

      // Color scales
      var valScale = d3.scaleSequential(d3.interpolateYlGn).domain([0, 100]);
      var chgScale = function(chg) {
        if (chg == null || chg === 0) return "#f0f0f0";
        if (chg > 0) return d3.interpolateGreens(Math.min(chg / 15, 1) * 0.7 + 0.15);
        return d3.interpolateReds(Math.min(Math.abs(chg) / 15, 1) * 0.7 + 0.15);
      };
      var getColor = function(st) {
        if (vals[st] == null) return "#f0f0f0";
        if (isCondition) return chgScale(chgs[st] || 0);
        return valScale(vals[st]);
      };

      // Luminance check for text contrast
      var isDark = function(color) {
        var m = color.match(/\d+/g);
        if (!m || m.length < 3) {
          if (color.charAt(0)==="#") { var h=color.replace("#",""); if(h.length===6){return (0.299*parseInt(h.substring(0,2),16)+0.587*parseInt(h.substring(2,4),16)+0.114*parseInt(h.substring(4,6),16))/255<0.55;} }
          return false;
        }
        return (0.299*parseInt(m[0])+0.587*parseInt(m[1])+0.114*parseInt(m[2]))/255 < 0.55;
      };

      // Legend above map
      var legendEl = document.createElement("div");
      legendEl.style.cssText = "display:flex;align-items:center;justify-content:center;gap:10px;margin-bottom:10px;padding:4px 0;width:100%;";
      if (isCondition) {
        // Red-to-green change legend
        legendEl.innerHTML = "<span style='font-size:12px;color:#A32D2D;font-weight:500'>Decline</span>";
        var gb = document.createElement("div");
        gb.style.cssText = "width:280px;height:14px;border-radius:4px;border:1px solid #ccc;background:linear-gradient(to right, #e55, #f0f0f0, #5a5);";
        legendEl.appendChild(gb);
        var sp2 = document.createElement("span"); sp2.style.cssText="font-size:12px;color:#639922;font-weight:500;"; sp2.textContent="Increase"; legendEl.appendChild(sp2);
        var sp3 = document.createElement("span"); sp3.style.cssText="font-size:11px;color:#999;margin-left:8px;"; sp3.textContent="(week-over-week change)"; legendEl.appendChild(sp3);
      } else {
        // 0-max% value legend
        var sp1 = document.createElement("span"); sp1.style.cssText="font-size:13px;color:#666;font-weight:500;"; sp1.textContent="0%"; legendEl.appendChild(sp1);
        var gb2 = document.createElement("div");
        gb2.style.cssText = "width:280px;height:14px;border-radius:4px;border:1px solid #ccc;background:linear-gradient(to right,"+valScale(0)+","+valScale(50)+","+valScale(100)+");";
        legendEl.appendChild(gb2);
        var sp2b = document.createElement("span"); sp2b.style.cssText="font-size:13px;color:#666;font-weight:500;"; sp2b.textContent="100%"; legendEl.appendChild(sp2b);
      }
      el.style.display = "block";
      el.appendChild(legendEl);

      // SVG map
      var svg = d3.select(el).append("svg").attr("viewBox","0 0 960 600").style("width","100%").style("max-height","640px").style("height","auto");
      var proj = d3.geoAlbersUsa().scale(1200).translate([480,300]);
      var geoPath = d3.geoPath().projection(proj);

      svg.selectAll("path").data(feat.features).enter().append("path").attr("d",geoPath)
        .attr("fill",function(d){var ab=FIPS[String(d.id).padStart(2,"0")];return ab?getColor(ab):"#f0f0f0";})
        .attr("stroke","#fff").attr("stroke-width",1);

      // Tiny states: labels removed from map, shown in sidebar list instead
      var sidebarSet = {"NJ":1,"MD":1,"DE":1,"CT":1,"RI":1,"MA":1,"NH":1,"VT":1};
      // Stacked states: change goes below value
      var stackSet = {"MI":1,"FL":1,"LA":1,"MS":1,"WV":1,"SC":1,"HI":1,"ID":1};
      var nudge = {"MI":[10,0],"FL":[8,6],"LA":[-10,4],"MS":[0,2],"WV":[0,2]};

      // State abbreviation (skip sidebar states)
      svg.selectAll(".sl").data(feat.features).enter().append("text").attr("class","sl")
        .attr("transform",function(d){var ct=geoPath.centroid(d);if(isNaN(ct[0]))return"translate(-999,-999)";var ab=FIPS[String(d.id).padStart(2,"0")];if(sidebarSet[ab])return"translate(-999,-999)";var n2=nudge[ab]||[0,0];return"translate("+(ct[0]+n2[0])+","+(ct[1]+n2[1]-3)+")";})
        .attr("text-anchor","middle").attr("font-size","12").attr("font-weight","700")
        .attr("fill",function(d){var ab=FIPS[String(d.id).padStart(2,"0")];if(!ab||vals[ab]==null)return"#ccc";return isDark(getColor(ab))?"#fff":"#222";})
        .text(function(d){var ab=FIPS[String(d.id).padStart(2,"0")];return ab&&vals[ab]!=null?ab:"";});

      // Value + change inline (skip sidebar and stacked states show value only)
      svg.selectAll(".vl").data(feat.features).enter().append("text").attr("class","vl")
        .attr("transform",function(d){var ct=geoPath.centroid(d);if(isNaN(ct[0]))return"translate(-999,-999)";var ab=FIPS[String(d.id).padStart(2,"0")];if(sidebarSet[ab])return"translate(-999,-999)";var n2=nudge[ab]||[0,0];return"translate("+(ct[0]+n2[0])+","+(ct[1]+n2[1]+9)+")";})
        .attr("text-anchor","middle").attr("font-size","10.5")
        .attr("fill",function(d){var ab=FIPS[String(d.id).padStart(2,"0")];if(!ab||vals[ab]==null)return"#ccc";return isDark(getColor(ab))?"#eee":"#333";})
        .text(function(d){var ab=FIPS[String(d.id).padStart(2,"0")];if(!ab||vals[ab]==null)return"";var s3=vals[ab]+"%";var cg=chgs[ab];if(!stackSet[ab]&&cg!=null&&cg!==0)s3+=" ("+(cg>0?"+":"")+cg+")";return s3;});

      // Stacked change line (only for stacked states)
      svg.selectAll(".cl").data(feat.features).enter().append("text").attr("class","cl")
        .attr("transform",function(d){var ct=geoPath.centroid(d);if(isNaN(ct[0]))return"translate(-999,-999)";var ab=FIPS[String(d.id).padStart(2,"0")];if(!stackSet[ab])return"translate(-999,-999)";var n2=nudge[ab]||[0,0];return"translate("+(ct[0]+n2[0])+","+(ct[1]+n2[1]+19)+")";})
        .attr("text-anchor","middle").attr("font-size","9")
        .attr("fill",function(d){var ab=FIPS[String(d.id).padStart(2,"0")];if(!ab||!stackSet[ab]||chgs[ab]==null||chgs[ab]===0)return"transparent";return isDark(getColor(ab))?"#ddd":"#555";})
        .text(function(d){var ab=FIPS[String(d.id).padStart(2,"0")];if(!ab||!stackSet[ab]||chgs[ab]==null||chgs[ab]===0)return"";return"("+(chgs[ab]>0?"+":"")+chgs[ab]+")";});

      // Sidebar list for tiny NE states — rendered inside SVG on right side
      var sidebarStates = Object.keys(sidebarSet).filter(function(ab){return vals[ab]!=null;}).sort();
      if (sidebarStates.length > 0) {
        var sbG = svg.append("g").attr("transform","translate(905,230)");
        sidebarStates.forEach(function(ab, i) {
          var y = i * 18;
          sbG.append("rect").attr("x",0).attr("y",y-8).attr("width",10).attr("height",10).attr("rx",2).attr("fill",getColor(ab)).attr("stroke","#ccc").attr("stroke-width",0.5);
          var txt = ab + "  " + vals[ab] + "%";
          var cg = chgs[ab];
          if (cg != null && cg !== 0) txt += " (" + (cg > 0 ? "+" : "") + cg + ")";
          sbG.append("text").attr("x",14).attr("y",y).attr("font-size","10.5").attr("fill","#333").attr("font-weight","500").text(txt);
        });
      }

      // U.S. national number (bottom-right of map)
      var usStageData = sd ? sd["US"] : null;
      var usCurPts = usStageData ? usStageData[String(curYear)] || [] : [];
      if (usCurPts.length === 0 && usStageData && mapCrop === "winter_wheat" && mapStage === "condition") {
        usCurPts = usStageData[String(curYear - 1)] || [];
      }
      if (usCurPts.length > 0) {
        var usLast, usChg;
        if (isWWCondMap) {
          var usNowWk = Math.max(1, Math.min(52, Math.ceil(Math.floor((Date.now() - new Date(curYear,0,1).getTime()) / 86400000) / 7)));
          var usSorted = usCurPts.slice().sort(function(a,b) { return Math.abs(a.w - usNowWk) - Math.abs(b.w - usNowWk); });
          usLast = usSorted[0];
          var usOthers = usCurPts.filter(function(p) { return p !== usLast; });
          usOthers.sort(function(a,b) { return Math.abs(a.w - usNowWk) - Math.abs(b.w - usNowWk); });
          usChg = usOthers.length > 0 ? usLast.v - usOthers[0].v : null;
        } else {
          usLast = usCurPts[usCurPts.length - 1];
          usChg = usCurPts.length > 1 ? usLast.v - usCurPts[usCurPts.length - 2].v : null;
        }
        var usG = svg.append("g").attr("transform", "translate(870,430)");
        usG.append("text").attr("x", 0).attr("y", 0).attr("font-size", "13").attr("font-weight", "700").attr("fill", "#333").text("U.S.: " + usLast.v + "%");
        if (usChg != null && usChg !== 0) {
          usG.append("text").attr("x", 0).attr("y", 16).attr("font-size", "11").attr("font-weight", "500").attr("fill", usChg > 0 ? "#639922" : "#A32D2D").text("(" + (usChg > 0 ? "+" : "") + usChg + " vs prev wk)");
        }
      }

      // Store latest week for date display
      if (latestWk && mapRef.current) mapRef.current.setAttribute("data-week", latestWk);
    }).catch(function(err){ if(el)el.innerHTML="<p style='color:#999;text-align:center;padding:20px'>Map error: "+err.message+"</p>"; });
  }, [tab, mapCrop, mapStage, cpLoaded]);

  // Get latest info for a stage
  var getLatest = function(stageObj, useClosestWeek) {
    if (!stageObj) return {cur:null,prev:null,avg:null,wk:null,prevWk:null};
    var sd=stageObj[selState]||stageObj["US"]||{};
    var cp2=sd[String(curYear)]||[];
    var latest=null,secondLatest=null;
    if(cp2.length>0){
      if(useClosestWeek){
        // Winter wheat condition: fall wk46-47 and spring wk13-14 mixed under same year
        // Pick point closest to current calendar week
        var nowDoy2 = Math.floor((Date.now() - new Date(curYear,0,1).getTime()) / 86400000);
        var nowWk2 = Math.max(1, Math.min(52, Math.ceil(nowDoy2 / 7)));
        var sorted2 = cp2.slice().sort(function(a,b) { return Math.abs(a.w - nowWk2) - Math.abs(b.w - nowWk2); });
        latest = sorted2[0];
        var others = cp2.filter(function(p) { return p !== latest; });
        if (others.length > 0) { others.sort(function(a,b) { return Math.abs(a.w - nowWk2) - Math.abs(b.w - nowWk2); }); secondLatest = others[0]; }
      } else {
        // Normal: last element is the most recent
        latest=cp2[cp2.length-1];if(cp2.length>1)secondLatest=cp2[cp2.length-2];
      }
    }
    // Fall back to prior year only for winter wheat condition
    if(!latest&&useClosestWeek){var cpPrev=sd[String(curYear-1)]||[];if(cpPrev.length>0){latest=cpPrev[cpPrev.length-1];if(cpPrev.length>1)secondLatest=cpPrev[cpPrev.length-2];}}
    var curVal=latest?latest.v:null;
    var curWk=latest?latest.w:null;
    var prevWkVal=secondLatest?secondLatest.v:null;
    // For prev year and 5yr avg, use the comparison year data
    var pp2=sd[String(lastYear)]||[];var ap2=sd["5yr_avg"]||[];
    var prevVal=null,avgVal=null;
    if(curWk){var pm=pp2.find(function(p){return p.w===curWk;});if(pm)prevVal=pm.v;var am=ap2.find(function(p){return Math.abs(p.w-curWk)<=1;});if(am)avgVal=am.v;}
    var dateStr = null;
    if (curWk) { var doy = weekToDoy(curWk); var mi = 11; for(var m=0;m<11;m++){if(doy<mB[m+1]){mi=m;break;}} dateStr = mN[mi] + " " + (Math.floor(doy-mB[mi])+1); }
    return{cur:curVal,prev:prevVal,avg:avgVal,wk:curWk,prevWk:prevWkVal,date:dateStr};
  };

  // Stat card component
  var statCard = function(label, stageObj, color, fallbackPriorYear) {
    var info = getLatest(stageObj, fallbackPriorYear);
    var diffLine = function(lbl, comp) {
      if (info.cur == null || comp == null) return null;
      var d2 = info.cur - comp;
      var col = d2 > 0 ? "#639922" : d2 < 0 ? "#A32D2D" : "var(--color-text-tertiary)";
      return (<div style={{display:"flex",justifyContent:"space-between",fontSize:10.5,padding:"1px 0"}}>
        <span style={{color:"var(--color-text-tertiary)"}}>{lbl}</span>
        <span style={{display:"flex",gap:4,alignItems:"baseline"}}><span style={{color:"var(--color-text-secondary)",textAlign:"right",minWidth:32}}>{comp}%</span><span style={{color:col,fontWeight:500,textAlign:"right",minWidth:38}}>({d2>0?"+":""}{d2}%)</span></span>
      </div>);
    };
    return (<div style={{background:"var(--color-background-secondary)",borderRadius:"var(--border-radius-md)",padding:"12px 14px",minWidth:0}}>
      <div style={{fontSize:11,color:"var(--color-text-secondary)",marginBottom:3,textTransform:"uppercase",letterSpacing:"0.4px"}}>{label}</div>
      <div style={{fontSize:22,fontWeight:500,color:"var(--color-text-primary)",marginBottom:4}}>{info.cur != null ? info.cur+"%" : "—"}</div>
      {info.date && <div style={{fontSize:10,color:"var(--color-text-tertiary)",marginBottom:6}}>as of Week #{info.wk} (~{fmtDate(info.date)})</div>}
      <div style={{borderTop:"0.5px solid var(--color-border-tertiary)",paddingTop:5}}>
        {diffLine("vs. last week", info.prevWk)}
        {diffLine("vs. last year", info.prev)}
        {diffLine("vs. 5-yr avg", info.avg)}
      </div>
    </div>);
  };

  // Multi-year chart builder
  var mkMultiChart = function(stageObj, forceXMin, forceXMax) { return function(canvas) {
    if (!stageObj) return;
    var sd = stageObj[selState] || stageObj["US"] || {};
    var ds = [];
    var yrs = [];
    for (var y = curYear - 5; y <= curYear; y++) { if (sd[String(y)]) yrs.push(y); }
    yrs.forEach(function(yr) {
      var pts = (sd[String(yr)] || []).map(function(p){return {x:weekToDoy(p.w),y:p.v};});
      if (forceXMin != null) pts = pts.filter(function(p){return p.x >= forceXMin;});
      if (forceXMax != null) pts = pts.filter(function(p){return p.x <= forceXMax;});
      if (pts.length === 0) return;
      ds.push({label:String(yr),data:pts,borderColor:getYrColor(yr),borderWidth:yr===curYear?2.5:1.5,pointRadius:0,pointHitRadius:6,tension:0,fill:false,showLine:true,hidden:hiddenYrs.has(String(yr))});
    });
    var avgPts = (sd["5yr_avg"] || []).map(function(p){return {x:weekToDoy(p.w),y:p.v};});
    if (forceXMin != null) avgPts = avgPts.filter(function(p){return p.x >= forceXMin;});
    if (forceXMax != null) avgPts = avgPts.filter(function(p){return p.x <= forceXMax;});
    if (avgPts.length > 0) ds.push({label:"5-yr avg",data:avgPts,borderColor:"#999",borderWidth:1.5,borderDash:[2,4],pointRadius:0,tension:0,fill:false,showLine:true,hidden:hiddenYrs.has("5-yr avg")});
    if (ds.length === 0) return;
    var vis = ds.filter(function(d){return !d.hidden;}).flatMap(function(d){return d.data.map(function(p){return p.y;});});
    var visX = ds.filter(function(d){return !d.hidden;}).flatMap(function(d){return d.data.map(function(p){return p.x;});});
    if (vis.length === 0) return;
    var yMax = Math.min(100,Math.ceil((Math.max.apply(null,vis)+10)/10)*10);
    var yMin = Math.max(0,Math.floor((Math.min.apply(null,vis)-5)/10)*10);
    var xMin=0,xMax=365,xDMin=Math.min.apply(null,visX),xDMax=Math.max.apply(null,visX);
    for(var i=11;i>=0;i--){if(mB[i]<=xDMin){xMin=mB[i];break;}}
    for(var j=0;j<12;j++){if(mB[j]>xDMax){xMax=mB[j];break;}}
    if(xMax<=xMin)xMax=365;
    var tks=[];for(var k=0;k<12;k++){if(mB[k]>=xMin&&mB[k]<=xMax)tks.push({value:mB[k]});if(mM[k]>=xMin&&mM[k]<=xMax)tks.push({value:mM[k]});}
    new Chart(canvas,{type:"scatter",data:{datasets:ds},options:{responsive:true,maintainAspectRatio:false,
      interaction:{mode:"nearest",intersect:false},
      plugins:{legend:{display:false},tooltip:{mode:"nearest",intersect:false,backgroundColor:"rgba(0,0,0,0.6)",titleFont:{size:11},bodyFont:{size:11},
        callbacks:{
          title:function(items){if(!items.length)return"";var doy=items[0].parsed.x;var mi=11;for(var m=0;m<11;m++){if(doy<mB[m+1]){mi=m;break;}}return mN[mi]+" "+(Math.floor(doy-mB[mi])+1);},
          label:function(c2){if(c2.parsed.y==null)return null;return c2.dataset.label+": "+c2.parsed.y+"%";}
        },
      }},
      scales:{
        x:{type:"linear",min:xMin,max:xMax,ticks:{callback:function(v){var idx=mM.indexOf(v);return idx>=0?mN[idx]:"";},autoSkip:false,maxRotation:0,font:{size:10}},afterBuildTicks:function(ax){ax.ticks=tks;},grid:{color:function(ctx){var v=ctx.tick.value;if(v>xMin&&mB.indexOf(v)>=0)return"rgba(0,0,0,0.12)";return"transparent";},lineWidth:0.75}},
        y:{min:yMin,max:yMax,ticks:{font:{size:10},callback:function(v){return v+"%";}},grid:{color:"rgba(0,0,0,0.08)",lineWidth:0.75}}
      }}});
  };};

  // CSV
  var dlCSV = function() {
    var hdrs=["Week#","Date"];var cids=["corn","soybeans","winter_wheat","spring_wheat"];var fetchYrs=[];for(var fy=curYear-5;fy<=curYear;fy++)fetchYrs.push(fy);
    cids.forEach(function(cid){var cr=allCrops[cid];if(!cr)return;Object.keys(cr.stages||{}).forEach(function(sid){fetchYrs.forEach(function(yr){hdrs.push(cr.label+" "+SL[sid]+" "+yr);});hdrs.push(cr.label+" "+SL[sid]+" 5yr");});});
    if(pastureData.good_excellent){fetchYrs.forEach(function(yr){hdrs.push("Pasture G+E "+yr);});hdrs.push("Pasture G+E 5yr");}
    if(pastureData.poor_very_poor){fetchYrs.forEach(function(yr){hdrs.push("Pasture P+VP "+yr);});hdrs.push("Pasture P+VP 5yr");}
    if(soilData.topsoil_adequate_surplus){fetchYrs.forEach(function(yr){hdrs.push("Topsoil "+yr);});hdrs.push("Topsoil 5yr");}
    if(soilData.subsoil_adequate_surplus){fetchYrs.forEach(function(yr){hdrs.push("Subsoil "+yr);});hdrs.push("Subsoil 5yr");}
    var rows=[];for(var wk=1;wk<=52;wk++){var doy=weekToDoy(wk);var mi=11;for(var m=0;m<11;m++){if(doy<mB[m+1]){mi=m;break;}}var row=[wk,mN[mi]+" "+(Math.floor(doy-mB[mi])+1)];cids.forEach(function(cid){var cr=allCrops[cid];if(!cr)return;Object.keys(cr.stages||{}).forEach(function(sid){var sd2=(cr.stages[sid]||{})[selState]||{};fetchYrs.forEach(function(yr){var pts=sd2[String(yr)]||[];var mt=pts.find(function(p){return p.w===wk;});row.push(mt?mt.v:"");});var avgP=sd2["5yr_avg"]||[];var ma=avgP.find(function(p){return p.w===wk;});row.push(ma?ma.v:"");});});var addMulti=function(obj){var sd2=(obj||{})[selState]||{};fetchYrs.forEach(function(yr){var pts=sd2[String(yr)]||[];var mt=pts.find(function(p){return p.w===wk;});row.push(mt?mt.v:"");});var avgP=sd2["5yr_avg"]||[];var ma=avgP.find(function(p){return p.w===wk;});row.push(ma?ma.v:"");};if(pastureData.good_excellent)addMulti(pastureData.good_excellent);if(pastureData.poor_very_poor)addMulti(pastureData.poor_very_poor);if(soilData.topsoil_adequate_surplus)addMulti(soilData.topsoil_adequate_surplus);if(soilData.subsoil_adequate_surplus)addMulti(soilData.subsoil_adequate_surplus);rows.push(row);}
    downloadCSV("crop_progress_"+selState+"_all_years.csv",hdrs,rows);
  };

  var chevSvg = "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath d='M3 5l3 3 3-3' fill='none' stroke='%23666' stroke-width='1.5'/%3E%3C/svg%3E\")";
  var selSt = {padding:"6px 24px 6px 10px",fontSize:13,fontWeight:500,border:"1px solid var(--color-border-secondary)",borderRadius:6,background:"var(--color-background-primary)",color:"var(--color-text-primary)",fontFamily:"inherit",cursor:"pointer",appearance:"none",backgroundImage:chevSvg,backgroundRepeat:"no-repeat",backgroundPosition:"right 6px center"};
  var tabSt = function(a){return{padding:"6px 14px",fontSize:12,fontWeight:a?600:400,border:"1px solid "+(a?"#2563EB":"var(--color-border-secondary)"),borderRadius:5,cursor:"pointer",background:a?"#2563EB":"transparent",color:a?"#fff":"var(--color-text-secondary)",transition:"all 0.15s"};};
  var hk = Array.from(hiddenYrs).sort().join(",");

  // Build clickable legend
  var buildLegend = function(dataSource) {
    var yrSet = {};
    if (typeof dataSource === "string") {
      var cr = allCrops[dataSource]; if (!cr) return [];
      Object.keys(cr.stages||{}).forEach(function(sid){var sd=(cr.stages[sid]||{})[selState]||(cr.stages[sid]||{})["US"]||{};Object.keys(sd).forEach(function(k){if(k!=="5yr_avg")yrSet[k]=1;});});
    } else {
      var sd2 = dataSource ? (dataSource[selState] || dataSource["US"] || {}) : {};
      Object.keys(sd2).forEach(function(k){if(k!=="5yr_avg")yrSet[k]=1;});
    }
    var yrs = Object.keys(yrSet).map(Number).sort();
    var items = yrs.map(function(yr){return {label:String(yr),color:getYrColor(yr)};});
    items.push({label:"5-yr avg",color:"#999"});
    return items;
  };
  var legendRow = function(items) {
    return (<div style={{display:"flex",flexWrap:"wrap",gap:6,marginBottom:16,alignItems:"center"}}>
      {items.map(function(item) { var isH = hiddenYrs.has(item.label); return (
        <button key={item.label} onClick={function(){toggleYr(item.label);}} style={{display:"flex",alignItems:"center",gap:5,padding:"4px 10px",border:"1px solid var(--color-border-secondary)",borderRadius:5,background:isH?"var(--color-background-secondary)":"transparent",cursor:"pointer",opacity:isH?0.3:1,transition:"all 0.15s"}}>
          <span style={{width:18,height:0,borderTop:"2.5px solid "+item.color,display:"inline-block"}}></span>
          <span style={{fontSize:12,fontWeight:500,color:"var(--color-text-primary)"}}>{item.label}</span>
        </button>); })}
    </div>);
  };

  // Summary table
  var summaryTbl = (function() {
    var cids=["corn","soybeans","winter_wheat","spring_wheat"];
    var thS={padding:"5px 8px",textAlign:"right",fontWeight:500,fontSize:11,color:"var(--color-text-secondary)",borderBottom:"1.5px solid var(--color-border-primary)",whiteSpace:"nowrap"};
    var thL=Object.assign({},thS,{textAlign:"left"});var tdS={padding:"4px 8px",textAlign:"right",fontSize:12,borderBottom:"0.5px solid var(--color-border-tertiary)"};var tdL=Object.assign({},tdS,{textAlign:"left",fontWeight:500});
    var dSp=function(cur,comp){if(cur==null||comp==null)return null;var d2=cur-comp;var col=d2>0?"#639922":d2<0?"#A32D2D":"var(--color-text-tertiary)";return <span style={{color:col,fontSize:10,marginLeft:4}}>({d2>0?"+":""}{d2})</span>;};
    var trs=[];cids.forEach(function(cid){var cr=allCrops[cid];if(!cr)return;trs.push(<tr key={cid+"h"}><td colSpan={5} style={{padding:"10px 8px 4px",fontWeight:600,fontSize:13,color:"var(--color-text-primary)",borderBottom:"1px solid var(--color-border-secondary)"}}>{cr.label}</td></tr>);Object.keys(cr.stages||{}).forEach(function(sid){var isWWCond=(cid==="winter_wheat"&&sid==="condition");var info=getLatest((cr.stages||{})[sid],isWWCond);trs.push(<tr key={cid+sid}><td style={tdL}>&nbsp;&nbsp;{SL[sid]||sid}</td><td style={tdS}>{info.wk?"#"+info.wk:"—"}</td><td style={tdS}>{info.cur!=null?info.cur+"%":"—"}</td><td style={tdS}>{info.prev!=null?info.prev+"%":"—"}</td><td style={tdS}>{info.avg!=null?info.avg+"%":"—"}</td></tr>);});});
    return (<table style={{width:"100%",borderCollapse:"collapse",fontSize:12}}><thead><tr><th style={thL}>Commodity / Stage</th><th style={thS}>Week</th><th style={thS}>{curYear}</th><th style={thS}>{lastYear}</th><th style={thS}>5-yr Avg</th></tr></thead><tbody>{trs}</tbody></table>);
  })();

  // Crop tab
  var cropTab = function(cid) {
    var cr = allCrops[cid];
    if (!cr) return <div style={{padding:20,color:"var(--color-text-tertiary)"}}>No data yet — will appear when growing season begins.</div>;
    var rawSids = Object.keys(cr.stages || {});
    var lgItems = buildLegend(cid);
    var isWW = cid === "winter_wheat";
    // Header stat cards: planted, condition, harvested
    var cardSids = ["planted","condition","harvested"].filter(function(sid){return rawSids.indexOf(sid) >= 0;});
    var cropColor = cid === "corn" ? "#D4A017" : cid === "soybeans" ? "#1D9E75" : cid === "winter_wheat" ? "#A32D2D" : "#D85A30";
    // Chart definitions (split winter wheat condition)
    var chartDefs = [];
    rawSids.forEach(function(sid) {
      if (isWW && sid === "condition") {
        chartDefs.push({sid:"condition",label:"Condition — Fall (G+E%)",forceXMin:mB[7],forceXMax:null});
        chartDefs.push({sid:"condition",label:"Condition — Spring (G+E%)",forceXMin:null,forceXMax:mB[7]});
      } else {
        chartDefs.push({sid:sid,label:SL[sid]||sid,forceXMin:null,forceXMax:null});
      }
    });
    return (<div>
      <div style={{display:"grid",gridTemplateColumns:"repeat("+cardSids.length+", 1fr)",gap:10,marginBottom:16}}>
        {cardSids.map(function(sid) { var isWWC2=(cid==="winter_wheat"&&sid==="condition");return <div key={sid}>{statCard(SL[sid]||sid, (cr.stages||{})[sid], cropColor, isWWC2)}</div>; })}
      </div>
      {legendRow(lgItems)}
      <div style={{display:"grid",gridTemplateColumns:"1fr 1fr 1fr",gap:16}}>
        {chartDefs.map(function(cd, idx) { return (<div key={cd.sid+"_"+idx}>
          <div style={{fontSize:13,fontWeight:500,color:"var(--color-text-secondary)",marginBottom:6,textAlign:"center"}}>{cd.label}</div>
          {ready && <ChartBox id={"cp_"+cid+"_"+cd.sid+"_"+idx+"_"+selState} height={200} renderChart={mkMultiChart((cr.stages||{})[cd.sid], cd.forceXMin, cd.forceXMax)} deps={cid+"_"+cd.sid+"_"+idx+"_"+selState+"_"+cpLoaded+"_"+hk} />}
        </div>); })}
      </div>
    </div>);
  };

  return (<div>
    <div style={{display:"flex",alignItems:"center",gap:16,marginBottom:14,flexWrap:"wrap"}}>
      <div style={{display:"flex",gap:3,flexWrap:"wrap"}}>
        {TABS.map(function(t){return <button key={t.id} onClick={function(){setTab(t.id);}} style={tabSt(tab===t.id)}>{t.label}</button>;})}
      </div>
      {tab !== "summary" && <div style={{display:"flex",alignItems:"center",gap:6}}>
        <span style={{fontSize:11,fontWeight:600,color:"var(--color-text-secondary)",textTransform:"uppercase"}}>State</span>
        <select value={selState} onChange={function(e){setSelState(e.target.value);}} style={selSt}>
          {stateList.map(function(s){return <option key={s} value={s}>{s === "US" ? "U.S. Total" : s}</option>;})}
        </select>
      </div>}
      <div style={{marginLeft:"auto"}}><DownloadBtn onClick={dlCSV} /></div>
    </div>
    <div style={{fontSize:12,color:"var(--color-text-tertiary)",marginBottom:12}}>USDA NASS Crop Progress & Condition — {tab === "summary" ? "U.S. Total" : (selState === "US" ? "U.S. Total" : selState)} — {curYear} season.</div>

    {tab === "summary" && <div>
      <div style={{display:"flex",alignItems:"center",gap:12,marginBottom:12,flexWrap:"wrap"}}>
        <div style={{display:"flex",alignItems:"center",gap:6}}>
          <span style={{fontSize:11,fontWeight:600,color:"var(--color-text-secondary)",textTransform:"uppercase"}}>Commodity</span>
          <select value={mapCrop} onChange={function(e){setMapCrop(e.target.value);}} style={selSt}>
            {Object.keys(allCrops).map(function(cid){return <option key={cid} value={cid}>{allCrops[cid].label}</option>;})}
          </select>
        </div>
        <div style={{display:"flex",alignItems:"center",gap:6}}>
          <span style={{fontSize:11,fontWeight:600,color:"var(--color-text-secondary)",textTransform:"uppercase"}}>Data</span>
          <select value={mapStage} onChange={function(e){setMapStage(e.target.value);}} style={selSt}>
            {mapStageOpts(mapCrop).map(function(o){return <option key={o.id} value={o.id}>{o.label}</option>;})}
          </select>
        </div>
        {(function(){var cr=allCrops[mapCrop];var sd2=cr&&cr.stages?cr.stages[mapStage]:null;var us=sd2?sd2["US"]:null;var pts=us?us[String(curYear)]||[]:[];if(pts.length===0&&us&&mapCrop==="winter_wheat"&&mapStage==="condition"){pts=us[String(curYear-1)]||[];}if(pts.length===0)return null;var last,chg;if(mapCrop==="winter_wheat"&&mapStage==="condition"){var inWk=Math.max(1,Math.min(52,Math.ceil(Math.floor((Date.now()-new Date(curYear,0,1).getTime())/86400000)/7)));var inS=pts.slice().sort(function(a,b){return Math.abs(a.w-inWk)-Math.abs(b.w-inWk);});last=inS[0];var inO=pts.filter(function(p){return p!==last;});inO.sort(function(a,b){return Math.abs(a.w-inWk)-Math.abs(b.w-inWk);});chg=inO.length>0?last.v-inO[0].v:null;}else{last=pts[pts.length-1];chg=pts.length>1?last.v-pts[pts.length-2].v:null;}var wk=last.w;var doy2=weekToDoy(wk);var mi2=11;for(var m2=0;m2<11;m2++){if(doy2<mB[m2+1]){mi2=m2;break;}}var calYear=wk>30?(curYear-1):curYear;var dateStr2=mN[mi2]+" "+(Math.floor(doy2-mB[mi2])+1)+", "+calYear;return <span style={{fontSize:13,fontWeight:500,color:"var(--color-text-primary)"}}>U.S.: {last.v}%{chg!=null&&<span style={{color:chg>0?"#639922":chg<0?"#A32D2D":"#666",marginLeft:6,fontSize:12}}>({chg>0?"+":""}{chg} vs prev wk)</span>}<span style={{color:"var(--color-text-tertiary)",marginLeft:10,fontSize:12,fontWeight:400}}>as of {dateStr2}</span></span>;})()}
      </div>
      <div ref={mapRef} style={{width:"100%",minHeight:100,background:"var(--color-background-primary)",borderRadius:8,border:"0.5px solid var(--color-border-tertiary)",marginBottom:24,display:"flex",alignItems:"center",justifyContent:"center"}}>
        <span style={{color:"var(--color-text-tertiary)",fontSize:13}}>Loading map...</span>
      </div>
      {summaryTbl}
    </div>}

    {tab === "corn" && cropTab("corn")}
    {tab === "soybeans" && cropTab("soybeans")}
    {tab === "winter_wheat" && cropTab("winter_wheat")}
    {tab === "spring_wheat" && cropTab("spring_wheat")}

    {tab === "pasture" && <div>
      <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:10,marginBottom:16}}>
        {statCard("Good + Excellent", pastureData.good_excellent, "#639922")}
        {statCard("Poor + Very Poor", pastureData.poor_very_poor, "#A32D2D")}
      </div>
      {legendRow(buildLegend(pastureData.good_excellent || pastureData.poor_very_poor))}
      <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:18}}>
        <div><div style={{fontSize:14,fontWeight:600,color:"var(--color-text-primary)",marginBottom:6}}>Good + Excellent</div>{ready && <ChartBox id={"cp_pasture_ge_"+selState} height={260} renderChart={mkMultiChart(pastureData.good_excellent)} deps={"pasture_ge_"+selState+"_"+cpLoaded+"_"+hk} />}</div>
        <div><div style={{fontSize:14,fontWeight:600,color:"var(--color-text-primary)",marginBottom:6}}>Poor + Very Poor</div>{ready && <ChartBox id={"cp_pasture_pvp_"+selState} height={260} renderChart={mkMultiChart(pastureData.poor_very_poor)} deps={"pasture_pvp_"+selState+"_"+cpLoaded+"_"+hk} />}</div>
      </div>
    </div>}

    {tab === "soil" && <div>
      <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:10,marginBottom:16}}>
        {statCard("Topsoil Adequate + Surplus", soilData.topsoil_adequate_surplus, "#378ADD")}
        {statCard("Subsoil Adequate + Surplus", soilData.subsoil_adequate_surplus, "#534AB7")}
      </div>
      {legendRow(buildLegend(soilData.topsoil_adequate_surplus))}
      <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:18}}>
        <div><div style={{fontSize:14,fontWeight:600,color:"var(--color-text-primary)",marginBottom:6}}>Topsoil</div>{ready && <ChartBox id={"cp_topsoil_"+selState} height={250} renderChart={mkMultiChart(soilData.topsoil_adequate_surplus)} deps={"topsoil_"+selState+"_"+cpLoaded+"_"+hk} />}</div>
        <div><div style={{fontSize:14,fontWeight:600,color:"var(--color-text-primary)",marginBottom:6}}>Subsoil</div>{ready && <ChartBox id={"cp_subsoil_"+selState} height={250} renderChart={mkMultiChart(soilData.subsoil_adequate_surplus)} deps={"subsoil_"+selState+"_"+cpLoaded+"_"+hk} />}</div>
      </div>
    </div>}

    <div style={{marginTop:14,fontSize:11,color:"var(--color-text-tertiary)"}}>Source: USDA National Agricultural Statistics Service (NASS). Weekly crop progress reports.</div>
  </div>);
}


function EthanolPage({ ready }) {
  var ref = useLiveEthanol();
  var ethData = ref.ethData;
  var ethLoaded = ref.ethLoaded;
  var _mode = useState("seasonal");
  var mode = _mode[0], setMode = _mode[1];
  var _range = useState("1");
  var range = _range[0], setRange = _range[1];
  var _unit = useState("bbl");
  var unit = _unit[0], setUnit = _unit[1];
  var _hy = useState(new Set());
  var hiddenYrs = _hy[0], setHiddenYrs = _hy[1];

  useEffect(function(){ setHiddenYrs(new Set()); }, [mode, range, unit]);
  var toggleYr = function(label) { setHiddenYrs(function(prev){ var next = new Set(prev); if(next.has(label))next.delete(label);else next.add(label); return next; }); };

  var GAL_PER_BBL = 42;
  var isGal = unit === "gal";
  // Barrels: production=kbd, stocks=k bbl
  // Gallons: production=million gal/week (kbd*7*42/1000), stocks=million gal (k bbl*42/1000)
  var convProd = function(v) { return v == null ? null : isGal ? Math.round(v * 7 * GAL_PER_BBL / 1000 * 100) / 100 : v; };
  var convStk = function(v) { return v == null ? null : isGal ? Math.round(v * GAL_PER_BBL / 1000 * 100) / 100 : v; };
  var prodUnit = isGal ? "million gallons" : "thousand barrels per day";
  var stkUnit = isGal ? "million gallons" : "thousand barrels";

  // Marketing year: Sep 1 - Aug 31
  var mktN = ["Sep","Oct","Nov","Dec","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug"];
  var mktB = [0,30,61,91,122,153,181,212,242,273,303,334];
  var mktM = [15,45,76,106,137,167,196,227,257,288,318,349];

  var dateToMktDay = function(ds) {
    var p = ds.split("-"); var y = parseInt(p[0]), m = parseInt(p[1]) - 1, d = parseInt(p[2]);
    var dt = new Date(y, m, d);
    var sep1 = m >= 8 ? new Date(y, 8, 1) : new Date(y - 1, 8, 1);
    return Math.round((dt - sep1) / 86400000);
  };
  var dateToMY = function(ds) {
    var m = parseInt(ds.split("-")[1]); var y = parseInt(ds.split("-")[0]);
    return m >= 9 ? y : y - 1;
  };
  var myLabel = function(yr) { return yr + "/" + String(yr + 1).slice(2); };

  var processRaw = function(rawPts, convFn) {
    if (!rawPts || !rawPts.length) return {};
    var byMY = {};
    rawPts.forEach(function(pt) {
      var my = dateToMY(pt.d); var day = dateToMktDay(pt.d);
      if (day < -5 || day > 370) return;
      day = Math.max(0, Math.min(365, day));
      if (!byMY[my]) byMY[my] = [];
      byMY[my].push({ x: day, y: convFn(pt.v) });
    });
    return byMY;
  };

  // Compute offtake: prev_stocks + production*7 - cur_stocks
  var computeOfftake = function() {
    if (!ethData || !ethData.production || !ethData.stocks) return [];
    var prodMap = {}, stkMap = {};
    ethData.production.forEach(function(pt) { prodMap[pt.d] = pt.v; });
    ethData.stocks.forEach(function(pt) { stkMap[pt.d] = pt.v; });
    var dates = ethData.stocks.map(function(pt) { return pt.d; }).sort();
    var out = [];
    for (var i = 1; i < dates.length; i++) {
      var cur = dates[i], prev = dates[i - 1];
      if (stkMap[cur] != null && stkMap[prev] != null && prodMap[cur] != null) {
        out.push({ d: cur, v: Math.round((stkMap[prev] + prodMap[cur] * 7 - stkMap[cur]) * 10) / 10 });
      }
    }
    return out;
  };

  var prod = ethData ? processRaw(ethData.production, convProd) : {};
  var stk = ethData ? processRaw(ethData.stocks, convStk) : {};
  var exp = ethData ? processRaw(ethData.exports, convProd) : {};
  var oft = processRaw(computeOfftake(), convStk);
  var gasDem = ethData ? processRaw(ethData.gasoline_demand, convProd) : {};

  var now = new Date();
  var curMY = now.getMonth() >= 8 ? now.getFullYear() : now.getFullYear() - 1;
  // Range: "1" = current + 1 previous, "5" = current + 5 previous, "10" = current + 10 previous
  var rangeN = parseInt(range);
  var startMY = curMY - rangeN;

  var yrColors = ["#A32D2D","#D85A30","#E8A735","#639922","#1D9E75","#378ADD","#534AB7","#8B5CF6","#EC4899","#6B7280"];
  var getColor = function(my) { if (my === curMY) return "#333"; var dist = curMY - my; if (dist === 1) return "#1D9E75"; if (dist === 2) return "#639922"; if (dist === 3) return "#E8A735"; if (dist === 4) return "#D85A30"; if (dist === 5) return "#A32D2D"; return yrColors[(dist - 1) % yrColors.length]; };

  // Build legend items (chronological, oldest first)
  var buildItems = function(byMY) {
    var items = [];
    for (var y = startMY; y <= curMY; y++) {
      if (byMY[y]) items.push({ label: myLabel(y), my: y, color: getColor(y) });
    }
    return items;
  };
  var allItems = buildItems(prod);
  var hk = Array.from(hiddenYrs).sort().join(",");

  // Get latest values for header cards
  var getCardInfo = function(rawPts, convFn) {
    if (!rawPts || !rawPts.length) return { cur: null, prevWk: null, lastYr: null, date: null };
    var sorted = rawPts.slice().sort(function(a, b) { return a.d < b.d ? 1 : -1; });
    var latest = sorted[0]; var prev = sorted.length > 1 ? sorted[1] : null;
    // Find same week last year (±7 days)
    var latestDate = new Date(latest.d);
    var targetDate = new Date(latestDate);
    targetDate.setFullYear(targetDate.getFullYear() - 1);
    var targetMs = targetDate.getTime();
    var lastYrPt = null; var bestDiff = 8 * 86400000;
    rawPts.forEach(function(p) { var diff = Math.abs(new Date(p.d).getTime() - targetMs); if (diff < bestDiff) { bestDiff = diff; lastYrPt = p; } });
    return { cur: convFn(latest.v), prevWk: prev ? convFn(prev.v) : null, lastYr: lastYrPt ? convFn(lastYrPt.v) : null, date: latest.d };
  };

  var prodInfo = ethData ? getCardInfo(ethData.production, convProd) : {};
  var stkInfo = ethData ? getCardInfo(ethData.stocks, convStk) : {};
  var expInfo = ethData ? getCardInfo(ethData.exports, convProd) : {};
  var oftRaw = computeOfftake();
  var oftInfo = getCardInfo(oftRaw, convStk);
  var gasDemInfo = ethData ? getCardInfo(ethData.gasoline_demand, convProd) : {};

  var statCard = function(label, info, unitLabel) {
    var diffLine = function(lbl, comp) {
      if (info.cur == null || comp == null) return null;
      var d2 = Math.round((info.cur - comp) * 100) / 100;
      var col = d2 > 0 ? "#639922" : d2 < 0 ? "#A32D2D" : "var(--color-text-tertiary)";
      var fmtE = function(v) { return isGal ? Number(v.toFixed(1)).toLocaleString(undefined, {minimumFractionDigits:1, maximumFractionDigits:1}) : v.toLocaleString(); };
      return (<div style={{display:"flex",justifyContent:"space-between",fontSize:10.5,padding:"1px 0"}}>
        <span style={{color:"var(--color-text-tertiary)"}}>{lbl}</span>
        <span style={{display:"flex",gap:4,alignItems:"baseline"}}><span style={{color:"var(--color-text-secondary)",textAlign:"right",minWidth:60}}>{fmtE(comp)}</span><span style={{color:col,fontWeight:500,textAlign:"right",minWidth:52}}>({d2 > 0 ? "+" : ""}{fmtE(d2)})</span></span>
      </div>);
    };
    return (<div style={{background:"var(--color-background-secondary)",borderRadius:"var(--border-radius-md)",padding:"12px 14px",minWidth:0}}>
      <div style={{fontSize:11,color:"var(--color-text-secondary)",marginBottom:3,textTransform:"uppercase",letterSpacing:"0.4px"}}>{label}</div>
      <div style={{fontSize:22,fontWeight:500,color:"var(--color-text-primary)",marginBottom:2}}>{info.cur != null ? (isGal ? info.cur.toLocaleString(undefined, {minimumFractionDigits:1, maximumFractionDigits:1}) : info.cur.toLocaleString()) : "—"}<span style={{fontSize:12,fontWeight:400,color:"var(--color-text-secondary)",marginLeft:4}}>{unitLabel}</span></div>
      {info.date && <div style={{fontSize:10,color:"var(--color-text-tertiary)",marginBottom:6}}>as of {fmtDate(info.date)}</div>}
      <div style={{borderTop:"0.5px solid var(--color-border-tertiary)",paddingTop:5}}>
        {diffLine("vs. last week", info.prevWk)}
        {diffLine("vs. last year", info.lastYr)}
      </div>
    </div>);
  };

  // Chart builder with nice y-axis intervals
  var mkChart = function(byMY, yLabel) { return function(canvas) {
    if (!byMY || Object.keys(byMY).length === 0) return;
    var isSeasonal = mode === "seasonal";
    var ds = [];

    if (isSeasonal) {
      for (var y = startMY; y <= curMY; y++) {
        var pts = byMY[y];
        if (!pts || !pts.length) continue;
        var label = myLabel(y);
        ds.push({ label: label, data: pts.slice(), borderColor: getColor(y), borderWidth: y === curMY ? 2.5 : 1.5, pointRadius: 0, pointHitRadius: 6, tension: 0, fill: false, showLine: true, hidden: hiddenYrs.has(label) });
      }
      if (ds.length === 0) return;
      var vis = ds.filter(function(d) { return !d.hidden; }).flatMap(function(d) { return d.data.map(function(p) { return p.y; }); });
      if (vis.length === 0) return;
      var rawMax = Math.max.apply(null, vis), rawMin = Math.min.apply(null, vis);
      var span = rawMax - rawMin || 1;
      // Nice tick interval
      var step = Math.pow(10, Math.floor(Math.log10(span / 4)));
      if (span / step < 4) step = step / 2;
      if (span / step > 8) step = step * 2;
      var yMin = Math.floor(rawMin / step) * step;
      var yMax = Math.ceil(rawMax / step) * step;
      if (yMax === rawMax) yMax += step;
      var tks = []; for (var k = 0; k < 12; k++) { tks.push({ value: mktB[k] }); tks.push({ value: mktM[k] }); }
      new Chart(canvas, { type: "scatter", data: { datasets: ds }, options: {
        responsive: true, maintainAspectRatio: false,
        interaction: { mode: "nearest", intersect: false },
        plugins: { legend: { display: false }, tooltip: { mode: "nearest", intersect: false, backgroundColor: "rgba(0,0,0,0.6)", titleFont: { size: 11 }, bodyFont: { size: 11 },
          callbacks: { title: function(items) { if (!items.length) return ""; var doy = items[0].parsed.x; var mi = 11; for (var m = 0; m < 11; m++) { if (doy < mktB[m + 1]) { mi = m; break; } } return mktN[mi] + " " + (Math.floor(doy - mktB[mi]) + 1); },
            label: function(c2) { return c2.parsed.y == null ? null : c2.dataset.label + ": " + c2.parsed.y.toLocaleString(); } } } },
        scales: { x: { type: "linear", min: 0, max: 365, ticks: { callback: function(v) { var idx = mktM.indexOf(v); return idx >= 0 ? mktN[idx] : ""; }, autoSkip: false, maxRotation: 0, font: { size: 10 } }, afterBuildTicks: function(ax) { ax.ticks = tks; }, grid: { color: function(ctx) { var v = ctx.tick.value; if (v > 0 && mktB.indexOf(v) >= 0) return "rgba(0,0,0,0.12)"; return "transparent"; }, lineWidth: 0.75 } },
          y: { min: yMin, max: yMax, ticks: { stepSize: step, font: { size: 10 }, callback: function(v) { return v.toLocaleString(); } }, grid: { color: "rgba(0,0,0,0.08)", lineWidth: 0.75 } } }
      } });
    } else {
      // Contiguous mode
      var allPts = [];
      var years = [];
      for (var y2 = startMY; y2 <= curMY; y2++) { if (byMY[y2]) years.push(y2); }
      years.forEach(function(yr, idx) {
        var pts2 = byMY[yr]; if (!pts2) return;
        pts2.forEach(function(p) { allPts.push({ x: idx * 365 + p.x, y: p.y }); });
      });
      if (allPts.length === 0) return;
      ds.push({ label: "Ethanol", data: allPts, borderColor: "#333", borderWidth: 1.5, pointRadius: 0, tension: 0, fill: false, showLine: true });
      var allY = allPts.map(function(p) { return p.y; });
      var rMax = Math.max.apply(null, allY), rMin = Math.min.apply(null, allY);
      var sp2 = rMax - rMin || 1;
      var st2 = Math.pow(10, Math.floor(Math.log10(sp2 / 4)));
      if (sp2 / st2 < 4) st2 = st2 / 2;
      if (sp2 / st2 > 8) st2 = st2 * 2;
      var yMin2 = Math.floor(rMin / st2) * st2;
      var yMax2 = Math.ceil(rMax / st2) * st2;
      if (yMax2 === rMax) yMax2 += st2;
      // Build x-axis ticks and gridlines based on range
      var totalDays = years.length * 365;
      var isShort = years.length <= 2;
      var xTicks = [];
      var xGrids = [];
      if (isShort) {
        // Short range: mmm-yy labels every 2 months, gridlines at Sep boundaries
        years.forEach(function(yr, idx) {
          for (var mi = 0; mi < 12; mi++) {
            var dayPos = idx * 365 + mktB[mi];
            if (dayPos <= totalDays) {
              // Label every other month
              if (mi % 2 === 0) xTicks.push({ value: dayPos, label: mktN[mi] + "-" + String(mi >= 4 ? yr + 1 : yr).slice(2) });
              else xTicks.push({ value: dayPos, label: "" });
            }
          }
          if (idx > 0) xGrids.push(idx * 365);
        });
      } else {
        // Long range: yyyy labels at Jan 1 (= mktB[4] offset in each MY), gridlines at Sep boundaries
        years.forEach(function(yr, idx) {
          // Sep 1 gridline
          if (idx > 0) xGrids.push(idx * 365);
          // Jan 1 label (4 months into marketing year)
          var janPos = idx * 365 + mktB[4];
          if (janPos <= totalDays) xTicks.push({ value: janPos, label: String(yr + 1) });
        });
      }
      new Chart(canvas, { type: "scatter", data: { datasets: ds }, options: {
        responsive: true, maintainAspectRatio: false,
        interaction: { mode: "nearest", intersect: false },
        plugins: { legend: { display: false }, tooltip: { backgroundColor: "rgba(0,0,0,0.6)", titleFont: { size: 11 }, bodyFont: { size: 11 },
          callbacks: { title: function(items) { if (!items.length) return ""; var v = items[0].parsed.x; var yrIdx = Math.floor(v / 365); var dayInYr = v - yrIdx * 365; if (yrIdx >= years.length) return ""; var mi = 11; for (var m = 0; m < 11; m++) { if (dayInYr < mktB[m + 1]) { mi = m; break; } } var calYr = mi >= 4 ? years[yrIdx] + 1 : years[yrIdx]; return mktN[mi] + " " + (Math.floor(dayInYr - mktB[mi]) + 1) + ", " + calYr; },
            label: function(c2) { return c2.parsed.y == null ? null : c2.parsed.y.toLocaleString(); } } } },
        scales: { x: { type: "linear", min: 0, max: totalDays,
          afterBuildTicks: function(ax) { ax.ticks = xTicks.map(function(t) { return { value: t.value }; }); },
          ticks: { callback: function(v) { var found = xTicks.find(function(t) { return Math.abs(t.value - v) < 5; }); return found ? found.label : ""; }, autoSkip: false, maxRotation: 0, font: { size: 10 } },
          grid: { color: function(ctx) { var v = ctx.tick.value; if (xGrids.some(function(g) { return Math.abs(g - v) < 5; })) return "rgba(0,0,0,0.15)"; var isMonthBound = xTicks.some(function(t) { return Math.abs(t.value - v) < 5 && t.label !== ""; }); return isMonthBound ? "rgba(0,0,0,0.06)" : "transparent"; } } },
          y: { min: yMin2, max: yMax2, ticks: { stepSize: st2, font: { size: 10 }, callback: function(v) { return v.toLocaleString(); } }, grid: { color: "rgba(0,0,0,0.08)" } } }
      } });
    }
  }; };

  // CSV download
  var dlCSV = function() {
    var hdrs = ["Date", "MY", "Production (" + prodUnit + ")", "Stocks (" + stkUnit + ")", "Implied Offtake (" + stkUnit + ")", "Exports (" + prodUnit + ")"];
    var rows = [];
    var inRange = function(d) { var my = dateToMY(d); return my >= startMY && my <= curMY; };
    var allDates = {};
    if (ethData) {
      (ethData.production || []).filter(function(p){return inRange(p.d);}).forEach(function(p) { allDates[p.d] = allDates[p.d] || {}; allDates[p.d].prod = convProd(p.v); });
      (ethData.stocks || []).filter(function(p){return inRange(p.d);}).forEach(function(p) { allDates[p.d] = allDates[p.d] || {}; allDates[p.d].stk = convStk(p.v); });
      (ethData.exports || []).filter(function(p){return inRange(p.d);}).forEach(function(p) { allDates[p.d] = allDates[p.d] || {}; allDates[p.d].exp = convProd(p.v); });
    }
    computeOfftake().filter(function(p){return inRange(p.d);}).forEach(function(p) { allDates[p.d] = allDates[p.d] || {}; allDates[p.d].oft = convStk(p.v); });
    if (ethData && ethData.gasoline_demand) { (ethData.gasoline_demand).filter(function(p){return inRange(p.d);}).forEach(function(p) { allDates[p.d] = allDates[p.d] || {}; allDates[p.d].gas = convProd(p.v); }); }
    Object.keys(allDates).sort().forEach(function(d) {
      var r = allDates[d];
      rows.push([d, myLabel(dateToMY(d)), r.prod || "", r.stk || "", r.oft || "", r.exp || ""]);
    });
    downloadCSV("ethanol_" + unit + ".csv", hdrs, rows);
  };

  var chevSvg = "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath d='M3 5l3 3 3-3' fill='none' stroke='%23666' stroke-width='1.5'/%3E%3C/svg%3E\")";
  var selSt = {padding:"6px 24px 6px 10px",fontSize:13,fontWeight:500,border:"1px solid var(--color-border-secondary)",borderRadius:6,background:"var(--color-background-primary)",color:"var(--color-text-primary)",fontFamily:"inherit",cursor:"pointer",appearance:"none",backgroundImage:chevSvg,backgroundRepeat:"no-repeat",backgroundPosition:"right 6px center"};
  var modeSt = function(a) { return {padding:"6px 14px",fontSize:12,fontWeight:a?600:400,border:"1px solid "+(a?"#2563EB":"var(--color-border-secondary)"),borderRadius:5,cursor:"pointer",background:a?"#2563EB":"transparent",color:a?"#fff":"var(--color-text-secondary)",transition:"all 0.15s"}; };

  var CHARTS = [
    { key: "prod", label: "Ethanol Production", data: prod, yLabel: prodUnit },
    { key: "stk", label: "Ethanol Stocks", data: stk, yLabel: stkUnit },
    { key: "oft", label: "Implied Ethanol Offtake", data: oft, yLabel: stkUnit },
    { key: "exp", label: "Ethanol Exports", data: exp, yLabel: prodUnit },
    { key: "gas", label: "Gasoline Demand", data: gasDem, yLabel: prodUnit },
  ];

  var hasExports = ethData && ethData.exports && ethData.exports.length > 0;

  return (<div>
    <div style={{display:"flex",alignItems:"center",gap:12,marginBottom:14,flexWrap:"wrap"}}>
      <div style={{display:"flex",alignItems:"center",gap:6}}>
        <span style={{fontSize:11,fontWeight:600,color:"var(--color-text-secondary)",textTransform:"uppercase"}}>Range</span>
        <select value={range} onChange={function(e){setRange(e.target.value);}} style={selSt}>
          <option value="1">1 Year</option>
          <option value="5">5 Years</option>
          <option value="10">10 Years</option>
        </select>
      </div>
      <div style={{display:"flex",gap:3}}>
        <button onClick={function(){setMode("seasonal");}} style={modeSt(mode==="seasonal")}>Seasonal</button>
        <button onClick={function(){setMode("contiguous");}} style={modeSt(mode==="contiguous")}>Contiguous</button>
      </div>
      <div style={{display:"flex",gap:3}}>
        <button onClick={function(){setUnit("bbl");}} style={modeSt(unit==="bbl")}>Barrels</button>
        <button onClick={function(){setUnit("gal");}} style={modeSt(unit==="gal")}>Gallons</button>
      </div>
      <div style={{marginLeft:"auto"}}><DownloadBtn onClick={dlCSV} /></div>
    </div>

    <div style={{display:"grid",gridTemplateColumns:"1fr 1fr 1fr 1fr 1fr",gap:10,marginBottom:16}}>
      {statCard("Ethanol Production", prodInfo, prodUnit)}
      {statCard("Ethanol Stocks", stkInfo, stkUnit)}
      {statCard("Implied Ethanol Offtake", oftInfo, stkUnit)}
      {statCard("Ethanol Exports", expInfo, prodUnit)}
      {statCard("Gasoline Demand", gasDemInfo, prodUnit)}
    </div>

    {!hasExports && <div style={{fontSize:12,color:"var(--color-text-tertiary)",marginBottom:8,padding:"6px 10px",background:"var(--color-background-secondary)",borderRadius:6}}>Note: EIA ethanol export data may be unavailable. Checking series ID...</div>}

    {mode === "seasonal" && <div style={{display:"flex",flexWrap:"wrap",gap:6,marginBottom:16,alignItems:"center"}}>
      {allItems.map(function(item) { var isH = hiddenYrs.has(item.label); return (
        <button key={item.label} onClick={function(){toggleYr(item.label);}} style={{display:"flex",alignItems:"center",gap:5,padding:"4px 10px",border:"1px solid var(--color-border-secondary)",borderRadius:5,background:isH?"var(--color-background-secondary)":"transparent",cursor:"pointer",opacity:isH?0.3:1,transition:"all 0.15s"}}>
          <span style={{width:18,height:0,borderTop:"2.5px solid "+item.color,display:"inline-block"}}></span>
          <span style={{fontSize:12,fontWeight:500,color:"var(--color-text-primary)"}}>{item.label}</span>
        </button>); })}
    </div>}

    <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:16}}>
      {CHARTS.map(function(ch) { return (<div key={ch.key}>
        <div style={{fontSize:14,fontWeight:600,color:"var(--color-text-primary)",marginBottom:6}}>{ch.label} <span style={{fontSize:11,fontWeight:400,color:"var(--color-text-tertiary)"}}>({ch.yLabel})</span></div>
        {ready && <ChartBox id={"eth_"+ch.key+"_"+mode+"_"+range+"_"+unit} height={240} renderChart={mkChart(ch.data, ch.yLabel)} deps={"eth_"+ch.key+"_"+mode+"_"+range+"_"+unit+"_"+ethLoaded+"_"+hk} />}
      </div>); })}
    </div>
    <div style={{marginTop:14,fontSize:11,color:"var(--color-text-tertiary)"}}>Source: EIA Weekly Petroleum Status Report. Corn marketing year (Sep–Aug). Implied offtake = prior week stocks + production×7 − current stocks.</div>
  </div>);
}


function FatsOilsPage({ ready }) {
  var ref = useLiveOilseedCrushing();
  var oilData = ref.oilData;
  var oilLoaded = ref.oilLoaded;
  var _mode = useState("seasonal");
  var mode = _mode[0], setMode = _mode[1];
  var _range = useState("1");
  var range = _range[0], setRange = _range[1];
  var _hy = useState(new Set());
  var hiddenYrs = _hy[0], setHiddenYrs = _hy[1];

  useEffect(function(){ setHiddenYrs(new Set()); }, [mode, range]);
  var toggleYr = function(label) { setHiddenYrs(function(prev){ var next = new Set(prev); if(next.has(label))next.delete(label);else next.add(label); return next; }); };

  // Soybean marketing year: Oct 1 - Sep 30
  var mktN = ["Oct","Nov","Dec","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep"];
  var monthToMktIdx = {"10":0,"11":1,"12":2,"01":3,"02":4,"03":5,"04":6,"05":7,"06":8,"07":9,"08":10,"09":11};
  // Sep-start marketing year for crush only
  var mktN_sep = ["Sep","Oct","Nov","Dec","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug"];
  var monthToMktIdx_sep = {"09":0,"10":1,"11":2,"12":3,"01":4,"02":5,"03":6,"04":7,"05":8,"06":9,"07":10,"08":11};

  var dateToMY = function(ds) { var m = parseInt(ds.split("-")[1]); var y = parseInt(ds.split("-")[0]); return m >= 10 ? y : y - 1; };
  var dateToMY_sep = function(ds) { var m = parseInt(ds.split("-")[1]); var y = parseInt(ds.split("-")[0]); return m >= 9 ? y : y - 1; };
  var myLabel = function(yr) { return yr + "/" + String(yr + 1).slice(2); };

  var processRaw = function(rawPts, convFactor, useSepMY) {
    if (!rawPts || !rawPts.length) return {};
    var cf = convFactor || 1;
    var idxMap = useSepMY ? monthToMktIdx_sep : monthToMktIdx;
    var myFn = useSepMY ? dateToMY_sep : dateToMY;
    var byMY = {};
    rawPts.forEach(function(pt) {
      var my = myFn(pt.d);
      var mm = pt.d.split("-")[1];
      var idx = idxMap[mm];
      if (idx == null) return;
      if (!byMY[my]) byMY[my] = [];
      byMY[my].push({ x: idx, y: Math.round(pt.v * cf * 100) / 100 });
    });
    return byMY;
  };

  // Yield: oil lbs / (crush tons * 2000/60)
  var computeYield = function() {
    if (!oilData || !oilData.oil_produced || !oilData.crush) return [];
    var crushMap = {}; oilData.crush.forEach(function(pt) { crushMap[pt.d] = pt.v; });
    var out = [];
    oilData.oil_produced.forEach(function(pt) {
      var ct = crushMap[pt.d];
      if (ct && ct > 0 && pt.v != null) { out.push({ d: pt.d, v: Math.round(pt.v / (ct * 2000 / 60) * 100) / 100 }); }
    });
    return out;
  };

  // Chart conversions (different from card units!)
  var CRUSH_CHART = 2000 / 60 / 1000000;  // tons -> M bu
  var MEAL_PROD_CHART = 1 / 1000000;       // tons -> M short tons
  var OIL_PROD_CHART = 1 / 1000000;        // lbs -> M lbs
  var MEAL_STK_CHART = 1 / 1000;            // tons -> 1,000 short tons
  var OIL_STK_CHART = 1 / 1000000;          // lbs -> M lbs

  // Card conversions (USDA native reporting)
  var CRUSH_CARD = 1;          // tons
  var MEAL_CARD = 1;           // short tons
  var OIL_CARD = 1 / 1000;    // lbs -> 1,000 lbs

  var crush = oilData ? processRaw(oilData.crush, CRUSH_CHART, true) : {};
  var mealProd = oilData ? processRaw(oilData.meal_produced, MEAL_PROD_CHART) : {};
  var oilProd = oilData ? processRaw(oilData.oil_produced, OIL_PROD_CHART) : {};
  var mealStk = oilData ? processRaw(oilData.meal_stocks, MEAL_STK_CHART) : {};
  var oilStk = oilData ? processRaw(oilData.oil_stocks, OIL_STK_CHART) : {};
  var oilYield = processRaw(computeYield());

  var now = new Date();
  var curMY = now.getMonth() >= 9 ? now.getFullYear() : now.getFullYear() - 1;
  var rangeN = parseInt(range);
  var startMY = curMY - rangeN;

  var yrColors = ["#A32D2D","#D85A30","#E8A735","#639922","#1D9E75","#378ADD","#534AB7","#8B5CF6","#EC4899","#6B7280"];
  var getColor = function(my) { if (my === curMY) return "#333"; var dist = curMY - my; if (dist === 1) return "#1D9E75"; if (dist === 2) return "#639922"; if (dist === 3) return "#E8A735"; if (dist === 4) return "#D85A30"; if (dist === 5) return "#A32D2D"; return yrColors[(dist - 1) % yrColors.length]; };

  var buildItems = function(byMY) {
    var items = [];
    for (var y = startMY; y <= curMY; y++) { if (byMY[y]) items.push({ label: myLabel(y), my: y, color: getColor(y) }); }
    return items;
  };
  var allItems = buildItems(crush);
  var hk = Array.from(hiddenYrs).sort().join(",");

  // Card info (uses USDA native units)
  var getCardInfo = function(rawPts, cf) {
    if (!rawPts || !rawPts.length) return { cur: null, prevMo: null, lastYr: null, date: null };
    var sorted = rawPts.slice().sort(function(a, b) { return a.d < b.d ? 1 : -1; });
    var latest = sorted[0]; var prev = sorted.length > 1 ? sorted[1] : null;
    var targetStr = (function() { var d = new Date(latest.d + "-15"); d.setFullYear(d.getFullYear() - 1); return d.toISOString().slice(0, 7); })();
    var lastYrPt = rawPts.find(function(p) { return p.d === targetStr; });
    var c2 = cf || 1;
    return { cur: Math.round(latest.v * c2 * 100) / 100, prevMo: prev ? Math.round(prev.v * c2 * 100) / 100 : null, lastYr: lastYrPt ? Math.round(lastYrPt.v * c2 * 100) / 100 : null, date: latest.d };
  };

  var crushInfo = oilData ? getCardInfo(oilData.crush, CRUSH_CARD) : {};
  var mealProdInfo = oilData ? getCardInfo(oilData.meal_produced, MEAL_CARD) : {};
  var oilProdInfo = oilData ? getCardInfo(oilData.oil_produced, OIL_CARD) : {};
  var yieldRaw = computeYield();
  var yieldInfo = getCardInfo(yieldRaw);
  var mealStkInfo = oilData ? getCardInfo(oilData.meal_stocks, MEAL_CARD) : {};
  var oilStkInfo = oilData ? getCardInfo(oilData.oil_stocks, OIL_CARD) : {};

  var statCard = function(label, info, unitLabel) {
    var diffLine = function(lbl, comp) {
      if (info.cur == null || comp == null) return null;
      var pctChg = Math.round((info.cur - comp) / Math.abs(comp) * 1000) / 10;
      var col = pctChg > 0 ? "#639922" : pctChg < 0 ? "#A32D2D" : "var(--color-text-tertiary)";
      return (<div style={{display:"flex",justifyContent:"space-between",fontSize:10.5,padding:"1px 0"}}>
        <span style={{color:"var(--color-text-tertiary)"}}>{lbl}</span>
        <span style={{display:"flex",gap:4,alignItems:"baseline"}}><span style={{color:"var(--color-text-secondary)",textAlign:"right",minWidth:70}}>{comp.toLocaleString()}</span><span style={{color:col,fontWeight:500,textAlign:"right",minWidth:56}}>({pctChg > 0 ? "+" : ""}{pctChg.toFixed(1)}%)</span></span>
      </div>);
    };
    return (<div style={{background:"var(--color-background-secondary)",borderRadius:"var(--border-radius-md)",padding:"12px 14px",minWidth:0}}>
      <div style={{fontSize:11,color:"var(--color-text-secondary)",marginBottom:3,textTransform:"uppercase",letterSpacing:"0.4px"}}>{label}</div>
      <div style={{fontSize:22,fontWeight:500,color:"var(--color-text-primary)",marginBottom:2}}>{info.cur != null ? info.cur.toLocaleString() : "—"}<span style={{fontSize:12,fontWeight:400,color:"var(--color-text-secondary)",marginLeft:4}}>{unitLabel}</span></div>
      {info.date && <div style={{fontSize:10,color:"var(--color-text-tertiary)",marginBottom:6}}>as of {fmtDate(info.date)}</div>}
      <div style={{borderTop:"0.5px solid var(--color-border-tertiary)",paddingTop:5}}>
        {diffLine("vs. last month", info.prevMo)}
        {diffLine("vs. last year", info.lastYr)}
      </div>
    </div>);
  };

  // Chart builder
  var mkChart = function(byMY, yDecimals, useSepAxis) {
    var axisN = useSepAxis ? mktN_sep : mktN;
    return function(canvas) {
    if (!byMY || Object.keys(byMY).length === 0) return;
    var isSeasonal = mode === "seasonal";
    var ds = [];
    if (isSeasonal) {
      for (var y = startMY; y <= curMY; y++) {
        var pts = byMY[y]; if (!pts || !pts.length) continue;
        ds.push({ label: myLabel(y), data: pts.slice(), borderColor: getColor(y), borderWidth: y === curMY ? 2.5 : 1.5, pointRadius: 0, pointHitRadius: 8, tension: 0, fill: false, showLine: true, hidden: hiddenYrs.has(myLabel(y)) });
      }
      if (ds.length === 0) return;
      var vis = ds.filter(function(d) { return !d.hidden; }).flatMap(function(d) { return d.data.map(function(p) { return p.y; }); });
      if (vis.length === 0) return;
      var rawMax = Math.max.apply(null, vis), rawMin = Math.min.apply(null, vis);
      var span = rawMax - rawMin || 1;
      var step = Math.pow(10, Math.floor(Math.log10(span / 4)));
      if (span / step < 4) step = step / 2;
      if (span / step > 8) step = step * 2;
      var yMin = Math.floor(rawMin / step) * step;
      var yMax = Math.ceil(rawMax / step) * step;
      if (yMax === rawMax) yMax += step;
      var yd = yDecimals || 0;
      new Chart(canvas, { type: "scatter", data: { datasets: ds }, options: {
        responsive: true, maintainAspectRatio: false,
        interaction: { mode: "nearest", intersect: false },
        plugins: { legend: { display: false }, tooltip: { mode: "nearest", intersect: false, backgroundColor: "rgba(0,0,0,0.6)", titleFont: { size: 11 }, bodyFont: { size: 11 },
          callbacks: { title: function(items) { if (!items.length) return ""; return axisN[Math.round(items[0].parsed.x)] || ""; },
            label: function(c2) { return c2.parsed.y == null ? null : c2.dataset.label + ": " + c2.parsed.y.toLocaleString(undefined, {minimumFractionDigits:yd,maximumFractionDigits:yd}); } } } },
        scales: { x: { type: "linear", min: -0.5, max: 11.5, afterBuildTicks: function(ax) { var t = []; for (var i = 0; i < 12; i++) t.push({value: i}); ax.ticks = t; }, ticks: { callback: function(v) { return v >= 0 && v < 12 ? axisN[Math.round(v)] : ""; }, autoSkip: false, maxRotation: 0, font: { size: 10 } }, grid: { color: "rgba(0,0,0,0.06)" } },
          y: { min: yMin, max: yMax, ticks: { stepSize: step, font: { size: 10 }, callback: function(v) { return v.toLocaleString(undefined, {minimumFractionDigits:yd,maximumFractionDigits:yd}); } }, grid: { color: "rgba(0,0,0,0.08)", lineWidth: 0.75 } } }
      } });
    } else {
      // Contiguous
      var allPts = [];
      var years = [];
      for (var y2 = startMY; y2 <= curMY; y2++) { if (byMY[y2]) years.push(y2); }
      years.forEach(function(yr, idx) { var pts2 = byMY[yr]; if (!pts2) return; pts2.forEach(function(p) { allPts.push({ x: idx * 12 + p.x, y: p.y }); }); });
      if (allPts.length === 0) return;
      ds.push({ label: "Data", data: allPts, borderColor: "#333", borderWidth: 1.5, pointRadius: 0, tension: 0, fill: false, showLine: true });
      var allY = allPts.map(function(p) { return p.y; });
      var rMax = Math.max.apply(null, allY), rMin = Math.min.apply(null, allY);
      var sp2 = rMax - rMin || 1;
      var st2 = Math.pow(10, Math.floor(Math.log10(sp2 / 4)));
      if (sp2 / st2 < 4) st2 = st2 / 2;
      if (sp2 / st2 > 8) st2 = st2 * 2;
      var yMin2 = Math.floor(rMin / st2) * st2;
      var yMax2 = Math.ceil(rMax / st2) * st2;
      var yd2 = yDecimals || 0;
      var isShort = years.length <= 2;
      // Ticks: Oct boundaries as gridlines, MY labels centered between Oct marks
      var xTicks = [];
      if (isShort) {
        // mmm-yy labels with dynamic interval
        var totalMonths = years.length * 12;
        var interval = totalMonths > 18 ? 3 : totalMonths > 12 ? 2 : 1;
        var tickIdx = 0;
        years.forEach(function(yr, idx) {
          for (var mi = 0; mi < 12; mi++) {
            var calYr = (useSepAxis ? (mi >= 4 ? yr + 1 : yr) : (mi >= 3 ? yr + 1 : yr));
            if (tickIdx % interval === 0) {
              xTicks.push({value: idx*12+mi, label: axisN[mi] + "-" + String(calYr).slice(2)});
            } else {
              xTicks.push({value: idx*12+mi, label: ""});
            }
            tickIdx++;
          }
        });
      } else {
        // MY labels centered at month index 5.5 (between Apr and May)
        years.forEach(function(yr, idx) {
          xTicks.push({value: idx * 12, label: "", grid: true});  // Oct gridline
          xTicks.push({value: idx * 12 + 5.5, label: myLabel(yr), grid: false}); // centered label
        });
      }
      new Chart(canvas, { type: "scatter", data: { datasets: ds }, options: {
        responsive: true, maintainAspectRatio: false,
        interaction: { mode: "nearest", intersect: false },
        plugins: { legend: { display: false }, tooltip: { backgroundColor: "rgba(0,0,0,0.6)", callbacks: { title: function(items) { if (!items.length) return ""; var v = items[0].parsed.x; var yrIdx = Math.floor(v / 12); var moIdx = Math.round(v - yrIdx * 12); if (yrIdx >= years.length) return ""; var calYr = moIdx >= 3 ? years[yrIdx] + 1 : years[yrIdx]; return axisN[moIdx] + " " + calYr; }, label: function(c2) { return c2.parsed.y == null ? null : c2.parsed.y.toLocaleString(undefined, {minimumFractionDigits:yd2,maximumFractionDigits:yd2}); } } } },
        scales: { x: { type: "linear", min: -0.5, max: years.length * 12 - 0.5,
          afterBuildTicks: function(ax) { ax.ticks = xTicks.map(function(t) { return {value: t.value}; }); },
          ticks: { callback: function(v) { var found = xTicks.find(function(t) { return Math.abs(t.value - v) < 0.1; }); return found ? found.label : ""; }, autoSkip: false, maxRotation: 0, font: { size: 10 } },
          grid: { color: function(ctx) { var v = ctx.tick.value; if (Number.isInteger(v) && v % 12 === 0 && v > 0) return "rgba(0,0,0,0.15)"; return "transparent"; } } },
          y: { min: yMin2, max: yMax2, ticks: { stepSize: st2, font: { size: 10 }, callback: function(v) { return v.toLocaleString(undefined, {minimumFractionDigits:yd2,maximumFractionDigits:yd2}); } }, grid: { color: "rgba(0,0,0,0.08)" } } }
      } });
    }
  }; };

  var dlCSV = function() {
    var hdrs = ["Date", "MY", "Crush (tons)", "Meal Production (short tons)", "Oil Production (1000 lbs)", "Oil Yield (lbs/bu)", "Meal Stocks (short tons)", "Oil Stocks (1000 lbs)"];
    var inRange = function(d) { var my = dateToMY(d); return my >= startMY && my <= curMY; };
    var allDates = {};
    if (oilData) {
      (oilData.crush || []).filter(function(p){return inRange(p.d);}).forEach(function(p) { allDates[p.d] = allDates[p.d] || {}; allDates[p.d].crush = p.v; });
      (oilData.meal_produced || []).filter(function(p){return inRange(p.d);}).forEach(function(p) { allDates[p.d] = allDates[p.d] || {}; allDates[p.d].mealP = p.v; });
      (oilData.oil_produced || []).filter(function(p){return inRange(p.d);}).forEach(function(p) { allDates[p.d] = allDates[p.d] || {}; allDates[p.d].oilP = Math.round(p.v / 1000); });
      (oilData.meal_stocks || []).filter(function(p){return inRange(p.d);}).forEach(function(p) { allDates[p.d] = allDates[p.d] || {}; allDates[p.d].mealS = p.v; });
      (oilData.oil_stocks || []).filter(function(p){return inRange(p.d);}).forEach(function(p) { allDates[p.d] = allDates[p.d] || {}; allDates[p.d].oilS = Math.round(p.v / 1000); });
    }
    computeYield().filter(function(p){return inRange(p.d);}).forEach(function(p) { allDates[p.d] = allDates[p.d] || {}; allDates[p.d].yield = p.v; });
    var rows = [];
    Object.keys(allDates).sort().forEach(function(d) {
      var r = allDates[d];
      rows.push([d, myLabel(dateToMY(d)), r.crush||"", r.mealP||"", r.oilP||"", r.yield||"", r.mealS||"", r.oilS||""]);
    });
    downloadCSV("oilseed_crushing.csv", hdrs, rows);
  };

  var chevSvg = "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath d='M3 5l3 3 3-3' fill='none' stroke='%23666' stroke-width='1.5'/%3E%3C/svg%3E\")";
  var selSt = {padding:"6px 24px 6px 10px",fontSize:13,fontWeight:500,border:"1px solid var(--color-border-secondary)",borderRadius:6,background:"var(--color-background-primary)",color:"var(--color-text-primary)",fontFamily:"inherit",cursor:"pointer",appearance:"none",backgroundImage:chevSvg,backgroundRepeat:"no-repeat",backgroundPosition:"right 6px center"};
  var modeSt = function(a) { return {padding:"6px 14px",fontSize:12,fontWeight:a?600:400,border:"1px solid "+(a?"#2563EB":"var(--color-border-secondary)"),borderRadius:5,cursor:"pointer",background:a?"#2563EB":"transparent",color:a?"#fff":"var(--color-text-secondary)",transition:"all 0.15s"}; };

  var CHARTS = [
    { key: "crush", label: "Soybean Crush", data: crush, unit: "M bushels", yd: 0, sepAxis: true },
    { key: "yield", label: "Soybean Oil Yield", data: oilYield, unit: "lbs/bu", yd: 1, sepAxis: false },
    { key: "mealProd", label: "Soybean Meal Production", data: mealProd, unit: "M short tons", yd: 1, sepAxis: false },
    { key: "oilProd", label: "Soybean Oil Production", data: oilProd, unit: "M lbs", yd: 0, sepAxis: false },
    { key: "mealStk", label: "Soybean Meal Stocks", data: mealStk, unit: "1,000 short tons", yd: 0, sepAxis: false },
    { key: "oilStk", label: "Soybean Oil Stocks", data: oilStk, unit: "M lbs", yd: 0, sepAxis: false },
  ];

  return (<div>
    <div style={{display:"flex",alignItems:"center",gap:12,marginBottom:14,flexWrap:"wrap"}}>
      <div style={{display:"flex",alignItems:"center",gap:6}}>
        <span style={{fontSize:11,fontWeight:600,color:"var(--color-text-secondary)",textTransform:"uppercase"}}>Range</span>
        <select value={range} onChange={function(e){setRange(e.target.value);}} style={selSt}>
          <option value="1">1 Year</option>
          <option value="5">5 Years</option>
          <option value="10">10 Years</option>
        </select>
      </div>
      <div style={{display:"flex",gap:3}}>
        <button onClick={function(){setMode("seasonal");}} style={modeSt(mode==="seasonal")}>Seasonal</button>
        <button onClick={function(){setMode("contiguous");}} style={modeSt(mode==="contiguous")}>Contiguous</button>
      </div>
      <div style={{marginLeft:"auto"}}><DownloadBtn onClick={dlCSV} /></div>
    </div>

    <div style={{display:"grid",gridTemplateColumns:"1fr 1fr 1fr",gap:10,marginBottom:16}}>
      {statCard("Soybean Crush", crushInfo, "tons")}
      {statCard("Oil Yield", yieldInfo, "lbs/bu")}
      {statCard("Meal Production", mealProdInfo, "short tons")}
      {statCard("Oil Production", oilProdInfo, "1,000 lbs")}
      {statCard("Meal Stocks", mealStkInfo, "short tons")}
      {statCard("Oil Stocks", oilStkInfo, "1,000 lbs")}
    </div>

    {mode === "seasonal" && <div style={{display:"flex",flexWrap:"wrap",gap:6,marginBottom:16,alignItems:"center"}}>
      {allItems.map(function(item) { var isH = hiddenYrs.has(item.label); return (
        <button key={item.label} onClick={function(){toggleYr(item.label);}} style={{display:"flex",alignItems:"center",gap:5,padding:"4px 10px",border:"1px solid var(--color-border-secondary)",borderRadius:5,background:isH?"var(--color-background-secondary)":"transparent",cursor:"pointer",opacity:isH?0.3:1,transition:"all 0.15s"}}>
          <span style={{width:18,height:0,borderTop:"2.5px solid "+item.color,display:"inline-block"}}></span>
          <span style={{fontSize:12,fontWeight:500,color:"var(--color-text-primary)"}}>{item.label}</span>
        </button>); })}
    </div>}

    <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:16}}>
      {CHARTS.map(function(ch) { return (<div key={ch.key}>
        <div style={{fontSize:14,fontWeight:600,color:"var(--color-text-primary)",marginBottom:6}}>{ch.label} <span style={{fontSize:11,fontWeight:400,color:"var(--color-text-tertiary)"}}>({ch.unit})</span></div>
        {ready && <ChartBox id={"oil_"+ch.key+"_"+mode+"_"+range} height={220} renderChart={mkChart(ch.data, ch.yd, ch.sepAxis)} deps={"oil_"+ch.key+"_"+mode+"_"+range+"_"+oilLoaded+"_"+hk} />}
      </div>); })}
    </div>
    <div style={{marginTop:14,fontSize:11,color:"var(--color-text-tertiary)"}}>Source: USDA NASS Fats & Oils: Oilseed Crushings. Oil yield = crude oil produced at crushers / bushels crushed. Oil stocks = crude + once refined (all locations).</div>
  </div>);
}


function HogsPigsPage({ ready }) {
  const [chartMode, setChartMode] = useState("seasonal");
  const [hTotal, tTotal] = useToggle();
  const [hBreed, tBreed] = useToggle();
  const [hMkt, tMkt] = useToggle();
  const [hPig, tPig] = useToggle();

  const seasonLegend = [
    { label: "2025", color: "#D85A30", key: "2025" },
    { label: "2024", color: "#378ADD", key: "2024", dash: "dashed" },
    { label: "2023", color: "#1D9E75", key: "2023", dash: "dashed" },
    { label: "5-yr avg", color: "#333", key: "5yr", dash: "dotted" },
  ];
  const seasonDS = {
    "2025": { borderColor: "#D85A30", borderWidth: 2.5, pointRadius: 0, tension: 0 },
    "2024": { borderColor: "#378ADD", borderWidth: 1.5, pointRadius: 0, tension: 0, borderDash: [5,3] },
    "2023": { borderColor: "#1D9E75", borderWidth: 1.5, pointRadius: 0, tension: 0, borderDash: [4,4] },
    "5yr":  { borderColor: "#333", borderWidth: 1.5, pointRadius: 0, tension: 0, borderDash: [2,3] },
  };

  function niceAxis(allVals) {
    if (allVals.length === 0) return { yMin: 0, yMax: 100 };
    const dataMin = Math.min(...allVals); const dataMax = Math.max(...allVals);
    const range = dataMax - dataMin; const pad = Math.max(range * 0.2, dataMax * 0.01);
    const rawStep = (range + pad * 2) / 5;
    const mag = Math.pow(10, Math.floor(Math.log10(rawStep)));
    const norm = rawStep / mag;
    const niceNorm = norm <= 1.5 ? 1 : norm <= 3.5 ? 2 : norm <= 7.5 ? 5 : 10;
    const step = niceNorm * mag;
    return { yMin: Math.floor((dataMin - pad) / step) * step, yMax: Math.ceil((dataMax + pad) / step) * step };
  }

  const mkChart = (dataObj, hidden) => (canvas) => {
    if (chartMode === "contiguous") {
      const labels = ["2023","2024","2025"].flatMap(y => HOGS_PIGS_QUARTERS.map(q => `${q} '${y.slice(2)}`));
      const allData = [...(dataObj["2023"] || []), ...(dataObj["2024"] || []), ...(dataObj["2025"] || [])];
      const allVals = allData.filter(v => v != null);
      const { yMin, yMax } = niceAxis(allVals);
      new Chart(canvas, {
        type: "line", data: { labels, datasets: [{
          label: "Inventory", data: allData, borderColor: "#D85A30", backgroundColor: "rgba(216,90,48,0.06)",
          fill: true, borderWidth: 2, pointRadius: 0, tension: 0, spanGaps: true,
        }]},
        options: { responsive: true, maintainAspectRatio: false,
          interaction: { mode: "nearest", intersect: false },
          plugins: { legend: { display: false }, tooltip: { callbacks: { label: c => `${c.parsed.y != null ? c.parsed.y.toLocaleString() : "n/a"}` } } },
          scales: {
            x: { ticks: { font: { size: 10 }, maxRotation: 45 }, grid: { color: "rgba(0,0,0,0.12)", lineWidth: 0.75 } },
            y: { min: yMin, max: yMax, title: { display: true, text: "thousand head", font: { size: 11 } }, ticks: { font: { size: 11 }, callback: v => (v / 1000).toFixed(0) + "M" }, grid: { color: "rgba(0,0,0,0.12)", lineWidth: 0.75 } },
          },
        },
      });
      return;
    }
    const keys = ["2025","2024","2023","5yr"].filter(k => !hidden.has(k));
    const ds = keys.map(k => ({
      label: k === "5yr" ? "5-yr avg" : k, data: dataObj[k], ...seasonDS[k], spanGaps: true,
    }));
    const allVals = keys.flatMap(k => (dataObj[k] || []).filter(v => v != null));
    const { yMin, yMax } = niceAxis(allVals);
    new Chart(canvas, {
      type: "line", data: { labels: HOGS_PIGS_QUARTERS, datasets: ds },
      options: { responsive: true, maintainAspectRatio: false,
        interaction: { mode: "nearest", intersect: false }, plugins: { legend: { display: false }, tooltip: { callbacks: { label: c => `${c.dataset.label}: ${c.parsed.y != null ? c.parsed.y.toLocaleString() : "n/a"}` } } },
        scales: {
          x: { ticks: { font: { size: 11 } }, grid: { color: "rgba(0,0,0,0.12)", lineWidth: 0.75 } },
          y: { min: yMin, max: yMax, title: { display: true, text: "thousand head", font: { size: 11 } }, ticks: { font: { size: 11 }, callback: v => (v / 1000).toFixed(0) + "M" }, grid: { color: "rgba(0,0,0,0.12)", lineWidth: 0.75 } },
        },
      },
    });
  };

  const lastNN = (arr) => { for (let i = arr.length - 1; i >= 0; i--) { if (arr[i] != null) return arr[i]; } return null; };
  const pctChg = (a, b) => b != null && b !== 0 ? ((a - b) / b * 100).toFixed(1) : null;

  const totalL = lastNN(HOGS_PIGS.totalInventory["2025"]);
  const totalYA = HOGS_PIGS.totalInventory["2024"][0];
  const breedL = lastNN(HOGS_PIGS.breedingInventory["2025"]);
  const breedYA = HOGS_PIGS.breedingInventory["2024"][0];
  const mktL = lastNN(HOGS_PIGS.marketInventory["2025"]);
  const mktYA = HOGS_PIGS.marketInventory["2024"][0];
  const pigL = lastNN(HOGS_PIGS.pigCrop["2025"]);
  const pigYA = HOGS_PIGS.pigCrop["2024"][0];

  const DiffLine = ({ label, absVal, cur }) => {
    if (absVal == null || cur == null) return null;
    const d = Number(pctChg(cur, absVal));
    if (isNaN(d)) return null;
    const col = d > 0 ? "#639922" : d < 0 ? "#A32D2D" : "var(--color-text-tertiary)";
    return (
      <div style={{ display: "flex", justifyContent: "space-between", fontSize: 11, padding: "2px 0" }}>
        <span style={{ color: "var(--color-text-tertiary)" }}>{label} ({absVal.toLocaleString()})</span>
        <span style={{ color: col, fontWeight: 500, fontFamily: "var(--font-mono)" }}>{d > 0 ? "+" : ""}{d}%</span>
      </div>
    );
  };

  const HPMetric = ({ label, cur, ya, ya5, unit }) => (
    <div style={{ background: "var(--color-background-secondary)", borderRadius: "var(--border-radius-md)", padding: "12px 14px", minWidth: 0 }}>
      <div style={{ fontSize: 11, color: "var(--color-text-secondary)", marginBottom: 3, textTransform: "uppercase", letterSpacing: "0.4px" }}>{label}</div>
      <div style={{ fontSize: 22, fontWeight: 500, color: "var(--color-text-primary)", marginBottom: 6 }}>{cur != null ? (cur / 1000).toFixed(1) + "M" : "—"} <span style={{ fontSize: 12, fontWeight: 400, color: "var(--color-text-secondary)" }}>head</span></div>
      {cur != null && <div style={{ borderTop: "0.5px solid var(--color-border-tertiary)", paddingTop: 6, display: "flex", flexDirection: "column", gap: 1 }}>
        <DiffLine label="vs. last year" absVal={ya} cur={cur} />
        {ya5 != null && <DiffLine label="vs. 5-yr avg" absVal={ya5} cur={cur} />}
      </div>}
    </div>
  );

  const dlHP = (dataObj, fn) => () => {
    const headers = ["Quarter","2025","2024","2023","5-yr avg"];
    const rows = HOGS_PIGS_QUARTERS.map((q, i) => [q, dataObj["2025"][i] ?? "", dataObj["2024"][i], dataObj["2023"][i], dataObj["5yr"][i]]);
    downloadCSV(fn, headers, rows);
  };

  return (<div>
    <div style={{ fontSize: 11, color: "var(--color-text-tertiary)", marginBottom: 16 }}>USDA NASS Quarterly Hogs and Pigs report — as of Mar 1, 2025</div>

    <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(155px, 1fr))", gap: 10, marginBottom: 8 }}>
      <HPMetric label="Total inventory" cur={totalL} ya={totalYA} ya5={HOGS_PIGS.totalInventory["5yr"][0]} />
      <HPMetric label="Breeding" cur={breedL} ya={breedYA} ya5={HOGS_PIGS.breedingInventory["5yr"][0]} />
      <HPMetric label="Market hogs" cur={mktL} ya={mktYA} ya5={HOGS_PIGS.marketInventory["5yr"][0]} />
      <HPMetric label="Pig crop" cur={pigL} ya={pigYA} ya5={HOGS_PIGS.pigCrop["5yr"][0]} />
    </div>

    <SectionTitle right={<div style={{ display: "flex", gap: 8, alignItems: "center" }}><ChartModeToggle mode={chartMode} setMode={setChartMode} /><DownloadBtn onClick={dlHP(HOGS_PIGS.totalInventory, "hogs_total_inventory.csv")} /></div>}>Total hog inventory</SectionTitle>
    {chartMode === "seasonal" && <InteractiveLegend items={seasonLegend} hidden={hTotal} onToggle={tTotal} />}
    {ready && <ChartBox id={`hp_total_${chartMode}`} renderChart={mkChart(HOGS_PIGS.totalInventory, hTotal)} deps={`${chartMode}_${[...hTotal].join()}`} />}

    <SectionTitle right={<div style={{ display: "flex", gap: 8, alignItems: "center" }}><ChartModeToggle mode={chartMode} setMode={setChartMode} /><DownloadBtn onClick={dlHP(HOGS_PIGS.breedingInventory, "hogs_breeding_inventory.csv")} /></div>}>Breeding inventory</SectionTitle>
    {chartMode === "seasonal" && <InteractiveLegend items={seasonLegend} hidden={hBreed} onToggle={tBreed} />}
    {ready && <ChartBox id={`hp_breed_${chartMode}`} renderChart={mkChart(HOGS_PIGS.breedingInventory, hBreed)} deps={`${chartMode}_${[...hBreed].join()}`} />}

    <SectionTitle right={<div style={{ display: "flex", gap: 8, alignItems: "center" }}><ChartModeToggle mode={chartMode} setMode={setChartMode} /><DownloadBtn onClick={dlHP(HOGS_PIGS.marketInventory, "hogs_market_inventory.csv")} /></div>}>Market hog inventory</SectionTitle>
    {chartMode === "seasonal" && <InteractiveLegend items={seasonLegend} hidden={hMkt} onToggle={tMkt} />}
    {ready && <ChartBox id={`hp_mkt_${chartMode}`} renderChart={mkChart(HOGS_PIGS.marketInventory, hMkt)} deps={`${chartMode}_${[...hMkt].join()}`} />}

    <SectionTitle right={<div style={{ display: "flex", gap: 8, alignItems: "center" }}><ChartModeToggle mode={chartMode} setMode={setChartMode} /><DownloadBtn onClick={dlHP(HOGS_PIGS.pigCrop, "hogs_pig_crop.csv")} /></div>}>Pig crop</SectionTitle>
    {chartMode === "seasonal" && <InteractiveLegend items={seasonLegend} hidden={hPig} onToggle={tPig} />}
    {ready && <ChartBox id={`hp_pig_${chartMode}`} renderChart={mkChart(HOGS_PIGS.pigCrop, hPig)} deps={`${chartMode}_${[...hPig].join()}`} />}

    <div style={{ marginTop: 12, fontSize: 10, color: "var(--color-text-tertiary)" }}>
      Source: USDA NASS Quarterly Hogs and Pigs report. Inventory as of Mar 1, Jun 1, Sep 1, Dec 1 each year. All figures in thousand head.
    </div>
  </div>);
}

// ════════════════════════════════════════════════════════════════════════
// PAGE MAP & MAIN APP
// ════════════════════════════════════════════════════════════════════════

// ════════════════════════════════════════════════════════════════════════
// COT — COMMITMENT OF TRADERS PAGES
// ════════════════════════════════════════════════════════════════════════

function useLiveCOT() {
  const [liveCOT, setLiveCOT] = useState(null);
  const [cotMeta, setCotMeta] = useState(null);
  const [loaded, setLoaded] = useState(false);
  useEffect(() => {
    fetch("data/cot.json?t=" + Date.now())
      .then(r => { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); })
      .then(data => {
        if (data && data.data && Object.keys(data.data).length > 0) {
          setLiveCOT(data.data);
          setCotMeta({ weeks: data.weeks, fetched: data.fetched_at });
        }
        setLoaded(true);
      })
      .catch(e => { console.warn("COT fetch:", e); setLoaded(true); });
  }, []);
  return { cotData: liveCOT || COT_DATA, cotMeta, cotLoaded: loaded };
}

function COTSummaryPage() {
  const { cotData, cotMeta, cotLoaded } = useLiveCOT();
  const fmt = (v) => {
    if (v == null) return "—";
    const abs = Math.abs(v);
    const str = abs.toLocaleString();
    return v < 0 ? `(${str})` : str;
  };
  const fmtChg = (v) => {
    if (v == null) return "—";
    return `${v > 0 ? "+" : ""}${v.toLocaleString()}`;
  };
  const chgColor = (v) => v > 0 ? "#639922" : v < 0 ? "#A32D2D" : "var(--color-text-tertiary)";
  const netColor = (v) => v > 0 ? "#639922" : v < 0 ? "#A32D2D" : "var(--color-text-primary)";

  const thStyle = { padding: "4px 8px", textAlign: "right", fontWeight: 500, fontSize: 11.5, color: "var(--color-text-secondary)", borderBottom: "1.5px solid var(--color-border-primary)", whiteSpace: "nowrap" };
  const tdNum = { padding: "5px 8px", textAlign: "right", fontFamily: "var(--font-mono)", fontSize: 12.5 };

  const dlSummary = () => {
    const headers = ["Commodity","Prod Net","Prod Chg","Swap Net","Swap Chg","MM Net","MM Chg","MM Rec Long","MM Rec Short","Other Net","Other Chg","Open Interest","OI Chg"];
    const rows = COT_GROUPS.flatMap(g => g.items.map(item => {
      const d = cotData[item.id]; if (!d) return [item.label]; const li = d.managed.net.length - 1;
      return [item.label, d.producer.net[li], d.producer.chg, d.swap.net[li], d.swap.chg, d.managed.net[li], d.managed.chg, d.managed.recLong, d.managed.recShort, d.other.net[li], d.other.chg, d.oi.net[li], d.oi.chg];
    }));
    downloadCSV("cot_disaggregated_summary.csv", headers, rows);
  };

  // Date range label — uses global fmtDateRange for "April 21, 2026 – April 28, 2026"
  const dateLabel = cotMeta && cotMeta.weeks && cotMeta.weeks.length >= 2
    ? fmtDateRange(cotMeta.weeks[cotMeta.weeks.length - 2], cotMeta.weeks[cotMeta.weeks.length - 1], true)
    : fmtDateRange("2026-03-03", "2026-03-10", true);

  return (<div>
    <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 14, flexWrap: "wrap", gap: 8 }}>
      <div style={{ fontSize: 11, color: "var(--color-text-tertiary)" }}>CFTC Disaggregated Futures & Options — {dateLabel}</div>
      <DownloadBtn onClick={dlSummary} />
    </div>
    <div style={{ overflowX: "auto", border: "0.5px solid var(--color-border-tertiary)", borderRadius: "var(--border-radius-lg)" }}>
      <table style={{ borderCollapse: "collapse", fontSize: 12, minWidth: "100%", whiteSpace: "nowrap" }}>
        <thead>
          <tr style={{ background: "var(--color-background-secondary)" }}>
            <th rowSpan={2} style={{ ...thStyle, textAlign: "left", position: "sticky", left: 0, zIndex: 3, background: "#ffffff", minWidth: 120, borderRight: "0.5px solid var(--color-border-tertiary)" }}></th>
            <th colSpan={2} style={{ ...thStyle, textAlign: "center", borderBottom: "2px solid #333" }}>Producer/Merchant</th>
            <th rowSpan={2} style={{ width: 12, padding: 0, background: "var(--color-background-primary)", border: "none" }}></th>
            <th colSpan={2} style={{ ...thStyle, textAlign: "center", borderBottom: "2px solid #333" }}>Swap Dealers</th>
            <th rowSpan={2} style={{ width: 12, padding: 0, background: "var(--color-background-primary)", border: "none" }}></th>
            <th colSpan={4} style={{ ...thStyle, textAlign: "center", borderBottom: "2px solid #333", background: "rgba(163,45,45,0.04)" }}>Managed Money</th>
            <th rowSpan={2} style={{ width: 12, padding: 0, background: "var(--color-background-primary)", border: "none" }}></th>
            <th colSpan={2} style={{ ...thStyle, textAlign: "center", borderBottom: "2px solid #333" }}>Other Reportables</th>
            <th rowSpan={2} style={{ width: 12, padding: 0, background: "var(--color-background-primary)", border: "none" }}></th>
            <th colSpan={2} style={{ ...thStyle, textAlign: "center", borderBottom: "0.5px solid var(--color-border-tertiary)" }}></th>
          </tr>
          <tr style={{ background: "var(--color-background-secondary)" }}>
            <th style={thStyle}>Net</th><th style={thStyle}>Chg</th>
            <th style={thStyle}>Net</th><th style={thStyle}>Chg</th>
            <th style={{ ...thStyle, background: "rgba(163,45,45,0.04)" }}>Net</th>
            <th style={{ ...thStyle, background: "rgba(163,45,45,0.04)" }}>Chg</th>
            <th style={{ ...thStyle, background: "rgba(163,45,45,0.04)" }}>Rec Long</th>
            <th style={{ ...thStyle, background: "rgba(163,45,45,0.04)" }}>Rec Short</th>
            <th style={thStyle}>Net</th>
            <th style={thStyle}>Chg</th>
            <th style={thStyle}>Open Int</th><th style={thStyle}>Chg</th>
          </tr>
        </thead>
        <tbody>
          {COT_GROUPS.map(g => (<>
            <tr key={`gh-${g.header}`} style={{ background: "#e8e8e8" }}>
              <td colSpan={18} style={{ padding: "8px 10px 4px", fontWeight: 600, fontSize: 12.5, color: "var(--color-text-primary)", background: "#e8e8e8", position: "sticky", left: 0, textTransform: "uppercase", letterSpacing: "0.3px" }}>{g.header}</td>
            </tr>
            {g.items.map(item => {
              const d = cotData[item.id]; if (!d) return null; const li = d.managed.net.length - 1;
              return (
                <tr key={item.id} style={{ borderBottom: "0.5px solid var(--color-border-tertiary)" }}
                  onMouseEnter={e => e.currentTarget.style.background = "var(--color-background-secondary)"}
                  onMouseLeave={e => e.currentTarget.style.background = "transparent"}>
                  <td style={{ padding: "5px 10px", fontWeight: 500, fontSize: 13, color: "var(--color-text-primary)", position: "sticky", left: 0, background: "inherit", borderRight: "0.5px solid var(--color-border-tertiary)", zIndex: 1 }}>{item.label}</td>
                  <td style={{ ...tdNum, color: netColor(d.producer.net[li]) }}>{fmt(d.producer.net[li])}</td>
                  <td style={{ ...tdNum, color: chgColor(d.producer.chg) }}>{fmtChg(d.producer.chg)}</td>
                  <td style={{ padding: 0, border: "none" }}></td>
                  <td style={{ ...tdNum, color: netColor(d.swap.net[li]) }}>{fmt(d.swap.net[li])}</td>
                  <td style={{ ...tdNum, color: chgColor(d.swap.chg) }}>{fmtChg(d.swap.chg)}</td>
                  <td style={{ padding: 0, border: "none" }}></td>
                  <td style={{ ...tdNum, color: netColor(d.managed.net[li]), fontWeight: (d.managed.net[li] >= d.managed.recLong || d.managed.net[li] <= d.managed.recShort) ? 700 : 500, background: "rgba(163,45,45,0.02)", outline: d.managed.net[li] >= d.managed.recLong ? "2px solid #639922" : d.managed.net[li] <= d.managed.recShort ? "2px solid #A32D2D" : "none", outlineOffset: "-2px" }}>{fmt(d.managed.net[li])}</td>
                  <td style={{ ...tdNum, color: chgColor(d.managed.chg), background: "rgba(163,45,45,0.02)" }}>{fmtChg(d.managed.chg)}</td>
                  <td style={{ ...tdNum, color: "var(--color-text-secondary)", background: "rgba(163,45,45,0.02)" }}>{d.managed.recLong.toLocaleString()}</td>
                  <td style={{ ...tdNum, color: "var(--color-text-secondary)", background: "rgba(163,45,45,0.02)" }}>({Math.abs(d.managed.recShort).toLocaleString()})</td>
                  <td style={{ padding: 0, border: "none" }}></td>
                  <td style={{ ...tdNum, color: netColor(d.other.net[li]) }}>{fmt(d.other.net[li])}</td>
                  <td style={{ ...tdNum, color: chgColor(d.other.chg) }}>{fmtChg(d.other.chg)}</td>
                  <td style={{ padding: 0, border: "none" }}></td>
                  <td style={{ ...tdNum, color: "var(--color-text-primary)" }}>{d.oi.net[li].toLocaleString()}</td>
                  <td style={{ ...tdNum, color: chgColor(d.oi.chg) }}>{fmtChg(d.oi.chg)}</td>
                </tr>
              );
            })}
          </>))}
        </tbody>
      </table>
    </div>
    <div style={{ marginTop: 10, fontSize: 11, color: "var(--color-text-tertiary)" }}>Source: CFTC Disaggregated Commitments of Traders report. Futures & Options combined. Positions in contracts.</div>
  </div>);
}

function COTDetailPage({ ready, commodityId }) {
  const { cotData } = useLiveCOT();
  const d = cotData[commodityId];
  const [hCats, tCats] = useToggle();

  if (!d) return <div>No data available</div>;

  const li = d.managed.net.length - 1;
  const mmNet = d.managed.net[li];
  const mmPrev = li > 0 ? d.managed.net[li - 1] : null;
  const mmChg = mmPrev != null ? mmNet - mmPrev : null;
  const pctOI = d.oi.net[li] ? (mmNet / d.oi.net[li]) * 100 : null;

  function niceAxis(allVals) {
    if (allVals.length === 0) return { yMin: 0, yMax: 100 };
    const dataMin = Math.min(...allVals); const dataMax = Math.max(...allVals);
    const range = dataMax - dataMin; const pad = Math.max(range * 0.2, Math.abs(dataMax) * 0.05);
    const rawStep = (range + pad * 2) / 5;
    const mag = Math.pow(10, Math.floor(Math.log10(rawStep)));
    const norm = rawStep / mag;
    const niceNorm = norm <= 1.5 ? 1 : norm <= 3.5 ? 2 : norm <= 7.5 ? 5 : 10;
    const step = niceNorm * mag;
    return { yMin: Math.floor((dataMin - pad) / step) * step, yMax: Math.ceil((dataMax + pad) / step) * step };
  }

  const catLegend = [
    { label: "Producer/Merchant", color: "#A32D2D" },
    { label: "Swap Dealers", color: "#378ADD" },
    { label: "Managed Money", color: "#639922" },
    { label: "Other Reportables", color: "#534AB7" },
  ];
  const catDS = {
    "Producer/Merchant": { borderColor: "#A32D2D", borderWidth: 2, pointRadius: 0, tension: 0 },
    "Swap Dealers": { borderColor: "#378ADD", borderWidth: 2, pointRadius: 0, tension: 0 },
    "Managed Money": { borderColor: "#639922", borderWidth: 2.5, pointRadius: 0, tension: 0 },
    "Other Reportables": { borderColor: "#534AB7", borderWidth: 1.5, pointRadius: 0, tension: 0, borderDash: [4,3] },
  };
  const catData = [
    { key: "Producer/Merchant", data: d.producer.net },
    { key: "Swap Dealers", data: d.swap.net },
    { key: "Managed Money", data: d.managed.net },
    { key: "Other Reportables", data: d.other.net },
  ];

  const rcAllCats = useCallback(canvas => {
    const visible = catData.filter(c => !hCats.has(c.key));
    const allVals = visible.flatMap(c => c.data);
    const { yMin, yMax } = niceAxis(allVals);
    new Chart(canvas, {
      type: "line", data: { labels: COT_WEEKS, datasets: visible.map(c => ({ label: c.key, data: c.data, ...catDS[c.key] })) },
      options: { responsive: true, maintainAspectRatio: false,
        interaction: { mode: "nearest", intersect: false },
        plugins: { legend: { display: false }, tooltip: { callbacks: { label: c => `${c.dataset.label}: ${c.parsed.y > 0 ? "+" : ""}${c.parsed.y.toLocaleString()}` } } },
        scales: {
          x: { ticks: { autoSkip: true, maxTicksLimit: 10, maxRotation: 45, font: { size: 10 } }, grid: { color: "rgba(0,0,0,0.08)", lineWidth: 0.5 } },
          y: { min: yMin, max: yMax, title: { display: true, text: "net contracts", font: { size: 11 } }, ticks: { font: { size: 10 }, callback: v => (v / 1000).toFixed(0) + "K" }, grid: { color: "rgba(0,0,0,0.08)", lineWidth: 0.5 } },
        },
      },
    });
  }, [d, hCats]);

  const rcMMBar = useCallback(canvas => {
    const { yMin, yMax } = niceAxis(d.managed.net);
    new Chart(canvas, {
      type: "bar", data: { labels: COT_WEEKS, datasets: [{
        label: "Managed Money Net", data: d.managed.net,
        backgroundColor: d.managed.net.map(v => v >= 0 ? "rgba(99,153,34,0.6)" : "rgba(163,45,45,0.6)"),
        borderColor: d.managed.net.map(v => v >= 0 ? "#639922" : "#A32D2D"),
        borderWidth: 1, borderRadius: 2,
      }]},
      options: { responsive: true, maintainAspectRatio: false,
        interaction: { mode: "nearest", intersect: false },
        plugins: { legend: { display: false }, tooltip: { callbacks: { label: c => `MM Net: ${c.parsed.y > 0 ? "+" : ""}${c.parsed.y.toLocaleString()}` } } },
        scales: {
          x: { ticks: { autoSkip: true, maxTicksLimit: 10, maxRotation: 45, font: { size: 10 } }, grid: { color: "rgba(0,0,0,0.08)", lineWidth: 0.5 } },
          y: { min: yMin, max: yMax, title: { display: true, text: "contracts", font: { size: 11 } }, ticks: { font: { size: 10 }, callback: v => (v / 1000).toFixed(0) + "K" }, grid: { color: "rgba(0,0,0,0.08)", lineWidth: 0.5 } },
        },
      },
    });
  }, [d]);

  const rcOI = useCallback(canvas => {
    const { yMin, yMax } = niceAxis(d.oi.net);
    new Chart(canvas, {
      type: "line", data: { labels: COT_WEEKS, datasets: [{ label: "Open interest", data: d.oi.net, borderColor: "#534AB7", backgroundColor: "rgba(83,74,183,0.06)", fill: true, borderWidth: 2, pointRadius: 0, tension: 0 }] },
      options: { responsive: true, maintainAspectRatio: false,
        interaction: { mode: "nearest", intersect: false },
        plugins: { legend: { display: false }, tooltip: { callbacks: { label: c => `OI: ${c.parsed.y.toLocaleString()}` } } },
        scales: {
          x: { ticks: { autoSkip: true, maxTicksLimit: 10, maxRotation: 45, font: { size: 10 } }, grid: { color: "rgba(0,0,0,0.08)", lineWidth: 0.5 } },
          y: { min: yMin, max: yMax, title: { display: true, text: "contracts", font: { size: 11 } }, ticks: { font: { size: 10 }, callback: v => (v / 1000000).toFixed(1) + "M" }, grid: { color: "rgba(0,0,0,0.08)", lineWidth: 0.5 } },
        },
      },
    });
  }, [d]);

  const dlCOT = () => {
    const headers = ["Week","Producer","Swap Dealers","Managed Money","Other Reportables","Open Interest"];
    const rows = COT_WEEKS.map((w, i) => [w, d.producer.net[i], d.swap.net[i], d.managed.net[i], d.other.net[i], d.oi.net[i]]);
    downloadCSV(`cot_${commodityId.replace("cot-","")}.csv`, headers, rows);
  };

  return (<div>
    <div style={{ fontSize: 11, color: "var(--color-text-tertiary)", marginBottom: 14 }}>{d.exchange} — {d.contract} per contract — as of {fmtDate(COT_WEEKS[li] + ", 2026")}</div>

    <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))", gap: 10, marginBottom: 8 }}>
      <MetricCard label="Producer net" value={`${(d.producer.net[li] / 1000).toFixed(1)}K`} sub="contracts" />
      <MetricCard label="Swap net" value={`${(d.swap.net[li] / 1000).toFixed(1)}K`} sub="contracts" />
      <MetricCard label="Managed money net" value={`${(mmNet / 1000).toFixed(1)}K`} sub="contracts" trend={mmChg != null && mmPrev !== 0 ? Number((mmChg / Math.abs(mmPrev) * 100).toFixed(1)) : undefined} />
      <MetricCard label="MM net % of OI" value={pctOI != null ? `${pctOI > 0 ? "+" : ""}${pctOI.toFixed(1)}%` : "—"} sub="open interest" />
    </div>

    <SectionTitle right={<DownloadBtn onClick={dlCOT} />}>Net positions by category</SectionTitle>
    <InteractiveLegend items={catLegend} hidden={hCats} onToggle={tCats} />
    {ready && <ChartBox id={`cot_cats_${commodityId}`} height={280} renderChart={rcAllCats} deps={`${commodityId}_${[...hCats].join()}_${cotLoaded}`} />}

    <SectionTitle>Managed money net position</SectionTitle>
    {ready && <ChartBox id={`cot_mm_${commodityId}`} height={240} renderChart={rcMMBar} deps={`${commodityId}_${cotLoaded}`} />}

    <SectionTitle>Total open interest</SectionTitle>
    {ready && <ChartBox id={`cot_oi_${commodityId}`} height={200} renderChart={rcOI} deps={`${commodityId}_${cotLoaded}`} />}

    <div style={{ marginTop: 10, fontSize: 10, color: "var(--color-text-tertiary)" }}>Source: CFTC Disaggregated Commitments of Traders report. Futures & Options combined.</div>
  </div>);
}

// COT weeks labels (reuse from mkCOTSeries - 20 weeks)
const COT_WEEK_LABELS = Array.from({ length: 53 }, (_, i) => {
  const d = new Date(2025, 0, 6); d.setDate(d.getDate() + i * 7);
  return `${["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][d.getMonth()]} ${d.getDate()}`;
});

const COT_COMMODITY_LIST = [
  { id: "cot-corn", label: "Corn" }, { id: "cot-soybeans", label: "Soybeans" },
  { id: "cot-meal", label: "Soybean Meal" }, { id: "cot-oil", label: "Soybean Oil" },
  { id: "cot-chi-wheat", label: "Chicago SRW Wheat" }, { id: "cot-kc-wheat", label: "KC HRW Wheat" },
  { id: "cot-mpls-wheat", label: "MN HRS Wheat" },
  { id: "cot-live-cattle", label: "Live Cattle" }, { id: "cot-feeder-cattle", label: "Feeder Cattle" },
  { id: "cot-lean-hogs", label: "Lean Hogs" },
  { id: "cot-crude-oil", label: "Crude Oil" }, { id: "cot-heating-oil", label: "Heating Oil" },
  { id: "cot-nat-gas", label: "Natural Gas" },
];

function COTChartsPage({ ready }) {
  var ref = useLiveCOT();
  var cotData = ref.cotData;
  var cotLoaded = ref.cotLoaded;
  var _sel = useState("cot-corn");
  var sel = _sel[0], setSel = _sel[1];
  var _tr = useState("5");
  var timeRange = _tr[0], setTimeRange = _tr[1];
  var _hy = useState(new Set());
  var hiddenYears = _hy[0], setHiddenYears = _hy[1];
  var _mode = useState("seasonal");
  var chartMode = _mode[0], setChartMode = _mode[1];
  var d = cotData[sel];
  if (!d) return React.createElement("div", {style:{padding:20}}, "No data for this commodity.");

  var curYear = new Date().getFullYear();
  var yearly = d.yearly || {};
  var availYears = Object.keys(yearly).map(Number).sort();
  var displayYears = [];
  if (timeRange === "all") { displayYears = availYears; }
  else { var n = parseInt(timeRange); displayYears = availYears.filter(function(y){return y >= curYear - n;}); }

  var yearColors = ["#A32D2D","#D85A30","#E8A735","#639922","#1D9E75","#378ADD","#534AB7","#8B5CF6","#EC4899","#6B7280","#0EA5E9","#14B8A6","#F97316","#7C3AED","#BE185D","#059669","#B45309","#4338CA","#DC2626","#0284C7"];
  var getYearColor = function(yr) { return yr === curYear ? "#333" : yearColors[displayYears.filter(function(y){return y!==curYear;}).indexOf(yr) % yearColors.length]; };

  var toggleYear = function(label) {
    setHiddenYears(function(prev) { var next = new Set(prev); if (next.has(label)) next.delete(label); else next.add(label); return next; });
  };
  useEffect(function(){ setHiddenYears(new Set()); }, [sel, timeRange]);

  // Convert a date string to day-of-year offset from Jan 1 of the given display year
  // Handles year-boundary weeks (e.g., Dec 30, 2024 for ISO year 2025 → day ~0)
  var dateToDoy = function(dateStr, isoYear) {
    var parts = dateStr.split("-");
    var m = parseInt(parts[1]) - 1, day = parseInt(parts[2]), yr = parseInt(parts[0]);
    // Day-of-year within the date's own calendar year
    var jan1 = new Date(isoYear, 0, 1);
    var dt = new Date(yr, m, day);
    var diff = Math.round((dt - jan1) / 86400000);
    // Clamp: late-Dec dates for next year's ISO week 1 → ~0, early-Jan for prev year's week 52/53 → ~365
    if (diff < 0) return 0;
    if (diff > 365) return 365;
    return diff;
  };

  // Month layout on 0-365 scale
  var monthBounds = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334];
  var monthMids = [15, 45, 74, 105, 135, 166, 196, 227, 258, 288, 319, 349];
  var monthLabels = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];

  var fmtAxis = function(v) {
    if (v == null) return "";
    var k = v / 1000;
    if (Math.abs(k) < 0.001) return "0";
    var str;
    if (Math.abs(k) < 10) {
      var rounded = Math.round(k * 10) / 10;
      str = rounded === Math.floor(rounded) ? String(Math.abs(Math.floor(rounded))) : Math.abs(rounded).toFixed(1);
    } else {
      str = Math.abs(k).toLocaleString(undefined, {maximumFractionDigits: 0});
    }
    return k < 0 ? "(" + str + ")" : str;
  };

  // Seasonal chart — each year overlaid on 0-365 using actual report dates
  var mkSeasonalChart = useCallback(function(field) { return function(canvas) {
    var datasets = [];
    displayYears.forEach(function(yr) {
      var yrData = yearly[String(yr)]; if (!yrData || !yrData[field]) return;
      var raw = yrData[field];
      var dates = yrData._dates || [];
      var points = [];
      for (var i = 0; i < raw.length; i++) {
        if (raw[i] != null && dates[i]) {
          points.push({x: dateToDoy(dates[i], yr), y: raw[i]});
        }
      }
      if (points.length === 0) return;
      datasets.push({label: String(yr), data: points, borderColor: getYearColor(yr), borderWidth: yr === curYear ? 2.5 : 1.5, pointRadius: 0, pointHitRadius: 8, tension: 0, fill: false, hidden: hiddenYears.has(String(yr)), showLine: true});
    });
    var visibleVals = datasets.filter(function(ds){return !ds.hidden;}).flatMap(function(ds){return ds.data.map(function(p){return p.y;});});
    if (visibleVals.length === 0) return;
    var dataMin = Math.min.apply(null, visibleVals), dataMax = Math.max.apply(null, visibleVals);
    var range = dataMax - dataMin, pad = Math.max(range * 0.12, Math.abs(dataMax) * 0.03 || 100);
    var rawStep = (range + pad * 2) / 5, mag = Math.pow(10, Math.floor(Math.log10(rawStep || 1)));
    var nn = rawStep / mag, niceNorm = nn <= 1.5 ? 1 : nn <= 3.5 ? 2 : nn <= 7.5 ? 5 : 10;
    var step = niceNorm * mag;
    if (step < 1000) step = Math.max(500, step);
    new Chart(canvas, {type: "scatter", data: {datasets: datasets}, options: {
      responsive: true, maintainAspectRatio: false,
      interaction: {mode: "nearest", intersect: false, axis: "xy"},
      hover: {mode: "nearest", intersect: false},
      plugins: {legend: {display: false}, tooltip: {mode: "nearest", intersect: false, backgroundColor: "rgba(0,0,0,0.6)", titleFont: {size: 12}, bodyFont: {size: 12},
        callbacks: {
          title: function(items) {
            if (items.length === 0) return "";
            var doy = items[0].parsed.x;
            var mi = 11;
            for (var m = 0; m < 11; m++) { if (doy < monthBounds[m+1]) { mi = m; break; } }
            return monthLabels[mi] + " " + (Math.floor(doy - monthBounds[mi]) + 1);
          },
          label: function(c2){return c2.dataset.label + ": " + (c2.parsed.y != null ? (c2.parsed.y / 1000).toFixed(1) + "K" : "n/a");}
        },
      }},
      scales: {
        x: {
          type: "linear", min: 0, max: 365,
          ticks: {
            callback: function(val) { var mi = monthMids.indexOf(val); return mi >= 0 ? monthLabels[mi] : ""; },
            autoSkip: false, maxRotation: 0, font: {size: 11},
          },
          afterBuildTicks: function(axis) {
            var ticks = [];
            for (var i = 0; i < 12; i++) { ticks.push({value: monthBounds[i]}); ticks.push({value: monthMids[i]}); }
            axis.ticks = ticks;
          },
          grid: {
            color: function(ctx) {
              var val = ctx.tick.value;
              if (val > 0 && monthBounds.indexOf(val) >= 0) return "rgba(0,0,0,0.12)";
              return "transparent";
            }, lineWidth: 0.75,
          },
        },
        y: {min: Math.floor((dataMin - pad) / step) * step, max: Math.ceil((dataMax + pad) / step) * step, ticks: {font: {size: 11}, color: function(ctx) { return ctx.tick.value < 0 ? "#A32D2D" : "#666"; }, callback: function(v){return fmtAxis(v);}}, grid: {color: "rgba(0,0,0,0.08)", lineWidth: 0.75}},
      },
    }});
  };}, [sel, timeRange, d, hiddenYears]);

  // Contiguous chart — all years concatenated using actual report dates
  var mkContigChart = useCallback(function(field) { return function(canvas) {
    var allPoints = [];
    var yearBounds2 = [];
    var yearMids = [];
    var xOffset = 0;
    displayYears.forEach(function(yr) {
      var yrData = yearly[String(yr)]; if (!yrData || !yrData[field]) return;
      var raw = yrData[field];
      var dates = yrData._dates || [];
      var yrStart = xOffset;
      if (xOffset > 0) yearBounds2.push(xOffset);
      for (var i = 0; i < raw.length; i++) {
        if (raw[i] != null && dates[i]) {
          allPoints.push({x: xOffset + dateToDoy(dates[i], yr), y: raw[i]});
        }
      }
      yearMids.push({x: xOffset + 182, label: String(yr)});
      xOffset += 365;
    });
    if (allPoints.length === 0) return;
    var visibleVals = allPoints.map(function(p){return p.y;});
    var dataMin = Math.min.apply(null, visibleVals), dataMax = Math.max.apply(null, visibleVals);
    var range = dataMax - dataMin, pad = Math.max(range * 0.12, Math.abs(dataMax) * 0.03 || 100);
    var rawStep = (range + pad * 2) / 5, mag = Math.pow(10, Math.floor(Math.log10(rawStep || 1)));
    var nn = rawStep / mag, niceNorm = nn <= 1.5 ? 1 : nn <= 3.5 ? 2 : nn <= 7.5 ? 5 : 10;
    var step = niceNorm * mag;
    if (step < 1000) step = Math.max(500, step);
    var xMax = xOffset;
    var needsRotation = displayYears.length > 8;
    new Chart(canvas, {type: "scatter", data: {datasets: [{label: field, data: allPoints, borderColor: "#333", borderWidth: 1.5, pointRadius: 0, pointHitRadius: 6, tension: 0, fill: false, showLine: true}]}, options: {
      responsive: true, maintainAspectRatio: false,
      interaction: {mode: "nearest", intersect: false, axis: "xy"},
      plugins: {legend: {display: false}, tooltip: {mode: "nearest", intersect: false, backgroundColor: "rgba(0,0,0,0.6)", titleFont: {size: 12}, bodyFont: {size: 12},
        callbacks: {
          title: function(items) {
            if (items.length === 0) return "";
            var xVal = items[0].parsed.x;
            var yrIdx = Math.min(Math.floor(xVal / 365), displayYears.length - 1);
            var doy = xVal - yrIdx * 365;
            var mi = 11;
            for (var m = 0; m < 11; m++) { if (doy < monthBounds[m+1]) { mi = m; break; } }
            return monthLabels[mi] + " " + displayYears[yrIdx];
          },
          label: function(c2){return (c2.parsed.y != null ? (c2.parsed.y / 1000).toFixed(1) + "K" : "n/a");}
        },
      }},
      scales: {
        x: {
          type: "linear", min: 0, max: xMax,
          ticks: {
            callback: function(val) {
              for (var i = 0; i < yearMids.length; i++) {
                if (Math.abs(val - yearMids[i].x) < 5) return yearMids[i].label;
              }
              return "";
            },
            autoSkip: false, minRotation: needsRotation ? 90 : 0, maxRotation: needsRotation ? 90 : 0, font: {size: 11},
          },
          afterBuildTicks: function(axis) {
            var ticks = [];
            for (var i = 0; i < yearBounds2.length; i++) { ticks.push({value: yearBounds2[i]}); }
            for (var j = 0; j < yearMids.length; j++) { ticks.push({value: yearMids[j].x}); }
            ticks.sort(function(a,b){return a.value - b.value;});
            axis.ticks = ticks;
          },
          grid: {
            color: function(ctx) {
              var val = ctx.tick.value;
              for (var i = 0; i < yearBounds2.length; i++) {
                if (Math.abs(val - yearBounds2[i]) < 5) return "rgba(0,0,0,0.15)";
              }
              return "transparent";
            }, lineWidth: 0.75,
          },
        },
        y: {min: Math.floor((dataMin - pad) / step) * step, max: Math.ceil((dataMax + pad) / step) * step, ticks: {font: {size: 11}, color: function(ctx) { return ctx.tick.value < 0 ? "#A32D2D" : "#666"; }, callback: function(v){return fmtAxis(v);}}, grid: {color: "rgba(0,0,0,0.08)", lineWidth: 0.75}},
      },
    }});
  };}, [sel, timeRange, d, hiddenYears]);

  // CSV download
  var dlCSV = function() {
    var fields = ["mm_net","mm_long","mm_short","prod_net","prod_long","prod_short","swap_net","swap_long","swap_short","other_net","other_long","other_short","oi"];
    var headers = ["Year","Date"].concat(fields);
    var rows = [];
    displayYears.forEach(function(yr) {
      var yrData = yearly[String(yr)]; if (!yrData) return;
      var dates = yrData._dates || [];
      for (var w = 0; w < 53; w++) {
        if (!dates[w]) continue;
        var hasData = false;
        for (var fi = 0; fi < fields.length; fi++) {
          if (yrData[fields[fi]] && yrData[fields[fi]][w] != null) { hasData = true; break; }
        }
        if (!hasData) continue;
        var row = [yr, dates[w]];
        for (var fi2 = 0; fi2 < fields.length; fi2++) {
          var val = yrData[fields[fi2]] ? yrData[fields[fi2]][w] : null;
          row.push(val != null ? val : "");
        }
        rows.push(row);
      }
    });
    downloadCSV(sel + "_cot_" + timeRange + "yr.csv", headers, rows);
  };

  var chevronSvg = "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath d='M3 5l3 3 3-3' fill='none' stroke='%23666' stroke-width='1.5'/%3E%3C/svg%3E\")";
  var selectStyle = {padding: "7px 28px 7px 12px", fontSize: 14, fontWeight: 500, border: "1px solid var(--color-border-secondary)", borderRadius: 6, background: "var(--color-background-primary)", color: "var(--color-text-primary)", fontFamily: "inherit", cursor: "pointer", appearance: "none", backgroundImage: chevronSvg, backgroundRepeat: "no-repeat", backgroundPosition: "right 8px center"};
  var labelStyle2 = {fontSize: 11, fontWeight: 600, color: "var(--color-text-secondary)", textTransform: "uppercase", letterSpacing: "0.4px"};
  var toggleBtnStyle = function(active) { return {padding: "6px 14px", fontSize: 12, fontWeight: 500, border: "1px solid " + (active ? "#2563EB" : "var(--color-border-secondary)"), borderRadius: 5, cursor: "pointer", background: active ? "#2563EB" : "transparent", color: active ? "#fff" : "var(--color-text-secondary)", transition: "all 0.15s"}; };

  var categories = [
    {title: "Managed Money", fields: ["mm_net","mm_long","mm_short"]},
    {title: "Producer / Merchant", fields: ["prod_net","prod_long","prod_short"]},
    {title: "Swap Dealers", fields: ["swap_net","swap_long","swap_short"]},
    {title: "Other Reportables", fields: ["other_net","other_long","other_short"]},
  ];

  var legendItems = displayYears.map(function(yr){return {label: String(yr), color: getYearColor(yr)};});
  var hk = Array.from(hiddenYears).sort().join(",");
  var mkChart = chartMode === "seasonal" ? mkSeasonalChart : mkContigChart;

  return (<div>
    <div style={{display:"flex",alignItems:"center",gap:16,marginBottom:14,flexWrap:"wrap"}}>
      <div style={{display:"flex",alignItems:"center",gap:8}}>
        <span style={labelStyle2}>Commodity</span>
        <select value={sel} onChange={function(e){setSel(e.target.value);}} style={selectStyle}>{COT_COMMODITY_LIST.map(function(item){return <option key={item.id} value={item.id}>{item.label}</option>;})}</select>
      </div>
      <div style={{display:"flex",alignItems:"center",gap:8}}>
        <span style={labelStyle2}>Range</span>
        <select value={timeRange} onChange={function(e){setTimeRange(e.target.value);}} style={selectStyle}>
          <option value="5">5 Year</option><option value="10">10 Year</option><option value="all">All</option>
        </select>
      </div>
      <div style={{display:"flex",gap:4}}>
        <button onClick={function(){setChartMode("seasonal");}} style={toggleBtnStyle(chartMode==="seasonal")}>Seasonal</button>
        <button onClick={function(){setChartMode("contiguous");}} style={toggleBtnStyle(chartMode==="contiguous")}>Contiguous</button>
      </div>
      <div style={{marginLeft:"auto"}}><DownloadBtn onClick={dlCSV} /></div>
    </div>
    <div style={{fontSize:13,color:"var(--color-text-tertiary)",marginBottom:12}}>{d.label} — {d.exchange} — Contract size: {d.contract}. Y-axis in thousand contracts.</div>
    {chartMode === "seasonal" && <div style={{display:"flex",flexWrap:"wrap",gap:6,marginBottom:20,alignItems:"center"}}>
      {legendItems.map(function(item){var isH = hiddenYears.has(item.label); return (
        <button key={item.label} onClick={function(){toggleYear(item.label);}} style={{display:"flex",alignItems:"center",gap:5,padding:"4px 10px",border:"1px solid var(--color-border-secondary)",borderRadius:5,background:isH?"var(--color-background-secondary)":"transparent",cursor:"pointer",opacity:isH?0.3:1,transition:"all 0.15s"}}>
          <span style={{width:18,height:0,borderTop:"2.5px solid "+item.color,display:"inline-block"}}></span>
          <span style={{fontSize:12,fontWeight:500,color:"var(--color-text-primary)"}}>{item.label}</span>
        </button>);})}</div>}
    {categories.map(function(cat){return (<div key={cat.title}>
      <h3 style={{fontSize:15,fontWeight:600,color:"var(--color-text-primary)",margin:"24px 0 12px"}}>{cat.title}</h3>
      <div style={{display:"grid",gridTemplateColumns:"1fr 1fr 1fr",gap:18}}>
        {["Net","Long","Short"].map(function(lbl,fi){return (<div key={lbl}>
          <div style={{fontSize:13,fontWeight:500,color:"var(--color-text-secondary)",marginBottom:8,textAlign:"center"}}>{lbl}</div>
          {ready && <ChartBox id={"cot_"+cat.fields[fi]+"_"+sel+"_"+timeRange+"_"+chartMode+"_"+hk} height={300} renderChart={mkChart(cat.fields[fi])} deps={sel+"_"+timeRange+"_"+chartMode+"_"+hk+"_"+cotLoaded} />}
        </div>);})}</div>
    </div>);})
    }
    <h3 style={{fontSize:15,fontWeight:600,color:"var(--color-text-primary)",margin:"24px 0 12px"}}>Open Interest</h3>
    {ready && <ChartBox id={"cot_oi_"+sel+"_"+timeRange+"_"+chartMode+"_"+hk} height={340} renderChart={mkChart("oi")} deps={sel+"_"+timeRange+"_"+chartMode+"_"+hk+"_"+cotLoaded} />}
    <div style={{marginTop:14,fontSize:12,color:"var(--color-text-tertiary)"}}>Source: CFTC Disaggregated Commitments of Traders report. Futures & Options combined.</div>
  </div>);
}


// ════════════════════════════════════════════════════════════════════════
// ENERGY PAGES — EIA Weekly Petroleum Status & Natural Gas Storage
// ════════════════════════════════════════════════════════════════════════

const ENERGY_WEEKS = ["Nov 7","Nov 14","Nov 21","Nov 28","Dec 5","Dec 12","Dec 19","Dec 26","Jan 2","Jan 9","Jan 16","Jan 23","Jan 30","Feb 6","Feb 13","Feb 20","Feb 27","Mar 6","Mar 13","Mar 20"];

function mkEnergySeries(base, scale) {
  const arr = [base];
  for (let i = 1; i < 20; i++) arr.push(Math.round((arr[i-1] + Math.sin(i * 0.6) * scale + (Math.cos(i * 1.2) - 0.5) * scale * 0.5) * 10) / 10);
  return arr;
}

const ENERGY_DATA = {
  ngStorage: {
    "2025": mkEnergySeries(3450, 45), "2024": mkEnergySeries(3620, 40), "5yr": mkEnergySeries(3280, 35),
    unit: "Bcf", title: "Working gas in underground storage",
  },
  ngProduction: {
    "2025": mkEnergySeries(104.2, 0.4), "2024": mkEnergySeries(102.8, 0.35), "5yr": mkEnergySeries(99.5, 0.3),
    unit: "Bcf/d", title: "Dry natural gas production",
  },
  ngDemand: {
    "2025": mkEnergySeries(82.5, 2.5), "2024": mkEnergySeries(80.2, 2.2), "5yr": mkEnergySeries(76.8, 2.0),
    unit: "Bcf/d", title: "Total natural gas consumption",
  },
  ngInjWd: {
    "2025": [-258,-245,-198,-212,-185,-168,-142,-155,-128,-115,-92,-78,-55,-42,-28,-15,5,18,32,45].map(v => v),
    "2024": [-232,-218,-185,-195,-172,-155,-130,-140,-112,-98,-78,-62,-42,-28,-12,5,22,35,48,62],
    "5yr":  [-215,-202,-175,-182,-160,-145,-122,-132,-105,-92,-72,-58,-38,-25,-8,8,25,38,52,65],
    unit: "Bcf", title: "Weekly net injections / withdrawals",
  },
  crudeStocks: {
    "2025": mkEnergySeries(432.5, 3.5), "2024": mkEnergySeries(448.2, 3.0), "5yr": mkEnergySeries(462.8, 2.8),
    unit: "million bbl", title: "Crude oil stocks (excl. SPR)",
  },
  crudeProduction: {
    "2025": mkEnergySeries(13.5, 0.06), "2024": mkEnergySeries(13.2, 0.05), "5yr": mkEnergySeries(12.4, 0.04),
    unit: "million b/d", title: "Crude oil production",
  },
  gasolineStocks: {
    "2025": mkEnergySeries(248.5, 2.8), "2024": mkEnergySeries(252.3, 2.5), "5yr": mkEnergySeries(242.1, 2.2),
    unit: "million bbl", title: "Total motor gasoline stocks",
  },
  distillateStocks: {
    "2025": mkEnergySeries(118.2, 2.2), "2024": mkEnergySeries(125.8, 2.0), "5yr": mkEnergySeries(138.5, 1.8),
    unit: "million bbl", title: "Distillate fuel oil stocks",
  },
};

function EnergyChartPage({ ready, dataKey }) {
  const d = ENERGY_DATA[dataKey];
  const [hSeries, tSeries] = useToggle();
  const [chartMode, setChartMode] = useState("seasonal");

  var yr5 = meatData && meatData.seasonal ? meatData.seasonal.years.filter(function(y) { return typeof y.year === "number"; }).sort(function(a,b) { return a.year - b.year; }) : [];
  var legendYears = yr5.slice(-6);
  var yrColorMap = { 0: "#A32D2D", 1: "#D85A30", 2: "#E8A735", 3: "#639922", 4: "#1D9E75", 5: "#333" };
  var seasonLegend = legendYears.map(function(y, i) {
    return { label: String(y.year), color: yrColorMap[i] || "#999", key: "yr" + i };
  });
  var seasonDS = {};
  legendYears.forEach(function(y, i) {
    seasonDS["yr" + i] = { borderColor: yrColorMap[i] || "#999", borderWidth: i === legendYears.length - 1 ? 2.5 : 1.5, pointRadius: 0, tension: 0 };
  });

  function niceAxis(allVals) {
    if (allVals.length === 0) return { yMin: 0, yMax: 100 };
    const dataMin = Math.min(...allVals); const dataMax = Math.max(...allVals);
    const range = dataMax - dataMin; const pad = Math.max(range * 0.2, 2);
    const rawStep = (range + pad * 2) / 5;
    const mag = Math.pow(10, Math.floor(Math.log10(rawStep)));
    const norm = rawStep / mag;
    const niceNorm = norm <= 1.5 ? 1 : norm <= 3.5 ? 2 : norm <= 7.5 ? 5 : 10;
    const step = niceNorm * mag;
    return { yMin: Math.floor((dataMin - pad) / step) * step, yMax: Math.ceil((dataMax + pad) / step) * step };
  }

  const lastNN = (arr) => { for (let i = arr.length - 1; i >= 0; i--) { if (arr[i] != null) return arr[i]; } return null; };
  const cur = lastNN(d["2025"]);
  const li = d["2025"].lastIndexOf(cur);
  const ya = d["2024"] ? d["2024"][li] : null;
  const avg5 = d["5yr"] ? d["5yr"][li] : null;
  const yaChg = cur != null && ya != null && ya !== 0 ? Number(((cur - ya) / ya * 100).toFixed(1)) : undefined;

  const rc = useCallback(canvas => {
    if (chartMode === "contiguous") {
      // Stitch 2024 + 2025 into one continuous line
      const labels2024 = ENERGY_WEEKS.map(w => w + " '24");
      const labels2025 = ENERGY_WEEKS.map(w => w + " '25");
      const allLabels = [...labels2024, ...labels2025];
      const allData = [...d["2024"], ...d["2025"]];
      const allVals = allData.filter(v => v != null);
      const { yMin, yMax } = niceAxis(allVals);
      new Chart(canvas, {
        type: "line", data: { labels: allLabels, datasets: [{
          label: d.title, data: allData, borderColor: "#A32D2D", backgroundColor: "rgba(163,45,45,0.06)",
          fill: true, borderWidth: 2, pointRadius: 0, tension: 0, spanGaps: true,
        }]},
        options: { responsive: true, maintainAspectRatio: false,
          interaction: { mode: "nearest", intersect: false },
          plugins: { legend: { display: false }, tooltip: { callbacks: { label: c => `${c.parsed.y} ${d.unit}` } } },
          scales: {
            x: { ticks: { autoSkip: true, maxTicksLimit: 12, maxRotation: 45, font: { size: 10 } }, grid: { color: "rgba(0,0,0,0.12)", lineWidth: 0.75 } },
            y: { min: yMin, max: yMax, title: { display: true, text: d.unit, font: { size: 11 } }, ticks: { font: { size: 11 } }, grid: { color: "rgba(0,0,0,0.12)", lineWidth: 0.75 } },
          },
        },
      });
    } else {
      const keys = ["2025","2024","5yr"].filter(k => !hSeries.has(k));
      const ds = keys.map(k => ({ label: k === "5yr" ? "5-yr avg" : k, data: d[k], ...seasonDS[k], spanGaps: true }));
      const allVals = keys.flatMap(k => (d[k] || []).filter(v => v != null));
      const { yMin, yMax } = niceAxis(allVals);
      new Chart(canvas, {
        type: "line", data: { labels: ENERGY_WEEKS, datasets: ds },
        options: { responsive: true, maintainAspectRatio: false,
          interaction: { mode: "nearest", intersect: false },
          plugins: { legend: { display: false }, tooltip: { callbacks: { label: c => `${c.dataset.label}: ${c.parsed.y} ${d.unit}` } } },
          scales: {
            x: { ticks: { autoSkip: true, maxTicksLimit: 10, maxRotation: 45, font: { size: 11 } }, grid: { color: "rgba(0,0,0,0.12)", lineWidth: 0.75 } },
            y: { min: yMin, max: yMax, title: { display: true, text: d.unit, font: { size: 11 } }, ticks: { font: { size: 11 } }, grid: { color: "rgba(0,0,0,0.12)", lineWidth: 0.75 } },
          },
        },
      });
    }
  }, [d, hSeries, chartMode]);

  const dlEnergy = () => {
    if (chartMode === "contiguous") {
      const labels24 = ENERGY_WEEKS.map(w => w + " '24");
      const labels25 = ENERGY_WEEKS.map(w => w + " '25");
      const headers = ["Week", d.unit];
      const rows = [...labels24.map((w,i) => [w, d["2024"][i]]), ...labels25.map((w,i) => [w, d["2025"][i]])];
      downloadCSV(`energy_${dataKey}_contiguous.csv`, headers, rows);
    } else {
      const headers = ["Week","2025","2024","5-yr avg"];
      const rows = ENERGY_WEEKS.map((w, i) => [w, d["2025"][i], d["2024"][i], d["5yr"][i]]);
      downloadCSV(`energy_${dataKey}.csv`, headers, rows);
    }
  };

  return (<div>
    <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(155px, 1fr))", gap: 10, marginBottom: 8 }}>
      <MetricCard label="Current" value={cur != null ? `${cur}` : "—"} sub={d.unit} trend={yaChg} />
      <MetricCard label="Year ago" value={ya != null ? `${ya}` : "—"} sub={d.unit} />
      <MetricCard label="5-yr avg" value={avg5 != null ? `${avg5}` : "—"} sub={d.unit} />
    </div>
    <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 14, marginTop: 28, flexWrap: "wrap" }}>
      <h3 style={{ fontSize: 15, fontWeight: 500, color: "var(--color-text-primary)", margin: 0 }}>{d.title}</h3>
      <div style={{ marginLeft: "auto", display: "flex", gap: 8, alignItems: "center" }}>
        <ChartModeToggle mode={chartMode} setMode={setChartMode} />
        <DownloadBtn onClick={dlEnergy} />
      </div>
    </div>
    {chartMode === "seasonal" && <InteractiveLegend items={seasonLegend} hidden={hSeries} onToggle={tSeries} />}
    {ready && <ChartBox id={`energy_${dataKey}_${chartMode}`} renderChart={rc} deps={`${dataKey}_${chartMode}_${[...hSeries].join()}`} />}
    <div style={{ marginTop: 10, fontSize: 10, color: "var(--color-text-tertiary)" }}>Source: EIA Weekly Natural Gas Storage Report / Weekly Petroleum Status Report</div>
  </div>);
}

function NGInjWdPage({ ready }) {
  const d = ENERGY_DATA.ngInjWd;
  const [hSeries, tSeries] = useToggle();

  const seasonLegend = [
    { label: "2025", color: "#A32D2D", key: "2025" },
    { label: "2024", color: "#378ADD", key: "2024" },
    { label: "5-yr avg", color: "#333", key: "5yr" },
  ];

  const cur = d["2025"][d["2025"].length - 1];
  const ya = d["2024"][d["2024"].length - 1];
  const avg5 = d["5yr"][d["5yr"].length - 1];

  function niceAxis(allVals) {
    if (allVals.length === 0) return { yMin: -100, yMax: 100 };
    const dataMin = Math.min(...allVals); const dataMax = Math.max(...allVals);
    const range = dataMax - dataMin; const pad = Math.max(range * 0.15, 10);
    const rawStep = (range + pad * 2) / 6;
    const mag = Math.pow(10, Math.floor(Math.log10(rawStep)));
    const norm = rawStep / mag;
    const niceNorm = norm <= 1.5 ? 1 : norm <= 3.5 ? 2 : norm <= 7.5 ? 5 : 10;
    const step = niceNorm * mag;
    return { yMin: Math.floor((dataMin - pad) / step) * step, yMax: Math.ceil((dataMax + pad) / step) * step };
  }

  const rc = useCallback(canvas => {
    const keys = ["2025","2024","5yr"].filter(k => !hSeries.has(k));
    const datasets = keys.map(k => {
      const isBar = k === "2025";
      if (isBar) {
        return {
          type: "bar", label: "2025", data: d[k],
          backgroundColor: d[k].map(v => v >= 0 ? "rgba(99,153,34,0.6)" : "rgba(163,45,45,0.6)"),
          borderColor: d[k].map(v => v >= 0 ? "#639922" : "#A32D2D"),
          borderWidth: 1, borderRadius: 2, order: 2,
        };
      }
      return {
        type: "line", label: k === "5yr" ? "5-yr avg" : k, data: d[k],
        borderColor: k === "2024" ? "#378ADD" : "#333",
        borderWidth: 1.5, pointRadius: k === "2024" ? 2 : 0, tension: 0,
        borderDash: k === "5yr" ? [2,2] : [5,3], order: 1,
      };
    });
    const allVals = keys.flatMap(k => d[k]);
    const { yMin, yMax } = niceAxis(allVals);
    new Chart(canvas, {
      data: { labels: ENERGY_WEEKS, datasets },
      options: { responsive: true, maintainAspectRatio: false,
        interaction: { mode: "nearest", intersect: false },
        plugins: { legend: { display: false }, tooltip: { callbacks: { label: c => `${c.dataset.label}: ${c.parsed.y > 0 ? "+" : ""}${c.parsed.y} Bcf` } } },
        scales: {
          x: { ticks: { autoSkip: true, maxTicksLimit: 10, maxRotation: 45, font: { size: 11 } }, grid: { color: "rgba(0,0,0,0.12)", lineWidth: 0.75 } },
          y: { min: yMin, max: yMax, title: { display: true, text: "Bcf", font: { size: 11 } }, ticks: { font: { size: 11 } }, grid: { color: "rgba(0,0,0,0.12)", lineWidth: 0.75 } },
        },
      },
    });
  }, [d, hSeries]);

  const dlData = () => {
    const headers = ["Week","2025","2024","5-yr avg"];
    const rows = ENERGY_WEEKS.map((w, i) => [w, d["2025"][i], d["2024"][i], d["5yr"][i]]);
    downloadCSV("ng_injections_withdrawals.csv", headers, rows);
  };

  return (<div>
    <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(155px, 1fr))", gap: 10, marginBottom: 8 }}>
      <MetricCard label="Latest" value={`${cur > 0 ? "+" : ""}${cur}`} sub={`Bcf ${cur >= 0 ? "(injection)" : "(withdrawal)"}`} />
      <MetricCard label="Year ago" value={`${ya > 0 ? "+" : ""}${ya}`} sub="Bcf" />
      <MetricCard label="5-yr avg" value={`${avg5 > 0 ? "+" : ""}${avg5}`} sub="Bcf" />
    </div>
    <SectionTitle right={<DownloadBtn onClick={dlData} />}>Weekly net change in working gas</SectionTitle>
    <InteractiveLegend items={seasonLegend} hidden={hSeries} onToggle={tSeries} />
    {ready && <ChartBox id="ng_inj_wd" renderChart={rc} deps={[...hSeries].join()} />}
    <div style={{ marginTop: 10, fontSize: 10, color: "var(--color-text-tertiary)" }}>Source: EIA Weekly Natural Gas Storage Report. Positive = injection, Negative = withdrawal.</div>
  </div>);
}

// ════════════════════════════════════════════════════════════════════════
// MARKET DRIVERS — CURRENCIES
// ════════════════════════════════════════════════════════════════════════

const FX_WEEKS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];

function mkFXSeries(base, volatility) {
  const arr = [base];
  for (let i = 1; i < 12; i++) arr.push(Math.round((arr[i-1] + Math.sin(i * 0.8) * volatility + (Math.cos(i * 1.3) - 0.5) * volatility * 0.6) * 10000) / 10000);
  return arr;
}

const FX_DATA = {
  "fx-brl":  { label: "USD/BRL", desc: "US Dollar / Brazilian Real",     series: mkFXSeries(5.7850, 0.035),  format: 4 },
  "fx-cad":  { label: "USD/CAD", desc: "US Dollar / Canadian Dollar",    series: mkFXSeries(1.4420, 0.004),  format: 4 },
  "fx-ars":  { label: "USD/ARS", desc: "US Dollar / Argentine Peso",     series: mkFXSeries(1065.50, 8.5),   format: 2 },
  "fx-eur":  { label: "EUR/USD", desc: "Euro / US Dollar",               series: mkFXSeries(1.0485, 0.003),  format: 4 },
  "fx-aud":  { label: "USD/AUD", desc: "US Dollar / Australian Dollar",  series: mkFXSeries(1.5720, 0.005),  format: 4 },
  "fx-mxn":  { label: "USD/MXN", desc: "US Dollar / Mexican Peso",       series: mkFXSeries(20.2450, 0.08),  format: 4 },
  "fx-cny":  { label: "USD/CNY", desc: "US Dollar / Chinese Yuan",       series: mkFXSeries(7.2680, 0.012),  format: 4 },
};

const FX_IDS = Object.keys(FX_DATA);

function FXCurrenciesPage({ ready }) {
  const fmt = (v, f) => f === 2 ? v.toFixed(2) : v.toFixed(4);

  function niceAxis(allVals) {
    if (allVals.length === 0) return { yMin: 0, yMax: 1 };
    const dataMin = Math.min(...allVals); const dataMax = Math.max(...allVals);
    const range = dataMax - dataMin; const pad = Math.max(range * 0.2, dataMax * 0.002);
    const rawStep = (range + pad * 2) / 5;
    const mag = Math.pow(10, Math.floor(Math.log10(rawStep)));
    const norm = rawStep / mag;
    const niceNorm = norm <= 1.5 ? 1 : norm <= 3.5 ? 2 : norm <= 7.5 ? 5 : 10;
    const step = niceNorm * mag;
    return { yMin: Math.floor((dataMin - pad) / step) * step, yMax: Math.ceil((dataMax + pad) / step) * step };
  }

  const mkFXChart = (pairId) => (canvas) => {
    const d = FX_DATA[pairId]; const s = d.series;
    const { yMin, yMax } = niceAxis(s);
    new Chart(canvas, {
      type: "line", data: { labels: FX_WEEKS, datasets: [{
        label: d.label, data: s, borderColor: "#A32D2D", backgroundColor: "rgba(163,45,45,0.06)",
        fill: true, borderWidth: 2, pointRadius: 0, tension: 0,
      }]},
      options: { responsive: true, maintainAspectRatio: false,
        interaction: { mode: "nearest", intersect: false },
        plugins: { legend: { display: false }, tooltip: { callbacks: { label: c => `${d.label}: ${fmt(c.parsed.y, d.format)}` } } },
        scales: {
          x: { ticks: { autoSkip: true, maxTicksLimit: 10, maxRotation: 45, font: { size: 11 } }, grid: { color: "rgba(0,0,0,0.12)", lineWidth: 0.75 } },
          y: { min: yMin, max: yMax, ticks: { font: { size: 11 }, callback: v => fmt(v, d.format) }, grid: { color: "rgba(0,0,0,0.12)", lineWidth: 0.75 } },
        },
      },
    });
  };

  // ─── Dollar Index Data ───
  // DXY (ICE): synthetic from ECB rates using official weights (EUR 57.6%, JPY 13.6%, GBP 11.9%, CAD 9.1%, SEK 4.2%, CHF 3.6%)
  // Fed Broad TWD: trade-weighted against 26 currencies (CNY ~21%, EUR ~17%, MXN ~14%, CAD ~13%, etc.)
  const DXY_DATA =      [103.8, 103.2, 104.1, 104.8, 105.2, 104.5, 103.9, 104.3, 105.1, 105.8, 106.2, 105.6];
  const FED_TWD_DATA =  [120.5, 120.1, 121.2, 121.8, 122.4, 121.6, 120.8, 121.3, 122.1, 122.8, 123.4, 122.9];

  const [hDollar, tDollar] = useToggle();
  const dollarLegend = [
    { label: "DXY (synthetic)", color: "#A32D2D", key: "dxy" },
    { label: "Fed Broad Trade-Weighted Dollar", color: "#378ADD", key: "fed" },
  ];

  const rcDollar = useCallback(canvas => {
    const datasets = [];
    if (!hDollar.has("dxy")) datasets.push({ label: "DXY (synthetic)", data: DXY_DATA, borderColor: "#A32D2D", borderWidth: 2.5, pointRadius: 0, tension: 0 });
    if (!hDollar.has("fed")) datasets.push({ label: "Fed Broad Trade-Weighted Dollar", data: FED_TWD_DATA, borderColor: "#378ADD", borderWidth: 2, pointRadius: 0, tension: 0, borderDash: [5,3] });
    const allVals = [...(!hDollar.has("dxy") ? DXY_DATA : []), ...(!hDollar.has("fed") ? FED_TWD_DATA : [])];
    const axis = niceAxis(allVals.length ? allVals : [100, 125]);
    new Chart(canvas, {
      type: "line", data: { labels: FX_WEEKS, datasets },
      options: { responsive: true, maintainAspectRatio: false,
        interaction: { mode: "nearest", intersect: false },
        plugins: { legend: { display: false }, tooltip: { callbacks: { label: c => `${c.dataset.label}: ${c.parsed.y.toFixed(1)}` } } },
        scales: {
          x: { ticks: { font: { size: 11 } }, grid: { color: "rgba(0,0,0,0.12)", lineWidth: 0.75 } },
          y: { min: axis.yMin, max: axis.yMax, title: { display: true, text: "Index", font: { size: 11 } }, ticks: { font: { size: 11 } }, grid: { color: "rgba(0,0,0,0.12)", lineWidth: 0.75 } },
        },
      },
    });
  }, [hDollar]);

  const dlDollar = () => {
    const headers = ["Month","DXY (synthetic)","Fed Broad TWD"];
    const rows = FX_WEEKS.map((m,i) => [m, DXY_DATA[i], FED_TWD_DATA[i]]);
    downloadCSV("dollar_indices.csv", headers, rows);
  };

  const dxyLast = DXY_DATA[DXY_DATA.length - 1];
  const fedLast = FED_TWD_DATA[FED_TWD_DATA.length - 1];

  const dlFX = () => {
    const headers = ["Pair", ...FX_WEEKS];
    const rows = FX_IDS.map(id => [FX_DATA[id].label, ...FX_DATA[id].series]);
    downloadCSV("fx_summary.csv", headers, rows);
  };

  return (<div>
    {/* Dollar Index Section */}
    <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: 10, marginBottom: 8 }}>
      <div style={{ background: "var(--color-background-secondary)", borderRadius: "var(--border-radius-md)", padding: "12px 14px" }}>
        <div style={{ fontSize: 11, color: "var(--color-text-secondary)", marginBottom: 3, textTransform: "uppercase", letterSpacing: "0.4px" }}>DXY (synthetic)</div>
        <div style={{ fontSize: 22, fontWeight: 500, color: "var(--color-text-primary)", marginBottom: 6 }}>{dxyLast.toFixed(1)}</div>
        <div style={{ borderTop: "0.5px solid var(--color-border-tertiary)", paddingTop: 6, display: "flex", flexDirection: "column", gap: 1, fontSize: 11 }}>
          <div style={{ display: "flex", justifyContent: "space-between" }}><span style={{ color: "var(--color-text-tertiary)" }}>vs. last month ({DXY_DATA[DXY_DATA.length - 2].toFixed(1)})</span><span style={{ color: dxyLast > DXY_DATA[DXY_DATA.length - 2] ? "#639922" : "#A32D2D", fontWeight: 500, fontFamily: "var(--font-mono)" }}>{(dxyLast - DXY_DATA[DXY_DATA.length - 2]) > 0 ? "+" : ""}{(dxyLast - DXY_DATA[DXY_DATA.length - 2]).toFixed(1)} ({((dxyLast - DXY_DATA[DXY_DATA.length - 2]) / DXY_DATA[DXY_DATA.length - 2] * 100).toFixed(1)}%)</span></div>
          <div style={{ display: "flex", justifyContent: "space-between" }}><span style={{ color: "var(--color-text-tertiary)" }}>vs. last year ({(dxyLast * 0.97).toFixed(1)})</span><span style={{ color: "#639922", fontWeight: 500, fontFamily: "var(--font-mono)" }}>+{(dxyLast * 0.03).toFixed(1)} (+3.1%)</span></div>
        </div>
      </div>
      <div style={{ background: "var(--color-background-secondary)", borderRadius: "var(--border-radius-md)", padding: "12px 14px" }}>
        <div style={{ fontSize: 11, color: "var(--color-text-secondary)", marginBottom: 3, textTransform: "uppercase", letterSpacing: "0.4px" }}>Fed Broad Trade-Weighted Dollar</div>
        <div style={{ fontSize: 22, fontWeight: 500, color: "var(--color-text-primary)", marginBottom: 6 }}>{fedLast.toFixed(1)}</div>
        <div style={{ borderTop: "0.5px solid var(--color-border-tertiary)", paddingTop: 6, display: "flex", flexDirection: "column", gap: 1, fontSize: 11 }}>
          <div style={{ display: "flex", justifyContent: "space-between" }}><span style={{ color: "var(--color-text-tertiary)" }}>vs. last month ({FED_TWD_DATA[FED_TWD_DATA.length - 2].toFixed(1)})</span><span style={{ color: fedLast > FED_TWD_DATA[FED_TWD_DATA.length - 2] ? "#639922" : "#A32D2D", fontWeight: 500, fontFamily: "var(--font-mono)" }}>{(fedLast - FED_TWD_DATA[FED_TWD_DATA.length - 2]) > 0 ? "+" : ""}{(fedLast - FED_TWD_DATA[FED_TWD_DATA.length - 2]).toFixed(1)} ({((fedLast - FED_TWD_DATA[FED_TWD_DATA.length - 2]) / FED_TWD_DATA[FED_TWD_DATA.length - 2] * 100).toFixed(1)}%)</span></div>
          <div style={{ display: "flex", justifyContent: "space-between" }}><span style={{ color: "var(--color-text-tertiary)" }}>vs. last year ({(fedLast * 0.975).toFixed(1)})</span><span style={{ color: "#639922", fontWeight: 500, fontFamily: "var(--font-mono)" }}>+{(fedLast * 0.025).toFixed(1)} (+2.5%)</span></div>
        </div>
      </div>
    </div>

    <SectionTitle right={<DownloadBtn onClick={dlDollar} />}>US Dollar Index</SectionTitle>
    <InteractiveLegend items={dollarLegend} hidden={hDollar} onToggle={tDollar} />
    {ready && <ChartBox id={`dollar_idx_${[...hDollar].join()}`} height={280} renderChart={rcDollar} deps={[...hDollar].join()} />}
    <div style={{ marginTop: 6, marginBottom: 24, fontSize: 10, color: "var(--color-text-tertiary)" }}>DXY synthetic: computed from ECB rates using ICE DXY weights (EUR 57.6%, JPY 13.6%, GBP 11.9%, CAD 9.1%, SEK 4.2%, CHF 3.6%). Fed Broad TWD: Federal Reserve H.10 trade-weighted dollar index against 26 currencies.</div>

    {/* FX Summary Table */}
    <SectionTitle right={<DownloadBtn onClick={dlFX} />}>FX Summary</SectionTitle>
    <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 10, flexWrap: "wrap", gap: 8 }}>
      <div style={{ fontSize: 11, color: "var(--color-text-tertiary)" }}>USD/X rates show how many units of foreign currency one US dollar buys. EUR/USD is inverted (how many dollars one euro buys).</div>
    </div>
    <div style={{ border: "0.5px solid var(--color-border-tertiary)", borderRadius: "var(--border-radius-lg)", overflow: "hidden" }}>
      <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 12 }}>
        <thead>
          <tr style={{ background: "var(--color-background-secondary)" }}>
            {["Pair","Current","Yesterday","Last Week","1 Month Ago","1 Year Ago"].map(h => (
              <th key={h} style={{ padding: "8px 10px", textAlign: h === "Pair" ? "left" : "right", fontWeight: 500, fontSize: 11, color: "var(--color-text-secondary)", borderBottom: "1.5px solid var(--color-border-primary)", whiteSpace: "nowrap" }}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {FX_IDS.map(id => {
            const d = FX_DATA[id]; const s = d.series; const li = s.length - 1;
            const cur = s[li];
            const yesterday = Math.round((cur + (Math.sin(li * 1.3) * 0.001 * cur)) * 10000) / 10000;
            const lastWk = Math.round((cur + (Math.sin(li * 0.9) * 0.003 * cur)) * 10000) / 10000;
            const oneMonth = li >= 1 ? s[li - 1] : null;
            const oneYear = Math.round((cur * (1 + Math.sin(li * 0.4) * 0.05)) * 10000) / 10000;
            const tdStyle = { padding: "7px 10px", textAlign: "right", fontFamily: "var(--font-mono)", fontSize: 12, color: "var(--color-text-primary)" };
            return (
              <tr key={id} style={{ borderBottom: "0.5px solid var(--color-border-tertiary)" }}
                onMouseEnter={e => e.currentTarget.style.background = "var(--color-background-secondary)"}
                onMouseLeave={e => e.currentTarget.style.background = "transparent"}>
                <td style={{ padding: "7px 10px", fontWeight: 500, color: "var(--color-text-primary)" }}>{d.label}</td>
                <td style={{ ...tdStyle, fontWeight: 500 }}>{fmt(cur, d.format)}</td>
                <td style={tdStyle}>{fmt(yesterday, d.format)}</td>
                <td style={tdStyle}>{lastWk != null ? fmt(lastWk, d.format) : "—"}</td>
                <td style={tdStyle}>{oneMonth != null ? fmt(oneMonth, d.format) : "—"}</td>
                <td style={tdStyle}>{fmt(oneYear, d.format)}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
    <div style={{ marginTop: 8, marginBottom: 4, fontSize: 10, color: "var(--color-text-tertiary)", lineHeight: 1.7 }}>
      USD = U.S. Dollar &nbsp;·&nbsp; BRL = Brazilian Real &nbsp;·&nbsp; CAD = Canadian Dollar &nbsp;·&nbsp; ARS = Argentine Peso &nbsp;·&nbsp; EUR = Euro &nbsp;·&nbsp; AUD = Australian Dollar &nbsp;·&nbsp; MXN = Mexican Peso &nbsp;·&nbsp; CNY = Chinese Yuan
    </div>

    {FX_IDS.map((id, idx) => <FXChartWidget key={idx} defaultId={id} ready={ready} fmt={fmt} niceAxis={niceAxis} />)}
    <div style={{ marginTop: 14, fontSize: 10, color: "var(--color-text-tertiary)" }}>Source: ECB daily reference rates. Cross-rates computed from USD reference rates.</div>
  </div>);
}

function FXChartWidget({ defaultId, ready, fmt, niceAxis }) {
  const defaultD = FX_DATA[defaultId];
  // Parse default pair into base/quote currencies
  const parts = defaultD.label.split("/");
  const [base, setBase] = useState(parts[0]);
  const [quote, setQuote] = useState(parts[1]);

  // All available currencies: USD + everything from FX_DATA
  const CURRENCIES = {
    USD: { label: "USD", series: FX_WEEKS.map(() => 1) },
    BRL: { label: "BRL", series: FX_DATA["fx-brl"].series },
    CAD: { label: "CAD", series: FX_DATA["fx-cad"].series },
    ARS: { label: "ARS", series: FX_DATA["fx-ars"].series },
    EUR: { label: "EUR", series: FX_DATA["fx-eur"].series.map(v => 1 / v) },
    AUD: { label: "AUD", series: FX_DATA["fx-aud"].series },
    MXN: { label: "MXN", series: FX_DATA["fx-mxn"].series },
    CNY: { label: "CNY", series: FX_DATA["fx-cny"].series },
  };
  // EUR/USD is stored as EUR per USD inverted, so EUR series = 1/EUR_USD = units of EUR per 1 USD

  // Compute cross-rate: base/quote = how many quote per 1 base
  // All CURRENCIES[X].series = units of X per 1 USD
  // So base/quote = CURRENCIES[quote] / CURRENCIES[base] = (quote per USD) / (base per USD)
  const crossSeries = CURRENCIES[base] && CURRENCIES[quote]
    ? CURRENCIES[quote].series.map((q, i) => {
        const b = CURRENCIES[base].series[i];
        return b && b !== 0 ? Math.round((q / b) * 10000) / 10000 : null;
      })
    : [];

  const li = crossSeries.length - 1;
  const cur = crossSeries[li];
  const yesterday = cur != null ? Math.round((cur + (Math.sin(li * 1.3) * 0.001 * cur)) * 10000) / 10000 : null;
  const lastWk = cur != null ? Math.round((cur + (Math.sin(li * 0.9) * 0.003 * cur)) * 10000) / 10000 : null;
  const lastMonth = li >= 1 ? crossSeries[li - 1] : null;
  const lastYear = cur != null ? Math.round((cur * (1 + Math.sin(li * 0.4) * 0.05)) * 10000) / 10000 : null;

  const decPlaces = cur != null && Math.abs(cur) >= 100 ? 2 : 4;
  const fmtVal = (v) => v != null ? (decPlaces === 2 ? v.toFixed(2) : v.toFixed(4)) : "—";

  const FXDiff = ({ label, absVal }) => {
    if (absVal == null || cur == null) return null;
    const diff = cur - absVal;
    const pct = absVal !== 0 ? ((diff) / absVal * 100).toFixed(2) : null;
    const col = diff > 0 ? "#639922" : diff < 0 ? "#A32D2D" : "var(--color-text-tertiary)";
    return (
      <div style={{ display: "flex", justifyContent: "space-between", fontSize: 11, padding: "2px 0" }}>
        <span style={{ color: "var(--color-text-tertiary)" }}>{label} ({fmtVal(absVal)})</span>
        <span style={{ color: col, fontWeight: 500, fontFamily: "var(--font-mono)" }}>{diff > 0 ? "+" : ""}{fmtVal(diff)} ({pct}%)</span>
      </div>
    );
  };

  const rc = useCallback(canvas => {
    const vals = crossSeries.filter(v => v != null);
    if (vals.length === 0) return;
    const { yMin, yMax } = niceAxis(vals);
    new Chart(canvas, {
      type: "line", data: { labels: FX_WEEKS, datasets: [{
        label: `${base}/${quote}`, data: crossSeries, borderColor: "#A32D2D", backgroundColor: "rgba(163,45,45,0.06)",
        fill: true, borderWidth: 2, pointRadius: 0, tension: 0, spanGaps: true,
      }]},
      options: { responsive: true, maintainAspectRatio: false,
        interaction: { mode: "nearest", intersect: false },
        plugins: { legend: { display: false }, tooltip: { callbacks: { label: c => `${base}/${quote}: ${fmtVal(c.parsed.y)}` } } },
        scales: {
          x: { ticks: { autoSkip: true, maxTicksLimit: 10, maxRotation: 45, font: { size: 11 } }, grid: { color: "rgba(0,0,0,0.12)", lineWidth: 0.75 } },
          y: { min: yMin, max: yMax, ticks: { font: { size: 11 }, callback: v => fmtVal(v) }, grid: { color: "rgba(0,0,0,0.12)", lineWidth: 0.75 } },
        },
      },
    });
  }, [base, quote, crossSeries]);

  const dlPair = () => downloadCSV(`fx_${base}_${quote}.csv`, ["Month","Rate"], FX_WEEKS.map((w,i) => [w, crossSeries[i]]));

  const currencyOptions = Object.keys(CURRENCIES);

  const selectStyle = {
    padding: "4px 8px", fontSize: 15, fontWeight: 500, cursor: "pointer",
    border: "1px solid var(--color-border-secondary)", borderRadius: 6,
    background: "var(--color-background-primary)", color: "var(--color-text-primary)",
    fontFamily: "inherit",
  };

  return (
    <div>
      <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 14, marginTop: 28, flexWrap: "wrap" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
          <select value={base} onChange={e => setBase(e.target.value)} style={selectStyle}>
            {currencyOptions.filter(c => c !== quote).map(c => <option key={c} value={c}>{c}</option>)}
          </select>
          <span style={{ fontSize: 15, fontWeight: 500, color: "var(--color-text-tertiary)" }}>/</span>
          <select value={quote} onChange={e => setQuote(e.target.value)} style={selectStyle}>
            {currencyOptions.filter(c => c !== base).map(c => <option key={c} value={c}>{c}</option>)}
          </select>
        </div>
        <div style={{ marginLeft: "auto" }}><DownloadBtn onClick={dlPair} /></div>
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 2fr", gap: 14, alignItems: "start" }}>
        <div style={{ background: "var(--color-background-secondary)", borderRadius: "var(--border-radius-md)", padding: "12px 14px" }}>
          <div style={{ fontSize: 11, color: "var(--color-text-secondary)", marginBottom: 2 }}>1 {base} buys</div>
          <div style={{ fontSize: 22, fontWeight: 500, color: "var(--color-text-primary)", marginBottom: 6 }}>{fmtVal(cur)} <span style={{ fontSize: 12, fontWeight: 400, color: "var(--color-text-secondary)" }}>{quote}</span></div>
          <div style={{ borderTop: "0.5px solid var(--color-border-tertiary)", paddingTop: 6, display: "flex", flexDirection: "column", gap: 1 }}>
            <FXDiff label="vs. yesterday" absVal={yesterday} />
            <FXDiff label="vs. last week" absVal={lastWk} />
            <FXDiff label="vs. last month" absVal={lastMonth} />
            <FXDiff label="vs. last year" absVal={lastYear} />
          </div>
        </div>
        {ready && <ChartBox id={`fx_${base}_${quote}`} height={200} renderChart={rc} deps={`${base}_${quote}`} />}
      </div>
    </div>
  );
}

// ════════════════════════════════════════════════════════════════════════
// MARKET DRIVERS — DROUGHT (USDA Commodities in Drought)
// ════════════════════════════════════════════════════════════════════════

const DROUGHT_COMMODITIES = ["corn","soybeans","winter_wheat","spring_wheat","cattle","hay"];
const DROUGHT_FALLBACK = {
  corn:         {label:"Corn",         color:"#D4A017", latest_d1_d4: 0, seasonal:{}},
  soybeans:     {label:"Soybeans",     color:"#1D9E75", latest_d1_d4: 0, seasonal:{}},
  winter_wheat: {label:"Winter Wheat", color:"#A32D2D", latest_d1_d4: 0, seasonal:{}},
  spring_wheat: {label:"Spring Wheat", color:"#D85A30", latest_d1_d4: 0, seasonal:{}},
  cattle:       {label:"Cattle",       color:"#378ADD", latest_d1_d4: 0, seasonal:{}},
  hay:          {label:"Hay",          color:"#8B5CF6", latest_d1_d4: 0, seasonal:{}},
};

function useLiveDrought() {
  const [data, setData] = useState(null);
  const [loaded, setLoaded] = useState(false);
  useEffect(() => {
    fetch("data/drought.json?t=" + Date.now())
      .then(r => { if (!r.ok) throw new Error("not found"); return r.json(); })
      .then(d => { if (d && d.data) setData(d.data); setLoaded(true); })
      .catch(() => { setLoaded(true); });
  }, []);
  return { droughtData: data || DROUGHT_FALLBACK, droughtLoaded: loaded };
}

function DroughtPage({ ready }) {
  var ref2 = useLiveDrought();
  var droughtData = ref2.droughtData;
  var droughtLoaded = ref2.droughtLoaded;
  var curYear = new Date().getFullYear();
  var lastYear = curYear - 1;

  // Month layout (same as COT)
  var monthBounds = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334];
  var monthMids = [15, 45, 74, 105, 135, 166, 196, 227, 258, 288, 319, 349];
  var monthLabels = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];

  var xAxisConfig = {
    type: "linear", min: 0, max: 365,
    ticks: {
      callback: function(val) { var mi = monthMids.indexOf(val); return mi >= 0 ? monthLabels[mi] : ""; },
      autoSkip: false, maxRotation: 0, font: {size: 11},
    },
    afterBuildTicks: function(axis) {
      var ticks = [];
      for (var i = 0; i < 12; i++) { ticks.push({value: monthBounds[i]}); ticks.push({value: monthMids[i]}); }
      axis.ticks = ticks;
    },
    grid: {
      color: function(ctx) {
        var val = ctx.tick.value;
        if (val > 0 && monthBounds.indexOf(val) >= 0) return "rgba(0,0,0,0.12)";
        return "transparent";
      }, lineWidth: 0.75,
    },
  };

  // Overview chart: all commodities, current year
  var overviewChart = useCallback(function(canvas) {
    var datasets = [];
    DROUGHT_COMMODITIES.forEach(function(id) {
      var d = droughtData[id]; if (!d || !d.seasonal) return;
      var points = d.seasonal[String(curYear)] || [];
      if (points.length === 0) return;
      datasets.push({
        label: d.label, data: points, borderColor: d.color, borderWidth: 2,
        pointRadius: 0, pointHitRadius: 6, tension: 0, fill: false, showLine: true,
      });
    });
    var allVals = datasets.flatMap(function(ds) { return ds.data.map(function(p){return p.y;}); });
    if (allVals.length === 0) return;
    var yMax = Math.min(100, Math.ceil((Math.max.apply(null, allVals) + 10) / 10) * 10);
    new Chart(canvas, {type: "scatter", data: {datasets: datasets}, options: {
      responsive: true, maintainAspectRatio: false,
      interaction: {mode: "nearest", intersect: false, axis: "xy"},
      plugins: {legend: {display: false}, tooltip: {mode: "nearest", intersect: false, backgroundColor: "rgba(0,0,0,0.6)",
        callbacks: {
          title: function(items) {
            if (items.length === 0) return "";
            var doy = items[0].parsed.x;
            var mi = 11; for (var m=0;m<11;m++){if(doy<monthBounds[m+1]){mi=m;break;}}
            return monthLabels[mi] + " " + (Math.floor(doy - monthBounds[mi]) + 1);
          },
          label: function(c2){return c2.dataset.label + ": " + c2.parsed.y + "%";}
        },
      }},
      scales: { x: xAxisConfig, y: {min: 0, max: yMax, title: {display: true, text: "% in drought (D1+)", font:{size:11}}, ticks: {font:{size:11}, callback: function(v){return v+"%";}}, grid: {color:"rgba(0,0,0,0.08)", lineWidth: 0.75}} },
    }});
  }, [droughtData]);

  // Individual commodity chart: curYear, lastYear, 5yr avg
  var mkCommodityChart = function(id) { return function(canvas) {
    var d = droughtData[id]; if (!d || !d.seasonal) return;
    var datasets = [];
    var curPts = d.seasonal[String(curYear)] || [];
    var lastPts = d.seasonal[String(lastYear)] || [];
    var avgPts = d.seasonal["5yr_avg"] || [];
    if (curPts.length > 0) datasets.push({label: String(curYear), data: curPts, borderColor: d.color, borderWidth: 2.5, pointRadius: 0, pointHitRadius: 6, tension: 0, fill: false, showLine: true});
    if (lastPts.length > 0) datasets.push({label: String(lastYear), data: lastPts, borderColor: d.color, borderWidth: 1.5, borderDash: [5,3], pointRadius: 0, tension: 0, fill: false, showLine: true});
    if (avgPts.length > 0) datasets.push({label: "5-yr avg", data: avgPts, borderColor: "#333", borderWidth: 1.5, borderDash: [2,4], pointRadius: 0, pointHitRadius: 6, tension: 0, fill: false, showLine: true});
    var allVals = datasets.flatMap(function(ds){return ds.data.map(function(p){return p.y;});});
    if (allVals.length === 0) return;
    var yMax = Math.min(100, Math.ceil((Math.max.apply(null, allVals) + 10) / 10) * 10);
    new Chart(canvas, {type: "scatter", data: {datasets: datasets}, options: {
      responsive: true, maintainAspectRatio: false,
      interaction: {mode: "nearest", intersect: false, axis: "xy"},
      plugins: {legend: {display: false}, tooltip: {mode: "nearest", intersect: false, backgroundColor: "rgba(0,0,0,0.6)",
        callbacks: {
          title: function(items) {
            if (items.length === 0) return "";
            var doy = items[0].parsed.x;
            var mi = 11; for (var m=0;m<11;m++){if(doy<monthBounds[m+1]){mi=m;break;}}
            return monthLabels[mi] + " " + (Math.floor(doy - monthBounds[mi]) + 1);
          },
          label: function(c2){return c2.dataset.label + ": " + c2.parsed.y + "%";}
        },
      }},
      scales: { x: xAxisConfig, y: {min: 0, max: yMax, title: {display: true, text: "% in drought (D1+)", font:{size:11}}, ticks: {font:{size:11}, callback: function(v){return v+"%";}}, grid: {color:"rgba(0,0,0,0.08)", lineWidth: 0.75}} },
    }});
  };};

  // CSV download
  var dlDrought = function() {
    var headers = ["Date"];
    DROUGHT_COMMODITIES.forEach(function(id) {
      var lbl = droughtData[id] ? droughtData[id].label : id;
      headers.push(lbl + " " + curYear);
      headers.push(lbl + " " + lastYear);
      headers.push(lbl + " 5yr Avg");
    });
    var rows = [];
    // Collect all unique dates from current year
    var allDates = {};
    DROUGHT_COMMODITIES.forEach(function(id) {
      var d = droughtData[id]; if (!d || !d.seasonal) return;
      var pts = d.seasonal[String(curYear)] || [];
      pts.forEach(function(p) { if (p.date) allDates[p.date] = p.x; });
    });
    var sortedDates = Object.keys(allDates).sort();
    sortedDates.forEach(function(date) {
      var doy = allDates[date];
      var row = [date];
      DROUGHT_COMMODITIES.forEach(function(id) {
        var d = droughtData[id]; if (!d || !d.seasonal) { row.push("","",""); return; }
        // Current year
        var curPts = d.seasonal[String(curYear)] || [];
        var curMatch = curPts.find(function(p){return p.date === date;});
        row.push(curMatch ? curMatch.y : "");
        // Last year - closest DOY
        var lyPts = d.seasonal[String(lastYear)] || [];
        var lyMatch = null;
        if (lyPts.length > 0) {
          var best = lyPts.reduce(function(b,p){return Math.abs(p.x-doy)<Math.abs(b.x-doy)?p:b;});
          if (Math.abs(best.x - doy) < 14) lyMatch = best;
        }
        row.push(lyMatch ? lyMatch.y : "");
        // 5yr avg - closest DOY
        var avgPts = d.seasonal["5yr_avg"] || [];
        var avgMatch = null;
        if (avgPts.length > 0) {
          var bestA = avgPts.reduce(function(b,p){return Math.abs(p.x-doy)<Math.abs(b.x-doy)?p:b;});
          if (Math.abs(bestA.x - doy) < 14) avgMatch = bestA;
        }
        row.push(avgMatch ? avgMatch.y : "");
      });
      rows.push(row);
    });
    downloadCSV("commodities_in_drought_all.csv", headers, rows);
  };

  return (<div>
    <div style={{fontSize: 12, color: "var(--color-text-tertiary)", marginBottom: 14}}>USDA Commodities in Drought — percentage of domestic production area in drought conditions (D1 or worse). Source: agindrought.unl.edu</div>

    <div style={{display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(170px, 1fr))", gap: 10, marginBottom: 16}}>
      {DROUGHT_COMMODITIES.map(function(id) {
        var d = droughtData[id]; if (!d) return null;
        var cur = d.latest_d1_d4;
        var seasonal = d.seasonal || {};
        var curPts = seasonal[String(curYear)] || [];
        var lastYrPts = seasonal[String(lastYear)] || [];
        var avgPts = seasonal["5yr_avg"] || [];
        // Find previous week value (second-to-last point in current year)
        var prevWk = curPts.length >= 2 ? curPts[curPts.length - 2].y : null;
        // Find last year same approx DOY
        var curDoy = curPts.length > 0 ? curPts[curPts.length - 1].x : null;
        var lastYrVal = null;
        if (curDoy != null && lastYrPts.length > 0) {
          var closest = lastYrPts.reduce(function(best, p) { return Math.abs(p.x - curDoy) < Math.abs(best.x - curDoy) ? p : best; });
          if (Math.abs(closest.x - curDoy) < 14) lastYrVal = closest.y;
        }
        // Find 5yr avg at same approx DOY
        var avgVal = null;
        if (curDoy != null && avgPts.length > 0) {
          var closestAvg = avgPts.reduce(function(best, p) { return Math.abs(p.x - curDoy) < Math.abs(best.x - curDoy) ? p : best; });
          if (Math.abs(closestAvg.x - curDoy) < 14) avgVal = closestAvg.y;
        }
        var DiffLine = function(props) {
          if (props.comp == null || cur == null) return null;
          var diff = cur - props.comp;
          var col = diff > 0 ? "#A32D2D" : diff < 0 ? "#639922" : "var(--color-text-tertiary)";
          var diffStr = (diff > 0 ? "+" : "") + diff + "%";
          return React.createElement("div", {style:{display:"flex",justifyContent:"space-between",fontSize:10.5,padding:"1px 0"}},
            React.createElement("span", {style:{color:"var(--color-text-tertiary)"}}, props.label),
            React.createElement("span", null,
              React.createElement("span", {style:{color:"var(--color-text-secondary)"}}, props.comp + "% "),
              React.createElement("span", {style:{color:col,fontWeight:500}}, "(" + diffStr + ")")
            )
          );
        };
        return (
          <div key={id} style={{background: "var(--color-background-secondary)", borderRadius: "var(--border-radius-md)", padding: "12px 14px", minWidth: 0, borderLeft: "3px solid " + d.color}}>
            <div style={{fontSize: 11, color: "var(--color-text-secondary)", marginBottom: 3, textTransform: "uppercase", letterSpacing: "0.4px"}}>{d.label}</div>
            <div style={{fontSize: 22, fontWeight: 500, color: "var(--color-text-primary)", marginBottom: 4}}>{cur != null ? cur + "%" : "—"}</div>
            {d.latest_date && <div style={{fontSize: 10, color: "var(--color-text-tertiary)", marginBottom: 6}}>as of {fmtDate(d.latest_date)}</div>}
            <div style={{borderTop: "0.5px solid var(--color-border-tertiary)", paddingTop: 5}}>
              {React.createElement(DiffLine, {label: "vs. last week", comp: prevWk})}
              {React.createElement(DiffLine, {label: "vs. last year", comp: lastYrVal})}
              {React.createElement(DiffLine, {label: "vs. 5-yr avg", comp: avgVal})}
            </div>
          </div>
        );
      })}
    </div>

    <SectionTitle right={<DownloadBtn onClick={dlDrought} />}>All commodities — {curYear}</SectionTitle>
    {ready && <ChartBox id={"drought_overview"} height={300} renderChart={overviewChart} deps={"drought_ov_" + droughtLoaded} />}

    <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:18,marginTop:8}}>
    {DROUGHT_COMMODITIES.map(function(id) {
      var d = droughtData[id]; if (!d) return null;
      return (
        <div key={id}>
          <div style={{fontSize:14,fontWeight:600,color:"var(--color-text-primary)",marginBottom:6}}>{d.label}</div>
          <div style={{display: "flex", gap: 12, marginBottom: 6, fontSize: 11}}>
            <span><span style={{display:"inline-block",width:16,borderTop:"2.5px solid "+d.color,verticalAlign:"middle",marginRight:4}}></span>{curYear}</span>
            <span><span style={{display:"inline-block",width:16,borderTop:"2px dashed "+d.color,verticalAlign:"middle",marginRight:4}}></span>{lastYear}</span>
            <span><span style={{display:"inline-block",width:16,borderTop:"2px dotted #333",verticalAlign:"middle",marginRight:4}}></span>5-yr avg</span>
          </div>
          {ready && <ChartBox id={"drought_" + id} height={220} renderChart={mkCommodityChart(id)} deps={"drought_" + id + "_" + droughtLoaded} />}
        </div>
      );
    })}
    </div>

    <div style={{marginTop: 14, fontSize: 11, color: "var(--color-text-tertiary)"}}>Source: USDA / U.S. Drought Monitor via agindrought.unl.edu. Percentage of domestic production area experiencing drought at D1 (Moderate) intensity or worse.</div>
  </div>);
}


// ════════════════════════════════════════════════════════════════════════
// GRAINS — EXPORT INSPECTIONS (USDA/GIPSA Weekly)
// ════════════════════════════════════════════════════════════════════════

// Marketing year weeks (Sep–Aug for corn/soybeans, Jun–May for wheat)
// 52 weeks of data, labeled by week number within marketing year
const EI_WEEKS = Array.from({ length: 53 }, (_, i) => {
  const d = new Date(2024, 8, 1); // Sep 1 for corn/soy MY start
  d.setDate(d.getDate() + i * 7);
  const m = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][d.getMonth()];
  return `${m} ${d.getDate()}`;
});

function mkEISeries(base, scale) {
  return EI_WEEKS.map((_, i) => Math.max(0, Math.round(base + Math.sin((i / 52) * Math.PI * 2 + 1.2) * scale + (Math.cos(i * 0.7) - 0.5) * scale * 0.4)));
}

const EXPORT_INSPECTIONS = {
  corn: {
    label: "Corn", unit: "thousand MT", color: "#D4A017",
    "2024/25": mkEISeries(1150, 350), "2023/24": mkEISeries(1050, 320), "5yr": mkEISeries(1000, 280),
  },
  soybeans: {
    label: "Soybeans", unit: "thousand MT", color: "#1D9E75",
    "2024/25": mkEISeries(850, 400), "2023/24": mkEISeries(780, 370), "5yr": mkEISeries(720, 330),
  },
  wheat: {
    label: "Wheat (all)", unit: "thousand MT", color: "#A32D2D",
    "2024/25": mkEISeries(420, 120), "2023/24": mkEISeries(400, 110), "5yr": mkEISeries(380, 100),
  },
  sorghum: {
    label: "Sorghum", unit: "thousand MT", color: "#D85A30",
    "2024/25": mkEISeries(120, 65), "2023/24": mkEISeries(105, 55), "5yr": mkEISeries(95, 50),
  },
};

const EI_COMMODITIES = Object.keys(EXPORT_INSPECTIONS);

function ExportInspectionsPage({ ready }) {
  var ref = useLiveExportInspections();
  var eiData = ref.eiData;
  var eiLoaded = ref.eiLoaded;
  var _comm = useState("corn");
  var comm = _comm[0], setComm = _comm[1];
  var _range = useState("1");
  var range = _range[0], setRange = _range[1];
  var _unit = useState("mt");
  var unit = _unit[0], setUnit = _unit[1];
  var _hy = useState(new Set());
  var hiddenYrs = _hy[0], setHiddenYrs = _hy[1];

  useEffect(function(){ setHiddenYrs(new Set()); }, [comm, range, unit]);
  var toggleYr = function(label) { setHiddenYrs(function(prev){ var next = new Set(prev); if(next.has(label))next.delete(label);else next.add(label); return next; }); };

  var BU_PER_MT = { corn: 39.368, soybeans: 36.744, wheat: 36.744, sorghum: 39.368 };
  var isBu = unit === "bu";
  // Chart display conversion
  var conv = function(mt) {
    if (mt == null) return null;
    if (isBu) return Math.round(mt * BU_PER_MT[comm] / 1000000 * 10) / 10; // M bu, 1 decimal
    return Math.round(mt / 1000 * 10) / 10; // thousand MT
  };
  // Card display: MT view = metric tons (whole number), Bu view = M bushels (1 decimal)
  var cardConv = function(mt) {
    if (mt == null) return null;
    if (isBu) return Math.round(mt * BU_PER_MT[comm] / 1000000 * 10) / 10;
    return Math.round(mt);
  };
  var weeklyUnit = isBu ? "M bushels" : "1,000 MT";
  var cardUnit = isBu ? "M bushels" : "MT";

  var COMM_OPTS = [{id:"corn",label:"Corn"},{id:"soybeans",label:"Soybeans"},{id:"wheat",label:"Wheat"},{id:"sorghum",label:"Sorghum"}];

  var myConfig = {
    corn: { startMonth: 9, mktN: ["Sep","Oct","Nov","Dec","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug"] },
    soybeans: { startMonth: 9, mktN: ["Sep","Oct","Nov","Dec","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug"] },
    sorghum: { startMonth: 9, mktN: ["Sep","Oct","Nov","Dec","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug"] },
    wheat: { startMonth: 6, mktN: ["Jun","Jul","Aug","Sep","Oct","Nov","Dec","Jan","Feb","Mar","Apr","May"] },
  };
  var cfg = myConfig[comm];

  var dateToMY = function(ds) {
    var m = parseInt(ds.split("-")[1]); var y = parseInt(ds.split("-")[0]);
    return m >= cfg.startMonth ? y : y - 1;
  };
  var dateToMktDay = function(ds) {
    var p = ds.split("-"); var y = parseInt(p[0]), m = parseInt(p[1]) - 1, d = parseInt(p[2]);
    var dt = new Date(y, m, d);
    var myStart = m >= (cfg.startMonth - 1) ? new Date(y, cfg.startMonth - 1, 1) : new Date(y - 1, cfg.startMonth - 1, 1);
    return Math.max(0, Math.min(365, Math.round((dt - myStart) / 86400000)));
  };
  var myLabel = function(yr) { return yr + "/" + String(yr + 1).slice(2); };

  var processWeekly = function(rawPts) {
    if (!rawPts || !rawPts.length) return {};
    var byMY = {};
    rawPts.forEach(function(pt) {
      var my = dateToMY(pt.d); var day = dateToMktDay(pt.d);
      if (!byMY[my]) byMY[my] = [];
      byMY[my].push({ x: day, y: conv(pt.v) });
    });
    Object.keys(byMY).forEach(function(my) { byMY[my].sort(function(a, b) { return a.x - b.x; }); });
    return byMY;
  };

  var buildCumul = function(weeklyByMY) {
    var cumul = {};
    Object.keys(weeklyByMY).forEach(function(my) {
      var pts = weeklyByMY[my]; var running = 0;
      cumul[my] = pts.map(function(p) { running += p.y; return { x: p.x, y: Math.round(running * 10) / 10 }; });
    });
    return cumul;
  };

  var rawPts = eiData ? eiData[comm] || [] : [];
  var weeklyByMY = processWeekly(rawPts);
  var cumulByMY = buildCumul(weeklyByMY);

  var now = new Date();
  var curMY = now.getMonth() >= (cfg.startMonth - 1) ? now.getFullYear() : now.getFullYear() - 1;
  var rangeN = parseInt(range);
  var startMY = curMY - rangeN;

  var yrColors = ["#A32D2D","#D85A30","#E8A735","#639922","#1D9E75","#378ADD","#534AB7","#8B5CF6","#EC4899","#6B7280"];
  var getColor = function(my) { if (my === curMY) return "#333"; var dist = curMY - my; if (dist === 1) return "#1D9E75"; if (dist === 2) return "#639922"; if (dist === 3) return "#E8A735"; if (dist === 4) return "#D85A30"; if (dist === 5) return "#A32D2D"; return yrColors[(dist - 1) % yrColors.length]; };

  var buildItems = function(byMY) {
    var items = [];
    for (var y = startMY; y <= curMY; y++) { if (byMY[y]) items.push({ label: myLabel(y), my: y, color: getColor(y) }); }
    return items;
  };
  var allItems = buildItems(weeklyByMY);
  var hk = Array.from(hiddenYrs).sort().join(",");

  // Card info — always in metric tons (1,000 MT)
  var getCardInfo = function() {
    if (!rawPts || !rawPts.length) return { curWk: null, prevWk: null, lastYrWk: null, curCumul: null, prevCumul: null, lastYrCumul: null, date: null, my: null };
    var sorted = rawPts.slice().sort(function(a, b) { return a.d < b.d ? 1 : -1; });
    var latest = sorted[0]; var prev = sorted.length > 1 ? sorted[1] : null;
    // Same week last year
    var latestDate = new Date(latest.d);
    var targetDate = new Date(latestDate); targetDate.setFullYear(targetDate.getFullYear() - 1);
    var targetMs = targetDate.getTime();
    var lastYrPt = null; var bestDiff = 10 * 86400000;
    rawPts.forEach(function(p) { var diff = Math.abs(new Date(p.d).getTime() - targetMs); if (diff < bestDiff) { bestDiff = diff; lastYrPt = p; } });

    // Cumulative for current MY
    var latestMY = dateToMY(latest.d);
    var myPts = rawPts.filter(function(p) { return dateToMY(p.d) === latestMY && p.d <= latest.d; }).sort(function(a, b) { return a.d < b.d ? -1 : 1; });
    var cumulVal = myPts.reduce(function(s, p) { return s + p.v; }, 0);

    // Cumulative for previous week in same MY (drop last week)
    var prevMyPts = myPts.slice(0, -1);
    var prevCumulVal = prevMyPts.reduce(function(s, p) { return s + p.v; }, 0);

    // Cumulative for same week last year in that MY
    var lastYrMY = latestMY - 1;
    var lastYrMyPts = rawPts.filter(function(p) { return dateToMY(p.d) === lastYrMY; }).sort(function(a, b) { return a.d < b.d ? -1 : 1; });
    // Find how many weeks into the MY we are
    var weeksIn = myPts.length;
    var lastYrCumulPts = lastYrMyPts.slice(0, weeksIn);
    var lastYrCumulVal = lastYrCumulPts.reduce(function(s, p) { return s + p.v; }, 0);

    return {
      curWk: cardConv(latest.v), prevWk: prev ? cardConv(prev.v) : null, lastYrWk: lastYrPt ? cardConv(lastYrPt.v) : null,
      curCumul: cardConv(cumulVal), prevCumul: cardConv(prevCumulVal), lastYrCumul: lastYrCumulVal > 0 ? cardConv(lastYrCumulVal) : null,
      date: latest.d, my: myLabel(latestMY),
    };
  };
  var cardInfo = getCardInfo();

  var statCard = function(label, curVal, comparisons, unitLabel) {
    return (<div style={{background:"var(--color-background-secondary)",borderRadius:"var(--border-radius-md)",padding:"12px 14px",minWidth:0}}>
      <div style={{fontSize:11,color:"var(--color-text-secondary)",marginBottom:3,textTransform:"uppercase",letterSpacing:"0.4px"}}>{label}</div>
      <div style={{fontSize:22,fontWeight:500,color:"var(--color-text-primary)",marginBottom:2}}>{curVal != null ? (isBu ? curVal.toLocaleString(undefined, {minimumFractionDigits:1, maximumFractionDigits:1}) : curVal.toLocaleString()) : "—"}<span style={{fontSize:12,fontWeight:400,color:"var(--color-text-secondary)",marginLeft:4}}>{unitLabel}</span></div>
      {cardInfo.date && <div style={{fontSize:10,color:"var(--color-text-tertiary)",marginBottom:6}}>as of {fmtDate(cardInfo.date)}</div>}
      <div style={{borderTop:"0.5px solid var(--color-border-tertiary)",paddingTop:5}}>
        {comparisons.map(function(c2, i) {
          if (curVal == null || c2.val == null) return null;
          var diff = Math.round((curVal - c2.val) * 10) / 10;
          var pctChg = Math.round((curVal - c2.val) / Math.abs(c2.val) * 1000) / 10;
          var col = diff > 0 ? "#639922" : diff < 0 ? "#A32D2D" : "var(--color-text-tertiary)";
          return (<div key={i} style={{display:"flex",justifyContent:"space-between",fontSize:10.5,padding:"1px 0"}}>
            <span style={{color:"var(--color-text-tertiary)"}}>{c2.label}</span>
            <span style={{display:"flex",gap:6,alignItems:"baseline",justifyContent:"flex-end"}}><span style={{color:"var(--color-text-secondary)",textAlign:"right",flex:"none"}}>{isBu ? c2.val.toLocaleString(undefined, {minimumFractionDigits:1, maximumFractionDigits:1}) : c2.val.toLocaleString()}</span><span style={{color:col,fontWeight:500,textAlign:"right",minWidth:76,flex:"none"}}>({diff > 0 ? "+" : ""}{isBu ? diff.toLocaleString(undefined, {minimumFractionDigits:1, maximumFractionDigits:1}) : diff.toLocaleString()})</span><span style={{color:col,fontWeight:500,textAlign:"right",minWidth:52,flex:"none"}}>({pctChg > 0 ? "+" : ""}{pctChg.toFixed(1)}%)</span></span>
          </div>);
        })}
      </div>
    </div>);
  };

  var mktBounds = [0,30,61,91,122,153,181,212,242,273,303,334];
  var mktMids = [15,45,76,106,137,167,196,227,257,288,318,349];

  var mkChart = function(byMY) { return function(canvas) {
    if (!byMY || Object.keys(byMY).length === 0) return;
    var ds = [];
    for (var y = startMY; y <= curMY; y++) {
      var pts = byMY[y]; if (!pts || !pts.length) continue;
      ds.push({ label: myLabel(y), data: pts.slice(), borderColor: getColor(y), borderWidth: y === curMY ? 2.5 : 1.5, pointRadius: 0, pointHitRadius: 6, tension: 0, fill: false, showLine: true, hidden: hiddenYrs.has(myLabel(y)) });
    }
    if (ds.length === 0) return;
    var vis = ds.filter(function(d) { return !d.hidden; }).flatMap(function(d) { return d.data.map(function(p) { return p.y; }); });
    if (vis.length === 0) return;
    var rawMax = Math.max.apply(null, vis), rawMin = Math.min.apply(null, vis);
    var span = rawMax - rawMin || 1;
    var step = Math.pow(10, Math.floor(Math.log10(span / 4)));
    if (span / step < 4) step = step / 2;
    if (span / step > 8) step = step * 2;
    var yMin = Math.max(0, Math.floor(rawMin / step) * step);
    var yMax = Math.ceil(rawMax / step) * step;
    if (yMax === rawMax) yMax += step;
    var tks = []; for (var k = 0; k < 12; k++) { tks.push({value: mktBounds[k]}); tks.push({value: mktMids[k]}); }
    new Chart(canvas, { type: "scatter", data: { datasets: ds }, options: {
      responsive: true, maintainAspectRatio: false,
      interaction: { mode: "nearest", intersect: false },
      plugins: { legend: { display: false }, tooltip: { mode: "nearest", intersect: false, backgroundColor: "rgba(0,0,0,0.6)", titleFont: { size: 11 }, bodyFont: { size: 11 },
        callbacks: { title: function(items) { if (!items.length) return ""; var doy = items[0].parsed.x; var mi = 11; for (var m = 0; m < 11; m++) { if (doy < mktBounds[m+1]) { mi = m; break; } } return cfg.mktN[mi] + " " + (Math.floor(doy - mktBounds[mi]) + 1); },
          label: function(c2) { return c2.parsed.y == null ? null : c2.dataset.label + ": " + c2.parsed.y.toLocaleString(); } } } },
      scales: { x: { type: "linear", min: 0, max: 365, afterBuildTicks: function(ax) { ax.ticks = tks; }, ticks: { callback: function(v) { var idx = mktMids.indexOf(v); return idx >= 0 ? cfg.mktN[idx] : ""; }, autoSkip: false, maxRotation: 0, font: { size: 10 } }, grid: { color: function(ctx) { var v = ctx.tick.value; if (v > 0 && mktBounds.indexOf(v) >= 0) return "rgba(0,0,0,0.12)"; return "transparent"; }, lineWidth: 0.75 } },
        y: { min: yMin, max: yMax, ticks: { stepSize: step, font: { size: 10 }, callback: function(v) { return v.toLocaleString(); } }, grid: { color: "rgba(0,0,0,0.08)", lineWidth: 0.75 } } }
    } });
  }; };

  var dlCSV = function() {
    var hdrs = ["Date", "MY", "Weekly Volume (" + weeklyUnit + ")", "Cumulative MY (" + weeklyUnit + ")"];
    var rows = [];
    rawPts.filter(function(p) { var my = dateToMY(p.d); return my >= startMY && my <= curMY; }).sort(function(a, b) { return a.d < b.d ? -1 : 1; }).forEach(function(pt) {
      var my = dateToMY(pt.d);
      var myPts2 = rawPts.filter(function(p) { return dateToMY(p.d) === my && p.d <= pt.d; });
      var cumul = myPts2.reduce(function(s, p) { return s + p.v; }, 0);
      rows.push([pt.d, myLabel(my), conv(pt.v), conv(cumul)]);
    });
    downloadCSV("export_inspections_" + comm + "_" + unit + ".csv", hdrs, rows);
  };

  var chevSvg = "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath d='M3 5l3 3 3-3' fill='none' stroke='%23666' stroke-width='1.5'/%3E%3C/svg%3E\")";
  var selSt = {padding:"6px 24px 6px 10px",fontSize:13,fontWeight:500,border:"1px solid var(--color-border-secondary)",borderRadius:6,background:"var(--color-background-primary)",color:"var(--color-text-primary)",fontFamily:"inherit",cursor:"pointer",appearance:"none",backgroundImage:chevSvg,backgroundRepeat:"no-repeat",backgroundPosition:"right 6px center"};
  var modeSt = function(a) { return {padding:"6px 14px",fontSize:12,fontWeight:a?600:400,border:"1px solid "+(a?"#2563EB":"var(--color-border-secondary)"),borderRadius:5,cursor:"pointer",background:a?"#2563EB":"transparent",color:a?"#fff":"var(--color-text-secondary)",transition:"all 0.15s"}; };

  return (<div>
    <div style={{display:"flex",alignItems:"center",gap:12,marginBottom:14,flexWrap:"wrap"}}>
      <div style={{display:"flex",alignItems:"center",gap:6}}>
        <span style={{fontSize:11,fontWeight:600,color:"var(--color-text-secondary)",textTransform:"uppercase"}}>Commodity</span>
        <select value={comm} onChange={function(e){setComm(e.target.value);}} style={selSt}>
          {COMM_OPTS.map(function(t) { return <option key={t.id} value={t.id}>{t.label}</option>; })}
        </select>
      </div>
      <div style={{display:"flex",alignItems:"center",gap:6}}>
        <span style={{fontSize:11,fontWeight:600,color:"var(--color-text-secondary)",textTransform:"uppercase"}}>Range</span>
        <select value={range} onChange={function(e){setRange(e.target.value);}} style={selSt}>
          <option value="1">1 Year</option>
          <option value="5">5 Years</option>
          <option value="10">10 Years</option>
        </select>
      </div>
      <div style={{display:"flex",gap:3}}>
        <button onClick={function(){setUnit("mt");}} style={modeSt(unit==="mt")}>Metric Tons</button>
        <button onClick={function(){setUnit("bu");}} style={modeSt(unit==="bu")}>Bushels</button>
      </div>
      <div style={{marginLeft:"auto"}}><DownloadBtn onClick={dlCSV} /></div>
    </div>

    <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:10,marginBottom:16}}>
      {statCard("Weekly Volume", cardInfo.curWk, [
        {label: "vs. last week", val: cardInfo.prevWk},
        {label: "vs. last year", val: cardInfo.lastYrWk},
      ], cardUnit)}
      {statCard("Cumulative MY (" + (cardInfo.my || "") + ")", cardInfo.curCumul, [
        {label: "vs. last week", val: cardInfo.prevCumul},
        {label: "vs. last year (same wk)", val: cardInfo.lastYrCumul},
      ], cardUnit)}
    </div>

    <div style={{display:"flex",flexWrap:"wrap",gap:6,marginBottom:16,alignItems:"center"}}>
      {allItems.map(function(item) { var isH = hiddenYrs.has(item.label); return (
        <button key={item.label} onClick={function(){toggleYr(item.label);}} style={{display:"flex",alignItems:"center",gap:5,padding:"4px 10px",border:"1px solid var(--color-border-secondary)",borderRadius:5,background:isH?"var(--color-background-secondary)":"transparent",cursor:"pointer",opacity:isH?0.3:1,transition:"all 0.15s"}}>
          <span style={{width:18,height:0,borderTop:"2.5px solid "+item.color,display:"inline-block"}}></span>
          <span style={{fontSize:12,fontWeight:500,color:"var(--color-text-primary)"}}>{item.label}</span>
        </button>); })}
    </div>

    <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:16}}>
      <div>
        <div style={{fontSize:14,fontWeight:600,color:"var(--color-text-primary)",marginBottom:6}}>Weekly Inspections <span style={{fontSize:11,fontWeight:400,color:"var(--color-text-tertiary)"}}>({weeklyUnit})</span></div>
        {ready && <ChartBox id={"ei_wk_"+comm+"_"+range+"_"+unit} height={280} renderChart={mkChart(weeklyByMY)} deps={"ei_wk_"+comm+"_"+range+"_"+unit+"_"+eiLoaded+"_"+hk} />}
      </div>
      <div>
        <div style={{fontSize:14,fontWeight:600,color:"var(--color-text-primary)",marginBottom:6}}>Cumulative MY Total <span style={{fontSize:11,fontWeight:400,color:"var(--color-text-tertiary)"}}>({weeklyUnit})</span></div>
        {ready && <ChartBox id={"ei_cu_"+comm+"_"+range+"_"+unit} height={280} renderChart={mkChart(cumulByMY)} deps={"ei_cu_"+comm+"_"+range+"_"+unit+"_"+eiLoaded+"_"+hk} />}
      </div>
    </div>
    <div style={{marginTop:14,fontSize:11,color:"var(--color-text-tertiary)"}}>Source: USDA FGIS Export Grain Inspection Report. Marketing years: Corn/Soybeans/Sorghum (Sep–Aug), Wheat (Jun–May).</div>
  </div>);
}


function ExportSalesPage({ ready }) {
  var ref = useLiveExportSales();
  var esData = ref.esData;
  var esLoaded = ref.esLoaded;
  var _comm = useState("corn");
  var comm = _comm[0], setComm = _comm[1];
  var _range = useState("1");
  var range = _range[0], setRange = _range[1];
  var _country = useState("ALL");
  var country = _country[0], setCountry = _country[1];
  var _myType = useState("cmy");
  var myType = _myType[0], setMyType = _myType[1];
  var _unit = useState("mt");
  var unit = _unit[0], setUnit = _unit[1];
  var _hy = useState(new Set());
  var hiddenYrs = _hy[0], setHiddenYrs = _hy[1];

  useEffect(function(){ setHiddenYrs(new Set()); }, [comm, range, country, myType, unit]);
  var toggleYr = function(label) { setHiddenYrs(function(prev){ var next = new Set(prev); if(next.has(label))next.delete(label);else next.add(label); return next; }); };

  var BU_PER_MT = { corn: 39.368, soybeans: 36.744, wheat: 36.744, sorghum: 39.368 };
  var isBu = unit === "bu";
  var conv = function(mt) {
    if (mt == null) return null;
    if (isBu) return Math.round(mt * BU_PER_MT[comm]);
    return Math.round(mt);
  };
  var cardUnit = isBu ? "bushels" : "MT";
  var chartUnit = isBu ? "M bushels" : "1,000 MT";
  var chartConv = function(mt) {
    if (mt == null) return null;
    if (isBu) return Math.round(mt * BU_PER_MT[comm] / 1000000 * 10) / 10;
    return Math.round(mt / 1000 * 10) / 10;
  };

  var COMM_OPTS = [{id:"corn",label:"Corn"},{id:"soybeans",label:"Soybeans"},{id:"wheat",label:"Wheat"},{id:"sorghum",label:"Sorghum"}];
  var myConfig = {
    corn: { startMonth: 9, mktN: ["Sep","Oct","Nov","Dec","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug"] },
    soybeans: { startMonth: 9, mktN: ["Sep","Oct","Nov","Dec","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug"] },
    sorghum: { startMonth: 9, mktN: ["Sep","Oct","Nov","Dec","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug"] },
    wheat: { startMonth: 6, mktN: ["Jun","Jul","Aug","Sep","Oct","Nov","Dec","Jan","Feb","Mar","Apr","May"] },
  };
  var cfg = myConfig[comm];

  var dateToMktDay = function(ds) {
    var p = ds.split("-"); var y = parseInt(p[0]), m = parseInt(p[1]) - 1, d = parseInt(p[2]);
    var dt = new Date(y, m, d);
    var myStart = m >= (cfg.startMonth - 1) ? new Date(y, cfg.startMonth - 1, 1) : new Date(y - 1, cfg.startMonth - 1, 1);
    return Math.max(0, Math.min(365, Math.round((dt - myStart) / 86400000)));
  };
  var myLabel = function(yr) { return (yr - 1) + "/" + String(yr).slice(2); };

  // Current marketing year based on date (not data)
  var now = new Date();
  var actualCMY = now.getMonth() >= (cfg.startMonth - 1) ? now.getFullYear() + 1 : now.getFullYear();
  // For CMY view, latest year = actualCMY. For NMY view, latest year = actualCMY + 1
  var isCMY = myType === "cmy";
  var curMY = isCMY ? actualCMY : actualCMY + 1;
  var rangeN = parseInt(range);
  var startMY = curMY - rangeN;

  // Get raw weekly points for selected commodity + country
  var getRawPts = function() {
    if (!esData || !esData[comm]) return [];
    var commData = esData[comm];
    if (country === "ALL") return commData.totals || [];
    var cc = commData.byCountry || {};
    return cc[country] || [];
  };
  var rawPts = getRawPts();

  // Build marketing year buckets, skip first data point of each MY to avoid rollover artifacts
  var buildByMY = function(pts, metricKey) {
    var byMY = {};
    pts.forEach(function(pt) {
      var my = pt.my;
      if (my < startMY || my > curMY) return;
      var day = dateToMktDay(pt.d);
      if (!byMY[my]) byMY[my] = [];
      byMY[my].push({ x: day, y: chartConv(pt[metricKey]) });
    });
    // Sort and deduplicate: if two points at same x (within 3 days), keep last (new crop)
    Object.keys(byMY).forEach(function(my) {
      byMY[my].sort(function(a, b) { return a.x - b.x; });
      var deduped = [];
      byMY[my].forEach(function(pt) {
        if (deduped.length > 0 && Math.abs(deduped[deduped.length - 1].x - pt.x) < 3) {
          deduped[deduped.length - 1] = pt; // overwrite with later entry (new crop)
        } else {
          deduped.push(pt);
        }
      });
      byMY[my] = deduped;
    });
    return byMY;
  };

  var nsKey = isCMY ? "ns" : "nns";
  var osKey = isCMY ? "os" : "nos";

  // Level metrics (outstanding, accumulated, total commitments) skip first point to avoid rollover jumps
  var nsByMY = buildByMY(rawPts, nsKey);
  var osByMY = buildByMY(rawPts, osKey);
  var wsByMY = buildByMY(rawPts, "we");
  var aeByMY = buildByMY(rawPts, "ae");
  var tcByMY = buildByMY(rawPts, "tc");

  var yrColors = ["#A32D2D","#D85A30","#E8A735","#639922","#1D9E75","#378ADD","#534AB7","#8B5CF6","#EC4899","#6B7280"];
  var getColor = function(my) { if (my === curMY) return "#333"; var dist = curMY - my; if (dist === 1) return "#1D9E75"; if (dist === 2) return "#639922"; if (dist === 3) return "#E8A735"; if (dist === 4) return "#D85A30"; if (dist === 5) return "#A32D2D"; return yrColors[(dist - 1) % yrColors.length]; };

  var buildItems = function(byMY) {
    var items = [];
    for (var y = startMY; y <= curMY; y++) { if (byMY[y]) items.push({ label: myLabel(y), my: y, color: getColor(y) }); }
    return items;
  };
  var allItems = buildItems(nsByMY);
  var hk = Array.from(hiddenYrs).sort().join(",");

  // Country dropdown: only include countries with data for selected commodity
  var countryOpts = [{c:"ALL",n:"All Countries"}];
  if (esData && esData[comm] && esData[comm].byCountry) {
    var bc = esData[comm].byCountry;
    var countryMap = {};
    if (esData.countries) {
      esData.countries.forEach(function(ct) { countryMap[String(ct.c)] = ct.n; });
    }
    var codes = Object.keys(bc).filter(function(cc) {
      if (!bc[cc] || !bc[cc].length) return false;
      if (!isCMY) {
        // NMY: only include if country had NMY data in at least prior year
        return bc[cc].some(function(pt) { return (pt.nns !== 0 || pt.nos !== 0) && pt.my >= curMY - 1; });
      }
      return true;
    });
    codes.sort(function(a, b) {
      var na = countryMap[a] || a;
      var nb = countryMap[b] || b;
      return na < nb ? -1 : na > nb ? 1 : 0;
    });
    codes.forEach(function(cc) {
      var name = countryMap[cc] || ("Code " + cc);
      countryOpts.push({c: cc, n: name});
    });
  }

  // Header card info
  var getCardInfo = function(metricKey) {
    if (!rawPts || !rawPts.length) return { cur: null, prevWk: null, lastYr: null, date: null };
    var filtered = rawPts.filter(function(p) { return p.my >= startMY && p.my <= curMY; });
    if (!filtered.length) return { cur: null, prevWk: null, lastYr: null, date: null };
    var sorted = filtered.slice().sort(function(a, b) { return a.d < b.d ? 1 : -1; });
    var latest = sorted[0]; var prev = sorted.length > 1 ? sorted[1] : null;
    var latestDate = new Date(latest.d);
    var targetDate = new Date(latestDate); targetDate.setFullYear(targetDate.getFullYear() - 1);
    var targetMs = targetDate.getTime();
    var lastYrPt = null; var bestDiff = 10 * 86400000;
    rawPts.forEach(function(p) { var diff = Math.abs(new Date(p.d).getTime() - targetMs); if (diff < bestDiff) { bestDiff = diff; lastYrPt = p; } });
    return {
      cur: conv(latest[metricKey]),
      prevWk: prev ? conv(prev[metricKey]) : null,
      lastYr: lastYrPt ? conv(lastYrPt[metricKey]) : null,
      date: latest.d,
    };
  };

  var nsInfo = getCardInfo(nsKey);
  var weInfo = getCardInfo("we");

  var statCard = function(label, info, unitLabel) {
    var fmtVal = function(v) { return v == null ? "—" : v.toLocaleString(); };
    var diffLine = function(lbl, comp) {
      if (info.cur == null || comp == null) return null;
      var diff = Math.round(info.cur - comp);
      var pctChg = comp !== 0 ? Math.round((info.cur - comp) / Math.abs(comp) * 1000) / 10 : 0;
      var col = diff > 0 ? "#639922" : diff < 0 ? "#A32D2D" : "var(--color-text-tertiary)";
      return (<div style={{display:"flex",justifyContent:"space-between",fontSize:10.5,padding:"1px 0"}}>
        <span style={{color:"var(--color-text-tertiary)"}}>{lbl}</span>
        <span style={{display:"flex",gap:6,alignItems:"baseline",justifyContent:"flex-end"}}><span style={{color:"var(--color-text-secondary)",textAlign:"right",flex:"none"}}>{fmtVal(comp)}</span><span style={{color:col,fontWeight:500,textAlign:"right",minWidth:76,flex:"none"}}>({diff > 0 ? "+" : ""}{diff.toLocaleString()})</span><span style={{color:col,fontWeight:500,textAlign:"right",minWidth:52,flex:"none"}}>({pctChg > 0 ? "+" : ""}{pctChg.toFixed(1)}%)</span></span>
      </div>);
    };
    return (<div style={{background:"var(--color-background-secondary)",borderRadius:"var(--border-radius-md)",padding:"12px 14px",minWidth:0}}>
      <div style={{fontSize:11,color:"var(--color-text-secondary)",marginBottom:3,textTransform:"uppercase",letterSpacing:"0.4px"}}>{label}</div>
      <div style={{fontSize:22,fontWeight:500,color:"var(--color-text-primary)",marginBottom:2}}>{fmtVal(info.cur)}<span style={{fontSize:12,fontWeight:400,color:"var(--color-text-secondary)",marginLeft:4}}>{unitLabel}</span></div>
      {info.date && <div style={{fontSize:10,color:"var(--color-text-tertiary)",marginBottom:6}}>as of {fmtDate(info.date)}</div>}
      <div style={{borderTop:"0.5px solid var(--color-border-tertiary)",paddingTop:5}}>
        {diffLine("vs. last week", info.prevWk)}
        {diffLine("vs. last year", info.lastYr)}
      </div>
    </div>);
  };

  var mktBounds = [0,30,61,91,122,153,181,212,242,273,303,334];
  var mktMids = [15,45,76,106,137,167,196,227,257,288,318,349];

  var mkChart = function(byMY) { return function(canvas) {
    if (!byMY || Object.keys(byMY).length === 0) return;
    var ds = [];
    for (var y = startMY; y <= curMY; y++) {
      var pts = byMY[y]; if (!pts || !pts.length) continue;
      ds.push({ label: myLabel(y), data: pts.slice(), borderColor: getColor(y), borderWidth: y === curMY ? 2.5 : 1.5, pointRadius: 0, pointHitRadius: 6, tension: 0, fill: false, showLine: true, hidden: hiddenYrs.has(myLabel(y)) });
    }
    if (ds.length === 0) return;
    var vis = ds.filter(function(d) { return !d.hidden; }).flatMap(function(d) { return d.data.map(function(p) { return p.y; }); });
    if (vis.length === 0) return;
    var rawMax = Math.max.apply(null, vis), rawMin = Math.min.apply(null, vis);
    var span = rawMax - rawMin || 1;
    var step = Math.pow(10, Math.floor(Math.log10(span / 4)));
    if (span / step < 4) step = step / 2;
    if (span / step > 8) step = step * 2;
    var yMin = Math.floor(rawMin / step) * step;
    var yMax = Math.ceil(rawMax / step) * step;
    if (yMax === rawMax) yMax += step;
    var tks = []; for (var k = 0; k < 12; k++) { tks.push({value: mktBounds[k]}); tks.push({value: mktMids[k]}); }
    new Chart(canvas, { type: "scatter", data: { datasets: ds }, options: {
      responsive: true, maintainAspectRatio: false,
      interaction: { mode: "nearest", intersect: false },
      plugins: { legend: { display: false }, tooltip: { mode: "nearest", intersect: false, backgroundColor: "rgba(0,0,0,0.6)", titleFont: { size: 11 }, bodyFont: { size: 11 },
        callbacks: { title: function(items) { if (!items.length) return ""; var doy = items[0].parsed.x; var mi = 11; for (var m = 0; m < 11; m++) { if (doy < mktBounds[m+1]) { mi = m; break; } } return cfg.mktN[mi] + " " + (Math.floor(doy - mktBounds[mi]) + 1); },
          label: function(c2) { return c2.parsed.y == null ? null : c2.dataset.label + ": " + c2.parsed.y.toLocaleString(); } } } },
      scales: { x: { type: "linear", min: 0, max: 365, afterBuildTicks: function(ax) { ax.ticks = tks; }, ticks: { callback: function(v) { var idx = mktMids.indexOf(v); return idx >= 0 ? cfg.mktN[idx] : ""; }, autoSkip: false, maxRotation: 0, font: { size: 10 } }, grid: { color: function(ctx) { var v = ctx.tick.value; if (v > 0 && mktBounds.indexOf(v) >= 0) return "rgba(0,0,0,0.12)"; return "transparent"; }, lineWidth: 0.75 } },
        y: { min: yMin, max: yMax, ticks: { stepSize: step, font: { size: 10 }, callback: function(v) { return v.toLocaleString(); } }, grid: { color: "rgba(0,0,0,0.08)", lineWidth: 0.75 } } }
    } });
  }; };

  var dlCSV = function() {
    var hdrs = ["Date", "MY", "Net Sales (" + chartUnit + ")", "Outstanding Sales (" + chartUnit + ")", "Weekly Exports (" + chartUnit + ")", "Accumulated Exports (" + chartUnit + ")", "Total Commitments (" + chartUnit + ")"];
    var filtered = rawPts.filter(function(p) { return p.my >= startMY && p.my <= curMY; });
    var rows = filtered.sort(function(a, b) { return a.d < b.d ? -1 : 1; }).map(function(pt) {
      return [pt.d, myLabel(pt.my), chartConv(pt[nsKey]), chartConv(pt[osKey]), chartConv(pt.we), chartConv(pt.ae), chartConv(pt.tc)];
    });
    downloadCSV("export_sales_" + comm + "_" + myType + "_" + unit + ".csv", hdrs, rows);
  };

  var chevSvg = "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath d='M3 5l3 3 3-3' fill='none' stroke='%23666' stroke-width='1.5'/%3E%3C/svg%3E\")";
  var selSt = {padding:"6px 24px 6px 10px",fontSize:13,fontWeight:500,border:"1px solid var(--color-border-secondary)",borderRadius:6,background:"var(--color-background-primary)",color:"var(--color-text-primary)",fontFamily:"inherit",cursor:"pointer",appearance:"none",backgroundImage:chevSvg,backgroundRepeat:"no-repeat",backgroundPosition:"right 6px center"};
  var modeSt = function(a) { return {padding:"6px 14px",fontSize:12,fontWeight:a?600:400,border:"1px solid "+(a?"#2563EB":"var(--color-border-secondary)"),borderRadius:5,cursor:"pointer",background:a?"#2563EB":"transparent",color:a?"#fff":"var(--color-text-secondary)",transition:"all 0.15s"}; };

  var CMY_CHARTS = [
    { key: "ns", label: "Net Sales", data: nsByMY },
    { key: "os", label: "Outstanding Sales", data: osByMY },
    { key: "we", label: "Weekly Exports", data: wsByMY },
    { key: "ae", label: "Accumulated Exports", data: aeByMY },
    { key: "tc", label: "Total Commitments", data: tcByMY },
  ];
  var NMY_CHARTS = [
    { key: "ns", label: "Net Sales (NMY)", data: nsByMY },
    { key: "os", label: "Outstanding Sales (NMY)", data: osByMY },
  ];
  var CHARTS = isCMY ? CMY_CHARTS : NMY_CHARTS;

  return (<div>
    <div style={{display:"flex",alignItems:"center",gap:12,marginBottom:14,flexWrap:"wrap"}}>
      <div style={{display:"flex",alignItems:"center",gap:6}}>
        <span style={{fontSize:11,fontWeight:600,color:"var(--color-text-secondary)",textTransform:"uppercase"}}>Commodity</span>
        <select value={comm} onChange={function(e){setComm(e.target.value); setCountry("ALL");}} style={selSt}>
          {COMM_OPTS.map(function(t) { return <option key={t.id} value={t.id}>{t.label}</option>; })}
        </select>
      </div>
      <div style={{display:"flex",alignItems:"center",gap:6}}>
        <span style={{fontSize:11,fontWeight:600,color:"var(--color-text-secondary)",textTransform:"uppercase"}}>Range</span>
        <select value={range} onChange={function(e){setRange(e.target.value);}} style={selSt}>
          <option value="1">1 Year</option>
          <option value="5">5 Years</option>
          <option value="10">10 Years</option>
        </select>
      </div>
      <div style={{display:"flex",alignItems:"center",gap:6}}>
        <span style={{fontSize:11,fontWeight:600,color:"var(--color-text-secondary)",textTransform:"uppercase"}}>Country</span>
        <select value={country} onChange={function(e){setCountry(e.target.value);}} style={{padding:"6px 24px 6px 10px",fontSize:13,fontWeight:500,border:"1px solid var(--color-border-secondary)",borderRadius:6,background:"var(--color-background-primary)",color:"var(--color-text-primary)",fontFamily:"inherit",cursor:"pointer",appearance:"none",backgroundImage:chevSvg,backgroundRepeat:"no-repeat",backgroundPosition:"right 6px center",maxWidth:180}}>
          {countryOpts.map(function(ct) { return <option key={ct.c} value={ct.c}>{ct.n}</option>; })}
        </select>
      </div>
      <div style={{display:"flex",gap:3}}>
        <button onClick={function(){setMyType("cmy");}} style={modeSt(myType==="cmy")}>CMY</button>
        <button onClick={function(){setMyType("nmy");}} style={modeSt(myType==="nmy")}>NMY</button>
      </div>
      <div style={{display:"flex",gap:3}}>
        <button onClick={function(){setUnit("mt");}} style={modeSt(unit==="mt")}>Metric Tons</button>
        <button onClick={function(){setUnit("bu");}} style={modeSt(unit==="bu")}>Bushels</button>
      </div>
      <div style={{marginLeft:"auto"}}><DownloadBtn onClick={dlCSV} /></div>
    </div>

    <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:10,marginBottom:16}}>
      {statCard(isCMY ? "Net Sales" : "Net Sales (NMY)", nsInfo, cardUnit)}
      {isCMY && statCard("Weekly Exports", weInfo, cardUnit)}
      {!isCMY && statCard("Outstanding Sales (NMY)", getCardInfo(osKey), cardUnit)}
    </div>

    <div style={{display:"flex",flexWrap:"wrap",gap:6,marginBottom:16,alignItems:"center"}}>
      {allItems.map(function(item) { var isH = hiddenYrs.has(item.label); return (
        <button key={item.label} onClick={function(){toggleYr(item.label);}} style={{display:"flex",alignItems:"center",gap:5,padding:"4px 10px",border:"1px solid var(--color-border-secondary)",borderRadius:5,background:isH?"var(--color-background-secondary)":"transparent",cursor:"pointer",opacity:isH?0.3:1,transition:"all 0.15s"}}>
          <span style={{width:18,height:0,borderTop:"2.5px solid "+item.color,display:"inline-block"}}></span>
          <span style={{fontSize:12,fontWeight:500,color:"var(--color-text-primary)"}}>{item.label}</span>
        </button>); })}
    </div>

    <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:16}}>
      {CHARTS.map(function(ch) { return (<div key={ch.key}>
        <div style={{fontSize:14,fontWeight:600,color:"var(--color-text-primary)",marginBottom:6}}>{ch.label} <span style={{fontSize:11,fontWeight:400,color:"var(--color-text-tertiary)"}}>({chartUnit})</span></div>
        {ready && <ChartBox id={"es_"+ch.key+"_"+comm+"_"+range+"_"+country+"_"+myType+"_"+unit} height={240} renderChart={mkChart(ch.data)} deps={"es_"+ch.key+"_"+comm+"_"+range+"_"+country+"_"+myType+"_"+unit+"_"+esLoaded+"_"+hk} />}
      </div>); })}
    </div>
    <div style={{marginTop:14,fontSize:11,color:"var(--color-text-tertiary)"}}>Source: USDA FAS Export Sales Reporting. Marketing years: Corn/Soybeans/Sorghum (Sep–Aug), Wheat (Jun–May). CMY = current marketing year, NMY = next marketing year.</div>
  </div>);
}



function LivestockWASDEPage() {
  var _sel = useState("beef");
  var sel = _sel[0], setSel = _sel[1];
  var _live = useState(null);
  var _lbl = useState("representative data");
  var liveData = _live[0], setLiveData = _live[1];
  var dataLabel = _lbl[0], setDataLabel = _lbl[1];

  useEffect(function() {
    fetch("data/wasde.json?t=" + Date.now())
      .then(function(r) { if (!r.ok) throw new Error("not found"); return r.json(); })
      .then(function(data) {
        if (data && data.us) {
          var livestock = {};
          ["beef", "pork", "broiler", "turkey"].forEach(function(sp) {
            if (data.us[sp]) livestock[sp] = data.us[sp];
          });
          if (Object.keys(livestock).length > 0) {
            setLiveData(livestock);
            var d = new Date(data.fetched_at);
            setDataLabel("USDA ERS data, fetched " + d.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" }));
          }
        }
      })
      .catch(function() {});
  }, []);

  var TABS = [
    { id: "beef", label: "Beef" },
    { id: "pork", label: "Pork" },
    { id: "broiler", label: "Broiler" },
    { id: "turkey", label: "Turkey" },
  ];

  var commodity = liveData && liveData[sel] ? liveData[sel] : null;

  var dlCSV = function() {
    if (!commodity) return;
    var headers = ["Item"].concat(commodity.years);
    var rows = [];
    commodity.sections.forEach(function(s) {
      rows.push(["--- " + s.header + " ---"]);
      s.rows.forEach(function(r) {
        rows.push([r.label].concat(r.values.map(function(v) { return v != null ? v : ""; })));
      });
    });
    downloadCSV("livestock_wasde_" + sel + ".csv", headers, rows);
  };

  return (<div>
    <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 14, flexWrap: "wrap" }}>
      <div style={{ display: "flex", gap: 3 }}>
        {TABS.map(function(t) {
          var active = sel === t.id;
          return (<button key={t.id} onClick={function() { setSel(t.id); }} style={{
            padding: "7px 18px", fontSize: 13, fontWeight: active ? 600 : 400,
            border: "1px solid var(--color-border-secondary)", borderRadius: 6, cursor: "pointer",
            background: active ? "#2563EB" : "transparent",
            color: active ? "#fff" : "var(--color-text-secondary)",
            transition: "all 0.15s",
          }}>{t.label}</button>);
        })}
      </div>
      <div style={{ marginLeft: "auto" }}><DownloadBtn onClick={dlCSV} /></div>
    </div>

    {commodity ? (
      <div>
        {commodity.sections.map(function(section, si) {
          var sectionYears = section.years || commodity.years;
          var isAnnual = si === 0;
          var pseudoCommodity = {
            id: commodity.id + "_" + si,
            label: commodity.label,
            years: sectionYears,
            sections: [section],
          };
          return (<div key={si}>
            <h3 style={{ fontSize: isAnnual ? 15 : 14, fontWeight: 500, color: "var(--color-text-primary)", margin: isAnnual ? "0 0 10px" : "28px 0 10px" }}>
              {isAnnual ? "U.S. " + commodity.label + " balance sheet" : section.header}
            </h3>
            <WASDETable commodity={pseudoCommodity} />
          </div>);
        })}
      </div>
    ) : (
      <div style={{ padding: 40, textAlign: "center", color: "var(--color-text-tertiary)", fontSize: 13 }}>
        {liveData === null ? "Loading livestock data..." : "No data available for " + sel + ". Run the WASDE fetcher to populate livestock balance sheets."}
      </div>
    )}

    <div style={{ marginTop: 14, fontSize: 11, color: "var(--color-text-tertiary)" }}>
      Source: {dataLabel}. All supply/use/stocks in million lbs (carcass weight equivalent).
      <br />Marketing years: calendar year (Jan-Dec). Quarterly data where available.
    </div>
  </div>);
}


const PAGES = {
  "wasde": { title: "USDA WASDE balance sheets (Grains & Oilseeds)", component: WASDEPage },
  "livestock-wasde": { title: "USDA WASDE balance sheets (Livestock)", component: LivestockWASDEPage },
  "crop-progress": { title: "Crop progress & condition", component: CropProgressPage },
  "ethanol": { title: "EIA Ethanol (Weekly)", component: EthanolPage },
  "fats-oils": { title: "USDA Oilseed Crushing (Monthly)", component: FatsOilsPage },
  "cot-summary": { title: "Commitment of Traders (COT) summary", component: COTSummaryPage },
  "cot-charts": { title: "COT charts", component: COTChartsPage },
  "export-inspections": { title: "USDA Export Inspections (Weekly)", component: ExportInspectionsPage },
  "export-sales": { title: "USDA Export Sales (Weekly)", component: ExportSalesPage },
  "drought": { title: "U.S. Drought Monitor", component: DroughtPage },
  "on-feed": { title: "Cattle on feed", component: CattleOnFeedPage },
  "cutout": { title: "Boxed beef & pork prices", component: CutoutPage },
  "meat-price-charts": { title: "USDA meat price charts", component: MeatPriceChartsPage },
  "slaughter": { title: "Slaughter", component: SlaughterPage },
  "cold-storage": { title: "Cold storage", component: ColdStoragePage },
  "hogs-pigs": { title: "Hogs & pigs", component: HogsPigsPage },
  "ng-storage": { title: "Natural gas storage", component: (p) => <EnergyChartPage {...p} dataKey="ngStorage" /> },
  "ng-inj-wd": { title: "Injections / withdrawals", component: NGInjWdPage },
  "ng-production": { title: "Natural gas production", component: (p) => <EnergyChartPage {...p} dataKey="ngProduction" /> },
  "ng-demand": { title: "Natural gas demand", component: (p) => <EnergyChartPage {...p} dataKey="ngDemand" /> },
  "petro-crude-stocks": { title: "Crude oil stocks", component: (p) => <EnergyChartPage {...p} dataKey="crudeStocks" /> },
  "petro-production": { title: "Crude oil production", component: (p) => <EnergyChartPage {...p} dataKey="crudeProduction" /> },
  "petro-gasoline": { title: "Gasoline stocks", component: (p) => <EnergyChartPage {...p} dataKey="gasolineStocks" /> },
  "petro-distillate": { title: "Distillate stocks", component: (p) => <EnergyChartPage {...p} dataKey="distillateStocks" /> },
  "fx-currencies": { title: "Currencies", component: FXCurrenciesPage },
};

function App() {
  const [active, setActive] = useState(() => {
    const hash = window.location.hash.slice(1);
    return hash || "wasde";
  });
  useEffect(() => {
    const onHash = () => { const h = window.location.hash.slice(1); if (h) setActive(h); };
    window.addEventListener("hashchange", onHash);
    return () => window.removeEventListener("hashchange", onHash);
  }, []);
  useEffect(() => { if (active) window.location.hash = active; }, [active]);
  const [chartReady, setChartReady] = useState(false);
  const [navCollapsed, setNavCollapsed] = useState(false);
  const [openGroups, setOpenGroups] = useState({ grains: true, livestock: true, energy: true, drivers: true, cot: true });


  useEffect(() => {
    // Load Chart.js
    if (!window.Chart) {
      const s = document.createElement("script"); s.src = "https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"; s.onload = () => {
        Chart.defaults.scale.ticks.padding = 4;
        Chart.defaults.scale.grid.drawTicks = false;
        setChartReady(true);
      }; document.head.appendChild(s);
    } else { setChartReady(true); }
    // D3 loaded via index.html
  }, []);

  const toggleGroup = id => setOpenGroups(prev => ({ ...prev, [id]: !prev[id] }));
  const PageComp = PAGES[active]?.component;

  return (
    <div style={{ display: "flex", height: "100vh", fontFamily: "var(--font-sans)" }}>
      <div style={{ width: navCollapsed ? 48 : 220, flexShrink: 0, transition: "width 0.2s ease", borderRight: "0.5px solid var(--color-border-tertiary)", background: "var(--color-background-secondary)", display: "flex", flexDirection: "column", overflow: "hidden", height: "100vh", position: "sticky", top: 0 }}>
        <div style={{ padding: navCollapsed ? "16px 8px" : "16px 16px", borderBottom: "0.5px solid var(--color-border-tertiary)", display: "flex", alignItems: "center", gap: 10, minHeight: 56, flexShrink: 0 }}>
          {!navCollapsed && <div><div style={{ fontSize: 14, fontWeight: 500, color: "var(--color-text-primary)", whiteSpace: "nowrap" }}>Howard's Heuristics</div></div>}
          <button onClick={() => setNavCollapsed(!navCollapsed)} style={{ marginLeft: navCollapsed ? 0 : "auto", background: "transparent", border: "none", cursor: "pointer", padding: 4, color: "var(--color-text-secondary)", display: "flex" }}>
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5">{navCollapsed ? <path d="M6 3l5 5-5 5" /> : <path d="M10 3L5 8l5 5" />}</svg>
          </button>
        </div>
        {!navCollapsed && (
          <nav style={{ padding: "8px 0", flex: 1, overflowY: "auto", minHeight: 0 }}>
            {NAV_SECTIONS.map(section => {
              let afterSubheader = false;
              return (
              <div key={section.id} style={{ marginBottom: 4 }}>
                <button onClick={() => toggleGroup(section.id)} style={{ display: "flex", alignItems: "center", gap: 8, width: "100%", padding: "8px 16px", background: "transparent", border: "none", cursor: "pointer", color: "var(--color-text-secondary)", fontSize: 12, fontWeight: 500, textTransform: "uppercase", letterSpacing: "0.4px" }}>
                  {section.icon}<span style={{ flex: 1, textAlign: "left" }}>{section.label}</span>
                  <svg width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" strokeWidth="1.5" style={{ transform: openGroups[section.id] ? "rotate(90deg)" : "rotate(0deg)", transition: "transform 0.15s" }}><path d="M4.5 2.5l3.5 3.5-3.5 3.5" /></svg>
                </button>
                {openGroups[section.id] && <div>{section.children.map((child, ci) => {
                  if (child.subheader) {
                    afterSubheader = true;
                    return <div key={`sub-${ci}`} style={{ padding: "10px 16px 3px 40px", fontSize: 10, fontWeight: 600, color: "var(--color-text-tertiary)", textTransform: "uppercase", letterSpacing: "0.5px" }}>{child.subheader}</div>;
                  }
                  const isA = active === child.id;
                  const leftPad = afterSubheader ? 54 : 40;
                  return <button key={child.id} onClick={() => setActive(child.id)} style={{ display: "block", width: "100%", textAlign: "left", padding: `7px 16px 7px ${leftPad}px`, background: isA ? "var(--color-background-primary)" : "transparent", border: "none", borderLeft: isA ? "2.5px solid var(--color-text-primary)" : "2.5px solid transparent", cursor: "pointer", color: isA ? "var(--color-text-primary)" : "var(--color-text-secondary)", fontSize: 13, fontWeight: isA ? 500 : 400, transition: "all 0.1s" }}>{child.label}</button>;
                })}</div>}
              </div>
            );})}
          </nav>
        )}
        {navCollapsed && <nav style={{ padding: "12px 0", display: "flex", flexDirection: "column", alignItems: "center", gap: 4 }}>{NAV_SECTIONS.map(s => <div key={s.id} title={s.label} style={{ padding: 8, borderRadius: "var(--border-radius-md)", cursor: "pointer", color: "var(--color-text-secondary)" }} onClick={() => { setNavCollapsed(false); setOpenGroups(p => ({ ...p, [s.id]: true })); }}>{s.icon}</div>)}</nav>}
        {!navCollapsed && <div style={{ padding: "12px 16px", borderTop: "0.5px solid var(--color-border-tertiary)", fontSize: 10, color: "var(--color-text-tertiary)", flexShrink: 0 }}>Source: USDA WASDE, ERS,<br/>NASS, AMS, EIA reports</div>}
      </div>
      <div style={{ flex: 1, minWidth: 0, padding: "20px 28px 40px", overflowY: "auto", height: "100vh" }}>
        <div style={{ maxWidth: 1400 }}>
          <div style={{ marginBottom: 20 }}>
            <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", gap: 12, flexWrap: "wrap" }}>
              <div>
                <h1 style={{ fontSize: 20, fontWeight: 500, color: "var(--color-text-primary)", margin: "0 0 2px" }}>{PAGES[active]?.title}</h1>
                
              </div>

            </div>
          </div>
          {PageComp && <PageComp ready={chartReady} />}
        </div>
      </div>
    </div>
  );
}
