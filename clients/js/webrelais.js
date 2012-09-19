
var  util = require('util')
    ,events = require('events')
    ,https = require('https')
    ,http = require('http');


var  RESET  = 'DELETE'
    ,GET    = 'GET'
    ,SET    = 'POST';

var Client = function( url, port ) {
    
    events.EventEmitter.call(this);

    var client = this;
    
    this.http_client = http;
    this.url = url;
    this.username = false;
    this.password = false;

    if( port ) {
        this.port = port;    
    } else {
        if( url.indexOf('https://') !== -1 ) {
            this.port = 443;
            this.http_client = https;
        } else {
            this.port = 80;    
        }
    }

};

util.inherits(Client, events.EventEmitter);

Client.prototype.authenticate = function( username, password ) {
    this.username = username;
    this.password = password;
};

Client.prototype.needs_auth = function() {
    return (this.username && this.password);
};

Client.prototype.send_command = function( path, type, callback ) {

    this.once('command_sent', callback);

    var options = {
        host: this.url,
        port: this.port,
        path: path,
        method: type,
    };

    if( this.needs_auth() ) {
        options['auth'] = this.username + ":" + this.password;
    }

    console.log(options);

    // Set up the request
    var post_req = this.http_client.request(options, function(res) {
        res.setEncoding('utf8');
        res.on('end', function () {
            console.log("Emit event");
            this.emit('command_sent');
        });
    });

    // post the data
    post_req.end();
};

Client.prototype.set_port = function( port, value, callback ) {

    if( value == 0 ) {
        this.reset_port( port, callback );
        return;
    }

    this.send_command( '/relais/' + port, SET, callback );
};


Client.prototype.set_ports = function( value, callback ) {

    if( value == 0 ) {
        this.reset_ports( callback );
        return;
    }  

    this.send_command( '/relais', SET, callback );
};

Client.prototype.reset_port = function( port, callback ) {
    this.send_command( '/relais/' + port, RESET, callback );
};

Client.prototype.reset_ports = function( port, callback ) {
    this.send_command( '/relais', RESET, callback );
};

Client.prototype.get_port = function( port, callback ) {
    this.send_command( '/relais/' + port, GET, callback ); 
};

Client.prototype.get_ports = function( callback ) {
    this.send_command( '/relais', GET, callback );
};


module.exports = {
    Client: Client
};
