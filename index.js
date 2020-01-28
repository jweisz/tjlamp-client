const TJBot = require('tjbot-striplight');
const WebSocket = require('ws');
const config = require('./config');

var hardware = ['led-strip'];
var configuration = {
    shine: {
        led_strip: {
            num_leds: 60
        }
    }
};

var tj = new TJBot(hardware, configuration, {});
tj._setupLEDStrip();

const ws = new WebSocket(config.wsURL);

ws.on('open', function open() {
    console.log("connected to websocket server " + config.wsURL)
});

ws.on('message', function incoming(data) {
    console.log("received message: " + data);
    var msg = JSON.parse(data);
    if (msg.cmd == "shine") {
        var color = msg.color || "#FFFFFF";
        console.log("shining with color " + color);
        tj.shineStripWithRGBColor(color);

    } else if (msg.cmd == "rainbow") {
        console.log("rainbow strip");
        tj.rainbowStrip(0);

    } else if (msg.cmd == "pulse") {
        console.log("pulse not yet supported!");

    } else if (msg.cmd == "off") {
        console.log("turning off the strip");
        tj.shineStripWithRGBColor("#000000");
    }
});
