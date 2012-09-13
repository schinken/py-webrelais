
var  util = require('util')
    ,events = require('events');


var  RESET  = 'DELETE'
    ,GET    = 'GET'
    ,SET    = 'POST';

var Client = function( url ) {
    
    events.EventEmitter.call(this);

    var client = this;
    
    this.url = url;
    this.username = '';
    this.password = '';

    if( url.indexOf('https://') !== -1 ) {
        this.port = 443;    
    } else {
        this.port = 80;    
    }

};

util.inherits(Client, events.EventEmitter);

Client.prototype.authenticate = function( username, password ) {
    this.username = username;
    this.password = password;
};

Client.prototype.send_command = function( path, type, callback ) {
    
};

Client.prototype.set_port = function( port, value, callback ) {

    if( value == 0 ) {
        this.reset_port( port, callback );
        return;
    }

    this.once('set_port', callback);
    this.send_command( '/relais/' + port, SET, callback );
};


Client.prototype.set_ports = function( value, callback ) {

    if( value == 0 ) {
        this.reset_ports( callback );
        return;
    }  

    this.once('set_ports', callback);
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
