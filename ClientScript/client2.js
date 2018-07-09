
var net = require ('net');

var client = new net.Socket();
client.connect(4242,'10.4.0.49',function(){
    console.log('Connected');
    
});

client.on('data',function(data){

    
    console.log('Received: '+data);
    //client.destroy();

    var spawn = require("child_process").spawn;
    var pythonProcess = spawn('python',[data]);
});

client.on('close',function(){
    console.log('Connection closed');
});
