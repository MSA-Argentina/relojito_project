"use strict";

function ß(name){
    // Create a function that returns a particular property of its parameter.
    // If that property is a function, invoke it (and pass optional params).
    var v,params=Array.prototype.slice.call(arguments,1);
    return function(o){
        return (typeof (v=o[name])==='function' ? v.apply(o,params) : v );
    };
}

function time_stats(data){
    $("#total-time").text(data.total_hours);
    $("#total-tasks").text(data.total_tasks);
}

function time_chart(id, user_hours){
    var user_d = {
        time: user_hours,
        longDesc: "horas trabajadas",
        shortDesc: "Tus Horas"
    };

    var closest_time = _.min(TIMES, function(n){
        return Math.abs(user_hours - n.time)
    });

    var data = [user_d, closest_time];

    $('<span />')
        .addClass('hour-info')
        .text(['Comparadas con',
               data[1].longDesc,
               '(' + round(data[1].time) + 'hs)',
               'tenemos:'].join(' '))
        .appendTo(id);

    var margin = {top: 30, right: 70, bottom: 0, left: 150};
    var width = 400;
    var barHeight = 25;
    var height = barHeight * data.length;

    var xScale = d3.scale.linear()
        .domain([0, d3.max(data, ß('time'))])
        .range([0, width]);

    var chart = d3.select(id).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    chart.append("g")
        .attr("class", "labels")
      .selectAll("text")
        .data(data)
      .enter().append("text")
        .attr("class", "label")
        .attr("y", function(d, i){ return i * barHeight + (barHeight/2) + 2; })
        .attr("x", -5)
        .attr("text-anchor", "end")
        .text(ß('shortDesc'));

    chart.append("g")
        .attr("class", "bars")
      .selectAll("rect")
        .data(data)
      .enter().append("rect")
        .attr("class", "bar")
        .attr("y", function(d, i){ return i * barHeight; })
        .attr("height", barHeight - 5)
        .attr("width", function(d){ return xScale(d.time) });

    chart.append("g")
        .attr("class", "numbers")
      .selectAll("text")
        .data(data)
      .enter().append("text")
        .attr("class", "number")
        .attr("y", function(d, i){ return i * barHeight + (barHeight/2) + 2; })
        .attr("x", function(d){ return xScale(d.time) + 5 })
        .attr("text-anchor", "start")
        .text(function(d){ return round(d.time) + 'hs' });

}

function project_stats(projects){
    var count = projects.length;
    var mean = round(d3.mean(projects, ß('total_hours__sum')));
    var median = round(d3.median(projects, ß('total_hours__sum')));
    $("#project-count").text(count);
    $("#project-mean").text(mean + ' horas');
    $("#project-median").text(median + ' horas');
}

function project_chart(id, unsorted_data){
    // data: [
    //          ["Name P1", x1],
    //          ["Name P2", x2],
    //          ...
    //       ]
    var data = _(unsorted_data)
        .sortBy('total_hours__sum')
        .reverse()
        .value();

    $('<table/>')
        .addClass('table pull-left table-bordered project-table')
        .append(_.map(data, function(p, i){
            var $proj = $('<th/>').text(p.project__name);
            var $hours = $('<td/>').text(p.total_hours__sum + 'hs');
            return $('<tr/>').append([$proj, $hours]);
        }))
        .appendTo(id);

    var $chart = $('<div id="project-chart-cell"/>')
        .appendTo(id);

    var margin = {top: 0, right: 0, bottom: 20, left: 0};
    var width = 360;
    var barHeight = 34;
    var barSpace = 10;
    var height = barHeight * data.length;

    var dmax = d3.max(data, ß('total_hours__sum'));
    var xScale = d3.scale.linear()
        .domain([0, (dmax*0.1) + dmax])
        .range([0, width]);

    var xAxis = d3.svg.axis()
        .scale(xScale)
        .orient("bottom")
        .tickSize(height, 0);

    var chart = d3.select("#project-chart-cell").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    chart.append("g")
        .attr("class", "axis")
        .call(xAxis);

    chart.append("g")
        .attr("class", "bars")
      .selectAll("rect")
        .data(data)
      .enter().append("rect")
        .attr("class", "bar")
        .attr("fill", ß('project__color'))
        .attr("y", function(d, i){ return barSpace / 2 + i * barHeight; })
        .attr("height", barHeight - barSpace)
        .attr("width", function(d){ return xScale(d.total_hours__sum) });
}

function type_stats(data){
    $('#total-types').text(data.all_task_types.length);
    $('#user-types').text(data.total_tasks_per_type.length);
}

