"use strict";

var TIMES = [
    {
        time: 30 * 24,
        longDesc: "la vida promedio de la Mosca Común",
        shortDesc: "Mosca Común",
        source: 'http://www.orkin.com/flies/house-fly/life-expectancy-of-house-fly/'
    },
    {
        time: 45 / 60,
        longDesc: "la guerra Anglo-Zanzibariana",
        shortDesc: "Guerra Anglo-Zanzibariana",
        source: 'http://es.wikipedia.org/wiki/Guerra_anglo-zanzibariana'
    },
    {
        time: 12144 / 60,
        longDesc: "ver las 25 temporadas de Los Simpsons",
        shortDesc: "Los Simpsons",
        source: 'http://time.com/3154224/simpsons-marathon-fxx/'
    },
    {
        time: 136 * 100 / 60,
        longDesc: "ver Matrix 100 veces",
        shortDesc: "Matrix * 100",
        source: 'http://www.imdb.com/title/tt0133093/'
    },
    {
        time: 40,
        longDesc: "la LAN party mas larga de la historia",
        shortDesc: "LAN party",
        source: 'http://www.guinnessworldrecords.com/world-records/longest-lan-party/'
    },
    {
        time: 280.8 / 60,
        longDesc: "lo que tarda la luz en viajar de la Tierra a Pluton",
        shortDesc: "Tierra a Pluton a 1c",
        source: 'http://www.wolframalpha.com/input/?i=time+from+earth+to+pluto'
    },
    {
        time: 201 * 50 / 60,
        longDesc: "ver LotR: The Return of the King 50 veces",
        shortDesc: "LotR 3 * 50",
        source: 'http://www.imdb.com/title/tt0167260/'
    },
    {
        time: 240,
        longDesc: "ver la película más larga del mundo",
        shortDesc: "Modern Times Forever",
        source: 'http://en.wikipedia.org/wiki/Modern_Times_Forever_%28Stora_Enso_Building,_Helsinki%29'
    },
    {
        time: 17 * 24,
        longDesc: "lo que duró el Estado de Singapur como Estado Soberano",
        shortDesc: "Estado de Singapur",
        source: 'http://en.wikipedia.org/wiki/History_of_Singapore#Full_internal_self-government'
    },
];

function svg_wrap(text, width) {
  text.each(function() {
    var text = d3.select(this),
        words = text.text().split(/\s+/).reverse(),
        word,
        line = [],
        lineNumber = 0,
        lineHeight = 1.1, // ems
        y = text.attr("y"),
        dy = parseFloat(text.attr("dy")),
        tspan = text.text(null).append("tspan").attr("x", 0).attr("y", y).attr("dy", dy + "em");
    while (word = words.pop()) {
      line.push(word);
      tspan.text(line.join(" "));
      if (tspan.node().getComputedTextLength() > width) {
        line.pop();
        tspan.text(line.join(" "));
        line = [word];
        tspan = text.append("tspan").attr("x", 0).attr("y", y).attr("dy", ++lineNumber * lineHeight + dy + "em").text(word);
      }
    }
  });
}

function abc(i){
    var def = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
        'J', 'K', 'L', 'M', 'N', 'O', 'P',
        'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'];
    return def[i];
}
