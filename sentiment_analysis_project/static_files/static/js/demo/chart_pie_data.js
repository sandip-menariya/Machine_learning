// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';
const chart_pie=window.sentimentData;
// console.log("chart data string: ","{{chart_data_json|escapejs}}");
// console.log("chart data parsed: ",JSON.parse("{{chart_data_json|escapejs}}"));
// const chart_pie = JSON.parse('{{ chart_data_json|escapejs }}'); 
console.log("chart data: ",chart_pie);
new Chart(document.getElementById('sentiment_pie'), {
    type: "pie",
    data: {
        labels: ["Positive", "Neutral", "Negative"],
        datasets: [{
            data: [chart_pie.pos, chart_pie.neu, chart_pie.neg],
            backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc'],
            hoverBackgroundColor: ['#2e59d9', '#17a673', '#2c9faf'],
            hoverBorderColor: "rgba(234, 236, 244, 1)",
        }]
    },
options: {
    maintainAspectRatio: false,
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
    },
    legend: {
      display: false
    },
    cutoutPercentage: 80,
  },
});
  

    