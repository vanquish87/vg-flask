window.onload = function () {
    var chart = new CanvasJS.Chart("chartContainer",
    {

                        animationEnabled: true,
                         zoomEnabled: true, 
       legend:{
          verticalAlign: "center",
          horizontalAlign: "right",
          fontSize: 33,
          fontFamily: "Roboto",
          fontColor: "Sienna"
        },



      axisX:{

        gridColor: "Silver",
        tickColor: "silver",
        valueFormatString: "MMMY",
        titleFontFamily: "Roboto",
        labelFontFamily: "Roboto"
      },                        
                        toolTip:{
                          shared:true
                        },
      theme: "theme2",
      axisY: {
        gridColor: "Silver",
        gridThickness: 0 , 
        tickColor: "silver",
        titleFontFamily: "Roboto",
        labelFontFamily: "Roboto",
        title: "Returns %"
      },

      
      data: [
      {        
        type: "line",
        showInLegend: true,
        lineThickness: 2,
        name: "VGEX",
        markerType: "square",
        color: "#4FBEFF",
        dataPoints: [
        { x: new Date(2014,1,28), y: 0 },
        { x: new Date(2014,2,31), y: 17.2 },
        { x: new Date(2014,3,30), y: 9.8 },
        { x: new Date(2014,4,30), y: 38.3 },
        { x: new Date(2014,5,30), y: 46.4 },
        { x: new Date(2014,6,31), y: 41.1 },
        { x: new Date(2014,7,28), y: 36.3 },
        { x: new Date(2014,8,30), y: 69.1 },
        { x: new Date(2014,9,31), y: 57.5 },
        { x: new Date(2014,10,28), y: 62.6 },
        { x: new Date(2014,11,31), y: 52 },
        { x: new Date(2015,0,30), y: 56.1 },
        { x: new Date(2015,1,28), y: 60.4 },
        { x: new Date(2015,2,31), y: 52.3 },
        { x: new Date(2015,3,30), y: 49.6 },
        { x: new Date(2015,4,29), y: 48.2 },
        { x: new Date(2015,5,30), y: 56.4 },
        { x: new Date(2015,6,31), y: 80.9 },
        { x: new Date(2015,7,31), y: 58.1 },
        { x: new Date(2015,8,24), y: 59.4 },
        { x: new Date(2015,9,30), y: 79   },
        { x: new Date(2015,10,30), y: 94.6 },
        { x: new Date(2015,11,31), y: 98.1 },
        { x: new Date(2016,0,29), y: 89 },
        { x: new Date(2016,1,29), y: 63 },
        { x: new Date(2016,2,31), y: 81 },
        { x: new Date(2016,3,29), y: 85 },
        { x: new Date(2016,4,31), y: 90 },
        { x: new Date(2016,5,30), y: 114 },
        { x: new Date(2016,6,30), y: 108 }, 
        { x: new Date(2016,7,31), y: 121 },
        { x: new Date(2016,8,30), y: 135 },
        { x: new Date(2016,9,31), y: 149 },
        { x: new Date(2016,10,30), y: 118 },
        { x: new Date(2016,11,31), y: 125 },
        { x: new Date(2017,0,31), y: 134 },
        { x: new Date(2017,1,28), y: 132 },
        { x: new Date(2017,2,31), y: 148 },
        { x: new Date(2017,3,30), y: 151 },
        { x: new Date(2017,4,31), y: 140 },
        { x: new Date(2017,5,30), y: 141 },
        { x: new Date(2017,6,31), y: 142 },
        { x: new Date(2017,7,31), y: 140 },
        { x: new Date(2017,8,30), y: 141 },
        { x: new Date(2017,9,30), y: 155 },
        { x: new Date(2017,10,30), y: 160 },
        { x: new Date(2017,11,30), y: 187 , indexLabel:"+187%" },
        ]
      },
      {        
        type: "line",
        showInLegend: true,
        name: "Nifty",
        color: "#FBBC05",
        lineThickness: 2,

        dataPoints: [
        { x: new Date(2014,1,28), y: 0 },
        { x: new Date(2014,2,31), y: 2.6 },
        { x: new Date(2014,3,30), y: 0.5 },
        { x: new Date(2014,4,30), y: 5.1 },
        { x: new Date(2014,5,30), y: 8 },
        { x: new Date(2014,6,31), y: 7.4 },
        { x: new Date(2014,7,28), y: 9.4 },
        { x: new Date(2014,8,30), y: 7.7 },
        { x: new Date(2014,9,31), y: 11.6 },
        { x: new Date(2014,10,28), y: 13.4 },
        { x: new Date(2014,11,31), y: 7.5 },
        { x: new Date(2015,0,30), y: 14.4 },
        { x: new Date(2015,1,28), y: 14.2 },
        { x: new Date(2015,2,31), y: 7.7 },
        { x: new Date(2015,3,30), y: 3.1 },
        { x: new Date(2015,4,29), y: 5.9 },
        { x: new Date(2015,5,30), y: 5.1 },
        { x: new Date(2015,6,31), y: 6.6 },
        { x: new Date(2015,7,31), y: -0.7 },
        { x: new Date(2015,8,24), y: -1.8 },
        { x: new Date(2015,9,30), y: 0.5  },
        { x: new Date(2015,10,30), y: -1  },
        { x: new Date(2015,11,31), y: -0.9 },
        { x: new Date(2016,0,29), y: -6 },
        { x: new Date(2016,1,29), y: -12.6 },
        { x: new Date(2016,2,31), y: -3 },
        { x: new Date(2016,3,29), y: -1.1 },
        { x: new Date(2016,4,31), y: 2.9  },
        { x: new Date(2016,5,30), y: 3.9 },
        { x: new Date(2016,6,30), y: 8.5 },
        { x: new Date(2016,7,31), y: 10.6 },
        { x: new Date(2016,8,30), y: 8.3 },
        { x: new Date(2016,9,31), y: 8.5 },
        { x: new Date(2016,10,30), y: 1.7 },
        { x: new Date(2016,11,31), y: 3.9 },
        { x: new Date(2017,0,31), y: 9.7 },
        { x: new Date(2017,1,28), y: 12.4 },
        { x: new Date(2017,2,31), y: 16.7 },
        { x: new Date(2017,3,30), y: 17.2 },
        { x: new Date(2017,4,31), y: 17.1},
        { x: new Date(2017,5,30), y: 21.1},
        { x: new Date(2017,6,31), y: 26 },
        { x: new Date(2017,7,31), y: 26 },
        { x: new Date(2017,8,30), y: 23.4 },
        { x: new Date(2017,9,30), y: 30.6 },
        { x: new Date(2017,10,30), y: 27.6 },
        { x: new Date(2017,11,30), y: 32.8 , indexLabel:"+33%" },
        
        ]
      }

      
      ],
          legend:{
            cursor:"pointer",
            itemclick:function(e){
              if (typeof(e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
                e.dataSeries.visible = false;
              }
              else{
                e.dataSeries.visible = true;
              }
              chart.render();
            }
          }
    });

    chart.render();
    }