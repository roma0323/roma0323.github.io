let myGraph = document.getElementById('myGraph');
let myGraph2 = document.getElementById('myGraph2');
let myGraph3 = document.getElementById('myGraph3');
let myGraph4 = document.getElementById('myGraph4');
let trace1 = {};
let trace2 = {};
let trace3 = {};
let trace4 = {};
trace1.type = "histogram";
trace2.type = "histogram";
trace3.type = "histogram";
trace4.type = "histogram";
trace1.x = Netflix_list;
trace1.marker = { color: '#E50914' }; // You can also use 'line' or other attributes
trace2.x = Hulu_list;
trace2.marker = { color: '#1CE783' }; // You can also use 'line' or other attributes
trace3.x = prime_video_list;
trace3.marker = { color: '#00A8E1' }; // You can also use 'line' or other attributes
trace4.x = Disney_list;
trace4.marker = { color: '#0c2276' }; // You can also use 'line' or other attributes
let data = [];
let data2 = [];
let data3 = [];
let data4 = [];
data.push(trace1);
data2.push(trace2);
data3.push(trace3);
data4.push(trace4);
const layout = {
    width: '80%', // Set the width to 80%
    // Additional layout configurations...
};Plotly.newPlot(myGraph, data, layout);
Plotly.newPlot(myGraph2, data2, layout);
Plotly.newPlot(myGraph3, data3, layout);
Plotly.newPlot(myGraph4, data4, layout);

