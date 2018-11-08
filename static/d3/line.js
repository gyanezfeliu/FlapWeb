(function($){
  $(document).ready(function(){
    // Carga de JSON (desde archivo o API)
    d3.json('/static/plot.JSON')
    .then(response => response)
    .then((data)=>{

      var parseTime = d3.timeParse("%H:%M:%S");

      data.forEach((d)=>{
        d.Time_Src = d.Time;
        d.Time = parseTime(d.Time);
      })

      // Lógica D3 para graficar
      let container = $("#graph")
      let width = container.width()
      let height = container.height()
      let svg = d3.select("#graph").append("svg")
      .attr("width", "100%")
      .attr("height", "100%")
      let grp = svg.append("g")
      .attr("transform", "translate(0,10)")

      var n = data.length;

      var colorScale = d3.scaleOrdinal(d3.schemePaired)

      var xScale = d3.scaleTime()
      .domain(
        d3.extent(data, function(d) { return d.Time; })
      )
      .range([25, (width-25)]);

      var yScale = d3.scaleLinear()
      .domain(
        [0, d3.max(data, function(d) {
          return Math.max(d.C3, d.C4, d.C5, d.C6, d.C7, d.D3, d.D4, d.D5, d.D6, d.D7);
        })]
      )
      .range([(height-30), 0]);

      var line_c3 = d3.line()
      .x(function(d) { return xScale(d.Time); })
      .y(function(d) { return yScale(d.C3); })
      .curve(d3.curveMonotoneX)

      var line_c4 = d3.line()
      .x(function(d) { return xScale(d.Time); })
      .y(function(d) { return yScale(d.C4); })
      .curve(d3.curveMonotoneX)

      var line_c5 = d3.line()
      .x(function(d) { return xScale(d.Time); })
      .y(function(d) { return yScale(d.C5); })
      .curve(d3.curveMonotoneX)

      var line_c6 = d3.line()
      .x(function(d) { return xScale(d.Time); })
      .y(function(d) { return yScale(d.C6); })
      .curve(d3.curveMonotoneX)

      var line_c7 = d3.line()
      .x(function(d) { return xScale(d.Time); })
      .y(function(d) { return yScale(d.C7); })
      .curve(d3.curveMonotoneX)

      var line_d3 = d3.line()
      .x(function(d) { return xScale(d.Time); })
      .y(function(d) { return yScale(d.D3); })
      .curve(d3.curveMonotoneX)

      var line_d4 = d3.line()
      .x(function(d) { return xScale(d.Time); })
      .y(function(d) { return yScale(d.D4); })
      .curve(d3.curveMonotoneX)

      var line_d5 = d3.line()
      .x(function(d) { return xScale(d.Time); })
      .y(function(d) { return yScale(d.D5); })
      .curve(d3.curveMonotoneX)

      var line_d6 = d3.line()
      .x(function(d) { return xScale(d.Time); })
      .y(function(d) { return yScale(d.D6); })
      .curve(d3.curveMonotoneX)

      var line_d7 = d3.line()
      .x(function(d) { return xScale(d.Time); })
      .y(function(d) { return yScale(d.D7); })
      .curve(d3.curveMonotoneX)

      grp.append("path")
      .data([data])
      .attr("class", "line")
      .attr("d", line_c3)
      .style("stroke", (d,i)=>colorScale(0))

      grp.append("path")
      .data([data])
      .attr("class", "line")
      .attr("d", line_c4)
      .style("stroke", (d,i)=>colorScale(1))

      grp.append("path")
      .data([data])
      .attr("class", "line")
      .attr("d", line_c5)
      .style("stroke", (d,i)=>colorScale(2))

      grp.append("path")
      .data([data])
      .attr("class", "line")
      .attr("d", line_c6)
      .style("stroke", (d,i)=>colorScale(3))

      grp.append("path")
      .data([data])
      .attr("class", "line")
      .attr("d", line_c7)
      .style("stroke", (d,i)=>colorScale(4))

      grp.append("path")
      .data([data])
      .attr("class", "line")
      .attr("d", line_d3)
      .style("stroke", (d,i)=>colorScale(5))

      grp.append("path")
      .data([data])
      .attr("class", "line")
      .attr("d", line_d4)
      .style("stroke", (d,i)=>colorScale(6))

      grp.append("path")
      .data([data])
      .attr("class", "line")
      .attr("d", line_d5)
      .style("stroke", (d,i)=>colorScale(7))

      grp.append("path")
      .data([data])
      .attr("class", "line")
      .attr("d", line_d6)
      .style("stroke", (d,i)=>colorScale(8))

      grp.append("path")
      .data([data])
      .attr("class", "line")
      .attr("d", line_d7)
      .style("stroke", (d,i)=>colorScale(9))

      // Desplegar Ejes
      grp.append("g")
      .attr("transform", "translate(0," + (height - 30) + ")")
      .call(
        d3.axisBottom(xScale)
        .tickFormat(function(d,i){
          return `${d.getHours()}:${d.getMinutes()}`;
        })
      )

      // Eje Y
      grp.append("g")
      .attr("transform", "translate(25,0)")
      .call(d3.axisLeft(yScale))


    })
    .catch((e)=>{
      console.log("Error cargando JSON", e);
    })
  });

})(jQuery);