function type_project_chart(id, plain_data){
    /* `index` is a [0..max_task_type_pk] x [0..max_project_pk] array
     * initialized like [[0,0,...],[0,0,...],...]
     * updated by iterating over `tasks`.
     * Then it's used for the actual `data` later.
     */

    var max_t = _.max(plain_data.all_task_types, 'pk');
    var max_p = _.max(plain_data.projects, 'pk');

    var index = _.map(_.range(max_t.pk + 1),
            function(){ return _.map(_.range(max_p.pk + 1),
                _.constant(0)) });

    _.forEach(plain_data.tasks, function(t){
        index[t.task_type_id][t.project_id] += t.total_hours;
    });

    var task_types = _.filter(plain_data.all_task_types,
            function(tt){ return 0 < sum(index[tt.pk]) });

    var data = [];
    _.forEach(task_types, function(tts, x){
        tts.i = x;
        _.forEach(plain_data.projects, function(ps, y){
            ps.i = y;
            var total = index[tts.pk][ps.pk];
            data.push({'x': x, 'y': y, 'total': total});
        });
    });

    var margin = {top: 30, right: 100, bottom: 20, left: 20};
    var width = 650 - margin.left - margin.right;
    var height = 500 - margin.top - margin.bottom;
    var cell_width = width / task_types.length;
    var cell_height = height / plain_data.projects.length;
    var font_size = 12;

    var color = d3.scale.quantize()
        .domain(d3.extent(data, ß('total')))
        .range(d3.range(9).map(function(d) { return "q" + d + "-9"; }));

    var colorZero = function(v){ return v === 0 ? 'zero' : color(v) };

    function showHours(d){
        var g = d3.select(this);
        var rect = g.select('rect');

        var x = ~~rect.attr('x');
        var y = ~~rect.attr('y');

        // checks if color is too dark
        if (d.total > color.invertExtent('q6-9')[0]) {
            var fill = 'white';
        } else {
            var fill = 'black';
        }

        g.append('text')
            .attr('transform', function(){ return 'translate(' + x + ',' + y + ')' })
            .attr('text-anchor', 'middle')
            .style('pointer-events', 'none')
            .attr('fill', fill)
            .attr('dx', cell_width / 2)
            .attr('dy', cell_height / 2 + font_size / 2 )
            .text(d.total + 'hs');
    }

    function hideHours(d){
        d3.select(this).select('text').remove();
    }

    var chart = d3.select(id).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .attr("class", "PuBuGn")
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var cells = chart.append("g")
        .attr("class", "rows")
      .selectAll("rect")
        .data(data)
      .enter().append("g")
        .on('mouseover', showHours)
        .on('mouseout', hideHours)
      .append("rect")
        .attr("class", function(d){ return 'cell ' + colorZero(d.total) })
        .attr("x", function(d){ return d.x * cell_width })
        .attr("y", function(d){ return d.y * cell_height })
        .attr("width", cell_width)
        .attr("height", cell_height);

    var titles = chart.append("g")
        .attr("class", "projects")
        .attr("transform", "translate(" + (width + 5) + ", 0)")
      .selectAll("text")
        .data(plain_data.projects)
      .enter().append("text")
        .attr("class", "label")
        .attr("font-size", font_size)
        .attr("y", function(d, i){ return i * cell_height + cell_height/2 + font_size/2 })
        .attr("dy", 0)
        .attr("text-anchor", "start")
        .text(function(d){ return d.name })
        .call(svg_wrap, 100);

    _.forEach([-5, height + font_size + 5], function(y){
        chart.append("g")
            .attr("class", "types")
          .selectAll("text")
            .data(task_types)
          .enter().append("text")
            .attr("class", "label")
            .attr("font-size", font_size)
            .attr("x", function(d, i){ return i * cell_width + cell_width/2 })
            .attr("y", y)
            .attr("text-anchor", "middle")
            .text(function(d){ return abc(d.i) });
    });

    d3.select(id).append('p')
        .attr('class', 'legend')
        .text('| ')
      .selectAll('span')
        .data(task_types)
      .enter().append('span')
        .html(function(d){ return '<b>' + abc(d.i) + '</b> = ' + d.name + ' | '; });
}

function word_stats(data){
    $("#word-count").text(data);
}

function word_chart(id, data){
    var margin = {top: 10, right: 10, bottom: 20, left: 10};
    var width = 700 - margin.left - margin.right;
    var height = 550 - margin.top - margin.bottom;

    var fill = d3.scale.category20();
    var rotations = 4;

    var rScale = d3.scale.linear()
        .domain([0, rotations - 1])
        .range([-60, 60]);

    var sScale = d3.scale.log()
        .domain(d3.extent(data, ß('size')))
        .range([13, 100]);

    d3.layout.cloud().size([width, height])
        .words(data)
        .rotate(function() { return rScale(~~(Math.random() * rotations)) })
        .font("Impact")
        .fontSize(function(d) { return sScale(d.size)})
        .on("end", draw)
        .start();

    function draw(words) {
        d3.select(id).append("svg")
            .attr("width", width)
            .attr("height", height)
          .append("g")
            .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")")
          .selectAll("text")
            .data(data)
          .enter().append("text")
            .style("font-size", function(d) { return d.size + "px" })
            .style("font-family", "Impact")
            .style("fill", function(d, i) { return fill(i) })
            .attr("text-anchor", "middle")
            .attr("transform", function(d) {
                return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
            })
            .text(function(d) { return d.text })
            .on('mouseover', showInfo)
            .on('mouseout', hideInfo);
    }

    function showInfo(d){
        $("#word-cloud-info").html('<b>' + d.text + '</b>' +
                ' aparece ' + d.size + ' veces, osea un ' +
                d3.format('%')(d.frequency));
    }

    function hideInfo(d){
        $("#word-cloud-info").html('&nbsp;');
    }
}

function round(n){
   return Math.floor(n * 100) / 100;
}

function sum(arr){
    return _.reduce(arr, function(acc, x){
        return x ? acc + x : acc;
    }, 0);
}

$.ajax({
    url: "/ajax_stats",
    type: "GET"
}).done(function(data){
      console.log(data);

      time_stats(data);
      time_chart("#total-time-bars", data.total_hours);

      project_stats(data.total_hours_per_project);
      project_chart("#project-bars", data.total_hours_per_project);

      type_stats(data);
      type_project_chart("#type-project-chart", data);

      word_stats(data.word_frequencies.total);
      word_chart("#word-cloud", data.word_frequencies.frequencies);
});
