// Runs when user opens population_level.html.

var svgWidth = 960;
var svgHeight = 500;

var margin = {
  top: 20,
  right: 40,
  bottom: 60,
  left: 100
};

var width = svgWidth - margin.left - margin.right;
var height = svgHeight - margin.top - margin.bottom;

// Create an SVG wrapper, append an SVG group that will hold our chart, and shift the latter by left and top margins.
var svg = d3.select(".chart")
  .append("svg")
  .attr("width", svgWidth)
  .attr("height", svgHeight);

var chartGroup = svg.append("g")
  .attr("transform", `translate(${margin.left}, ${margin.top})`);

var stats_url = "/api/v1.0/summary";
var pop_url   = "/static/data/world-population-by-world-regions-post-1820.csv";
// Import Data
d3.csv(pop_url).then( function(popData) {
  d3.json(stats_url).then( function(statsData) {

    console.log(popData.length);
    console.log(statsData.length);

    // Step 1: Parse Data/Cast as numbers
    // ==============================
    popData.forEach(function(data) {
      data.Population = +data.Population;
    });

    // Step 2: Create scale functions
    // ==============================
    var xLinearScale = d3.scaleLinear()
      .domain([20, d3.max(popData, d => d.Population)])
      .range([0, width]);

    var yLinearScale = d3.scaleLinear()
      .domain([0, d3.max(statsData, d => d.total > 0 ? (d.satisfactory/d.total) * 100 : 0 )])
      .range([height, 0]);

    // Step 3: Create axis functions
    // ==============================
    var bottomAxis = d3.axisBottom(xLinearScale);
    var leftAxis = d3.axisLeft(yLinearScale);

    // Step 4: Append Axes to the chart
    // ==============================
    chartGroup.append("g")
      .attr("transform", `translate(0, ${height})`)
      .call(bottomAxis);

    chartGroup.append("g")
      .call(leftAxis);

    // Step 5: Create Circles
    // ==============================

    xvalues = popData.map( popRecord  => popRecord.Population);
    yvalues = statsData.map( statsRec => statsRec.total > 0 ? Math.round(statsRec.satisfactory/statsRec.total) * 100 : 0  );

    var circlesGroup = chartGroup.selectAll("circle")
    .data(xvalues)
    .enter()
    .append("circle")
    .attr("cx", d => xLinearScale(xvalues))
    .attr("cy", d => yLinearScale(yvalues))
    .attr("r", "15")
    .attr("fill", "pink")
    .attr("opacity", ".5");

    // Step 6: Initialize tool tip
    // ==============================
    var toolTip = d3.tip()
      .attr("class", "tooltip")
      .offset([80, -60])
      .html(function(d) {
        return (`${d.Entity}<br>Population: ${d.Population}`);
      });

    // Step 7: Create tooltip in the chart
    // ==============================
    //chartGroup.call(toolTip);

    // Step 8: Create event listeners to display and hide the tooltip
    // ==============================
    circlesGroup.on("click", function(data) {
      toolTip.show(data, this);
    })
      // onmouseout event
      .on("mouseout", function(data, index) {
        toolTip.hide(data);
      });

    // Create axes labels
    chartGroup.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0 - margin.left + 40)
      .attr("x", 0 - (height / 2))
      .attr("dy", "1em")
      .attr("class", "axisText")
      .text("Percentage Satisfactory");

    chartGroup.append("text")
      .attr("transform", `translate(${width / 2}, ${height + margin.top + 30})`)
      .attr("class", "axisText")
      .text("Population");
  }).catch(function(error) {
    console.log(error);
  });
});
