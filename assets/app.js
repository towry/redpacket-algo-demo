/*!
 * Copyright 2016 Towry Wang, http://towry.me
 */

(function () {
	var parentNode = document.querySelector('.charts');
	var config = window.config || {};

	var chart = {
		create: function (total_money, data, max, min, index) {
			if (max < min) {
				throw new TypeError("max < min");
			}

			if (Object.prototype.toString.call(data) !== '[object Array]') {
				throw new TypeError("data must be an array");
			}
            
            data.sort();

			this._init(total_money, data, max, min, index);
			this._makeChart();
		},

		append: function (node) {
			if (!this._chartNode) {
				throw new Error("no chart");
			}
			node.appendChild(this._chartNode);

            var p = document.createElement('div');
            p.className = 'data';

            var contents = this._stringify(this._data);
            p.innerHTML = '总钱数: ' + this._total_money + ', 最大值: ' + this._max + ', 最小值: ' + this._min + ' <br />' + contents;

            this._chartNode.appendChild(p);

            this._chartNode = null;
		},

        _stringify: function (data) {
            return data.join(', ');
        },

		_init: function (total_money, data, max, min, index) {
			this._id = index;
			this._chartNode = document.createElement('div');
			this._chartNode.className = 'chart chart_' + this._id++;
			this._data = data;
			this._max = max;
			this._min = min;
            this._total_money = total_money;
		},

		_makeChart: function () {
			var node = this._chartNode;
			d3.select(node)
				.datum(this._data)
                .call(lineChart())
				// .call(histogramChart()
				// 	.width(600)
				// 	.height(250)
				// 	.title(this._id)
				// 	.lowerBand(this._min)
				// 	.upperBand(this._max)
				// 	.bins(10)
				// 	.xAxisLabel('# of money')
				// 	.yAxisLabel('# of frequency'));
		}
	};

	var app = {
		fetch_json: function (url) {

			return phen.defer(function (res, rej) {
				d3.json(url, function (error, json) {
					if (error) {
						return rej(new Error(error));
					}

					return res(json);
				});
			});
		},

		start: function () {
			var self = this;
			this.fetch_json('./' + config.json_uri)
				.then(function (data) {
					self.make_charts(data);
				}, function (error) {
					console.error(error);
				})
		},

		make_charts: function (data) {
			data.map(function (d, index) {
				var max = d.max;
				var min = d.min;
				var darr = d.data;

				chart.create(d.total_money, darr, max, min, index);
				chart.append(parentNode);
			});
		}
	}

	app.start();
}).call(this);

