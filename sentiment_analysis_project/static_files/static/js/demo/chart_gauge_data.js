const gaugeChart = document.getElementById('gaugeChart');
const chart_guage=window.sentimentData;
// var data = [
//   {
//     type: "indicator",
//     mode: "gauge+number",
//     value: chart_guage.sentiment_index,
//     title: { text: "Sentiment Index" },
//     gauge: { axis: { range: [-1, 1] } }
//   }
// ], layout = { width: 400, height: 300 };

// Plotly.newPlot('gaugeChart', data, layout);
// var options = {
//   type: 'gauge',
//   data: {
//     labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
//     datasets: [{
//       label: 'sentiment_index',
//       data: [12, 19, 3, 5, 2, 3],
//       backgroundColor: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"]
//     }]
//   },
//   options: {
//     rotation: 270, // start angle in degrees
//     circumference: 180, // sweep angle in degrees
//   }
// }
// new Chart(gaugeChart, options);

var data = [
	{
		domain: { x: [0, 1], y: [0, 1] },
		value: chart_guage.sentiment_index,
		title: { text: "Sentiment Index" },
		type: "indicator",
		mode: "gauge+number"
	}
];

var layout = { width: 400, height: 300, margin: { t: 0, b: 0 } };
Plotly.newPlot(gaugeChart, data, layout);