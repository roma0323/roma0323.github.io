let myGraph = document.getElementById('myGraph');
let trace1 = {};
trace1.type = "histogram";
trace1.x = set1;
let data = [];
data.push(trace1);
let layout = { margin: { t: 0 } };
Plotly.newPlot(myGraph, data, layout);