function histogramChart(){
    var margin = {
        top: 64,
        right: 32,
        bottom: 72,
        left: 32,
        labels: 38
    };
    //defaults
    var height = 200;
    var width = 500;
    var lowerBand = 0;
    var upperBand = 100;
    var bins = 5;
    var chartTitle = ["test"];
    var yAxisLabel = "y axis label";
    var xAxisLabel = "x axis label";
    var xformat = function(d){return d};
    var formatCount = d3.format(",.0f");
    
    function chart(selection) {
        var maxBarHeight = height - (margin.top + margin.bottom);
        var chartWidth = width - margin.right - margin.left;
        
        selection.selectAll('svg').remove();//remove old charts
        
        selection.each(function(values) {
            
            var x = d3.scale.linear()
                .domain([lowerBand, upperBand])
                .range([margin.labels, chartWidth]);
            
            // Generate a histogram using XX bins.
            var data = d3.layout.histogram()
                .bins(x.ticks(bins))(values);
            
            //fill the chart width, with 1px spacing between
            var numBins = data.length;
            var barWidth = parseInt((chartWidth-margin.labels)/numBins) - 6;           
                
            var y = d3.scale.linear()
                .domain([0, d3.max(data, function(d) { return d.y; })])
                .range([maxBarHeight, 0]);
            
            var xAxis = d3.svg.axis()
                .scale(x)
                .orient("bottom")
                .tickFormat(xformat);
        
            var svgContainer = d3.select(this).append("svg")
                .attr("class", "chart mini-column-chart")
                .attr("width", width)
                .attr("height", height)
               .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

            var bar = svgContainer.selectAll(".bar")
                .data(data)
              .enter().append("g")
                .attr("class", "bar")
                .attr("transform", function(d) { return "translate(" + x(d.x) + "," + y(d.y) + ")"; });
            
            var xAxisG = svgContainer.append("g")
                .attr("class", "x axis")
                .attr("transform", "translate( 0," + (height - margin.top - margin.bottom) + ")")
                .call(xAxis)
                
            var header = svgContainer.append("text")
                .attr("class", "chart-title")
                .attr("x", width/2)
                .attr("text-anchor", "middle")
                .attr("dy", -32)
                .text(chartTitle);
            
            bar.append("rect")
                .attr("x", 1)
                .attr("width", barWidth)
                .attr("height", function(d) { return maxBarHeight - y(d.y); });

            bar.append("text")
                .attr("class", "axis-label")
                .attr("dy", "-.75em")
                .attr("y", 6)
                .attr("x", barWidth / 2)
                .attr("text-anchor", "middle")
                .text(function(d) { return formatCount(d.y); });

            xAxisG.append("text")
                .attr("class", "axis-label")
                .attr("x", margin.left)
                .attr("dy", 56)
                .text(xAxisLabel);

            svgContainer.append("g")
                .attr("class", "y axis")
                .append("text")
                .attr("class", "axis-label")
                .attr("transform", "rotate(-90)")
                .attr("y", 8)
                .attr("x", -(height-margin.top-margin.bottom))
                .style("text-anchor", "start")
                .text(yAxisLabel);
        
        });
    }


    chart.title = function(_) {
        if (!arguments.length) return chartTitle;
        chartTitle = _;
        return chart;
    };


    chart.lowerBand = function(_) {
        if (!arguments.length) return lowerBand;
        lowerBand = _;
        return chart;
    };

    chart.upperBand = function(_) {
        if (!arguments.length) return upperBand;
        upperBand = _;
        return chart;
    };

    chart.width = function(_) {
        if (!arguments.length) return width;
        width = _;
        return chart;
    };

    chart.height = function(_) {
        if (!arguments.length) return height;
        height = _;
        return chart;
    };

    chart.bins = function(_) {
        if (!arguments.length) return bins;
        bins = _;
        return chart;
    };
    
    chart.xformat = function(_) {
        if (!arguments.length) return xformat;
        xformat = _;
        return chart;
    };
    
    chart.yAxisLabel = function(_) {
        if (!arguments.length) return yAxisLabel;
        yAxisLabel = _;
        return chart;
    };

    chart.xAxisLabel = function(_) {
        if (!arguments.length) return xAxisLabel;
        xAxisLabel = _;
        return chart;
    };

    chart.focusLabel = function(_) {
        if (!arguments.length) return focusLabel;
        focusLabel = _;
        return chart;
    };

    chart.focusValue = function(_) {
        if (!arguments.length) return focusValue;
        focusValue = _;
        return chart;
    };

    return chart;
}


function lineChart() {
    var svg_width = 500,
    svg_height = 250,
    // data = [3, 4, 6, 3, 7, 8, 9, 7, 5, 3, 8],
    margin = {top:30, right: 20, bottom:30, left: 50},
    chart_width = svg_width - margin.left - margin.right,
    chart_height = svg_height - margin.top - margin.bottom


    function chart(selection) {
        selection.selectAll('svg').remove();

        var data = selection.data();
        var transfer_x = d3.scale.linear().range([0, chart_width]),
            transfer_y = d3.scale.linear().range([chart_height, 0])

        data = data[0];

        transfer_x.domain([0, data.length]);
        transfer_y.domain([d3.min(data), d3.max(data)]);

        selection.each(function (values) {
            var vis = d3.select(this)
            .append("svg:svg")
            .attr("width", svg_width)
            .attr("height", svg_height)

            var draw_line = d3.svg.line()
            .x(function(d,i) { return transfer_x(i); })
            .y(function(d) { return transfer_y(d); })
            .interpolate("cardinal")

            var g = vis.append("svg:g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

            g.append("svg:path")
            .attr("class", "area")
            .datum(values)
            .attr("d", draw_line);

            var x_axis = d3.svg.axis().scale(transfer_x).orient("bottom").ticks(5)
            var y_axis = d3.svg.axis().scale(transfer_y).orient("left").ticks(5)

            g.append("svg:g")
            .call(x_axis)
            .attr("class", "x axis")
            .attr("transform", "translate(0," + chart_height + ")");

            g.append("svg:g")
            .attr("class", "y axis")
            .call(y_axis)
            .append("text")
            .attr("y", 15)
            .style("text-anchor", "end")
            .attr("transform", "rotate(-90)")
            .text("钱数");
            })
    }

    return chart;
}
