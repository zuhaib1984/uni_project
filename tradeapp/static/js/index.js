function create_chart(canvasid, type, width, height, charttype){
    var ctx = document.getElementById(canvasid).getContext('2d');
    ctx.canvas.width = width;
    ctx.canvas.height = height;

    return new Chart(ctx, {
        type: charttype,
        options: {
        elements: {
                point: {
                    radius: 0
                }
            },
        animation: {
            duration: 0.1
            }
        },
        data: []
    });
}

function convert_data(data){
    d = {
        cs:[],
        bb: {ub:[], lb:[]},
        rsi: [],
        sma: []
    };

    //console.log(Object.keys(data['High']));
    const keys = Object.keys(data['High']);
    keys.forEach((key) => {
       d.cs.push({
            x: Number(key),
            o: data['Open'][key],
            h: data['High'][key],
            l: data['Low'][key],
            c: data['Close'][key]
        });

        d.bb.ub.push({
            x: Number(key),
            y: data['UB'][key],
        });

        d.bb.lb.push({
            x: Number(key),
            y: data['LB'][key],
        });

        d.rsi.push({
            x: Number(key),
            y: data['RSI'][key]
        })

        d.sma.push({
            x: Number(key),
            y: data['SMA'][key]
        })
    });

    return d;
}

var line_options =  {
    elements: {
        point:{
            radius: 10
        }
    }
}

     
var chartOne = create_chart('chartOne', 'candlestick', 1000, 250, 'candlestick');

// Chart Two
var chartTwo = create_chart('chartTwo', 'line', 1000, 250, 'line');

// Chart Three
var chartThree = create_chart('chartThree', 'line', 1000, 250, 'line');

function addLog(log){
    console.log('addinglog', log)
     let textele = document.getElementById("logs");
     textele.innerHTML = textele.innerHTML + '<br>' + log;
}

function update(data) {

    // Chart One
    chartOne.config.data.datasets = [{
        type: 'candlestick',
        label: 'Line',
        data: data.cs
    }, {
        type: 'line',
        options: line_options,
        label: 'BB - Upper Band',
        data: data.bb.ub
    }, {
        type: 'line',
        options: {
            elements: {
                point: {
                    radius: 0
                }
            }
        },
        label: 'BB - Lower Band',
        data: data.bb.lb
    }]

    // Chart Two
    chartTwo.config.data.datasets = [{
        type: 'candlestick',
        label: 'Line',
        data: []
    }, {
        type: 'line',
        options: line_options,
        label: 'RSI',
        borderColor: "#bae755",
        borderDash: [5, 5],
        backgroundColor: "#e755ba",
        pointBackgroundColor: "#55bae7",
        pointBorderColor: "#55bae7",
        pointHoverBackgroundColor: "#55bae7",
        pointHoverBorderColor: "#55bae7",
        data: data.rsi
    }]

    // Chart Three
    chartThree.config.data.datasets = [{
        type: 'candlestick',
        label: 'Line',
        data: []
    },{
        type: 'line',
        label: 'SMA',
        borderColor: "#bae755",
        borderDash: [5, 5],
        backgroundColor: "#e755ba",
        pointBackgroundColor: "#55bae7",
            pointBorderColor: "#55bae7",
            pointHoverBackgroundColor: "#55bae7",
            pointHoverBorderColor: "#55bae7",
        data: data.sma,
    }]

    chartOne.update();
    chartTwo.update();
    chartThree.update();
};

function createSocket(vars){
    console.log(vars);
    // Create WebSocket connection.
    let socket = new WebSocket("ws://"+ location.hostname +":8000/ws/getsignal");
    // Connection opened
    socket.addEventListener("open", (event) => {
      socket.send(JSON.stringify(vars));
    });

    // Listen for messages
    socket.addEventListener("message", (event) => {
      let response = JSON.parse(event.data)
      console.log("Message from server ", JSON.parse(event.data));
      data = convert_data(JSON.parse(response.data))
      console.log(data);
      signal = response.signal;
      let signalele = document.getElementById("signal");
      signalele.innerHTML = signal;

      console.log(signal);
      update(data);
    });
    return socket;
}
