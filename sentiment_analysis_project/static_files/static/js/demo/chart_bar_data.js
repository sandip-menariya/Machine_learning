const chart_bar=window.sentimentData;
new Chart(document.getElementById("BarChart"), {
  type: "bar",
  data: {
    labels: ["Positive", "Neutral", "Negative"],
    datasets: [{
      label: "Probability (%)",
      data: [
        chart_bar.pos_avg,
        chart_bar.neu_avg,
        chart_bar.neg_avg
      ],
      backgroundColor: ["#4e73df", "#1cc88a", "#36b9cc"],
      hoverBackgroundColor: ["#2e59d9", "#17a673", "#2c9faf"],
      borderColor: "#4e73df",
    }]
  }
});