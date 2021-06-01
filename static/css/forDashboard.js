 window.onload= function (){
        //for totoal search number
        var data = JSON.parse('{{ data | tojson | safe}}');
        console.log(data)
        //for spam rate
        var spam_cnt = data["spam_cnt"]
        var benign_cnt = data["benign_cnt"]

        new Chart(document.getElementById('spamRate'), {
        type: 'bar',
        data: {
            labels: ['Spam', 'Benign'],
            datasets: [{
                label:'Count of Each Tweets',
                data: [spam_cnt, benign_cnt],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                ],
                borderWidth: 1
            }]
        },
        options: {
            legend: {
                display: false
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
        });

        //for search history
        var time_cnt = data["time_cnt"]
        time_line = []
        count_line = []
        Object.keys(time_cnt).forEach(function(key) {
            time_line.push(key)
            count_line.push(time_cnt[key])
        });
        new Chart(document.getElementById("searchHistory"), {
          type: 'line',
          data: {
            labels: time_line,
            datasets: [{
                data: count_line,
                label: "Count",
                borderColor: "#3e95cd",
                fill: false
              },
            ]
          },
          options: {
              legend: {
                display: false
            },
          }
        });

        //for pie chart
        new Chart(document.getElementById("pieChart"), {
          type: 'pie',
          data: {
            labels: ['Spam', 'Benign'],
            datasets: [{
              data: [spam_cnt, benign_cnt],
              backgroundColor: [ '#36A2EB','#FF6384']
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
              labels: {
                render: 'percentage',
                fontColor: ['green', 'white'],
                precision: 2
              }
            },
          }
      });
    }