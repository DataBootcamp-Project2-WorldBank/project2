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

// If <div> exists in the DOM, create an SVG wrapper, append an SVG group that will hold our chart, and shift the latter by left and top margins.
if (document.getElementById("cpi-chart")) {
console.log("cpi-chart in DOM");
var svg = d3.select("#cpi-chart")
  .append("svg")
  .attr("width", svgWidth)
  .attr("height", svgHeight);

var chartGroup = svg.append("g")
  .attr("transform", `translate(${margin.left}, ${margin.top})`);

var stats_url = "/api/v1.0/summary";

// Import Data
  d3.json(stats_url).then( function(statsData) {

    console.log(statsData.length);
   
    // Step 1: Filter 0-project countries and
    // Parse Data/Cast as numbers
    // ==============================
    statsData = statsData.filter(country=>country.total > 0);  
    statsData.forEach(function(data) {
      data.cpi = +data.cpi;
    });

    // Step 2: Create scale functions
    // ==============================
    var xLogScale = d3.scaleLinear()
      .domain([d3.min(statsData, d => d.cpi)*0.8, d3.max(statsData, d => d.cpi)*1.2])
      .range([0, width]);

    var yLinearScale = d3.scaleLinear()
      .domain([0, d3.max(statsData, d => d.total > 0 ? (d.satisfactory/d.total) * 100 : 0 )])
      .range([height, 0]);

    // Step 3: Create axis functions
    // ==============================
    var bottomAxis = d3.axisBottom(xLogScale);
    var leftAxis = d3.axisLeft(yLinearScale);

    // Step 4: Append Axes to the chart
    // ==============================
    chartGroup.append("g")
      .attr("transform", `translate(0, ${height})`)
      .call(bottomAxis);

    chartGroup.append("g")
      .call(leftAxis);

      console.log(statsData);

    // Step 5: Create Circles
    // ==============================
    var circlesGroup = chartGroup.selectAll("circle")
    .data(statsData)
    .enter()
    .append("circle")
    .attr("cx", d => xLogScale(d.cpi) )
    .attr("cy", d => yLinearScale( d.total > 0 ? (d.satisfactory/d.total) * 100 :0 ))
    .attr("r", "7")
    .attr("fill", "red")
    .attr("opacity", ".5");

    // Step 6: Initialize tool tip
    // ==============================
    var toolTip = d3.tip()
      .attr("class", "tooltip")
      .offset([80, -60])
      .html(function(d) {
        return (`${d.country_name}<br>Corruption Index: ${Math.round(d.cpi)}<br>% Satisfactory: ${d.total > 0 ? Math.round((d.satisfactory/d.total) * 100) : 0}`);
      });

    // Step 7: Create tooltip in the chart
    // ==============================
    chartGroup.call(toolTip);

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
      .text("Corruption Index");
  }).catch(function(error) {
    console.log(error);
  });

};
