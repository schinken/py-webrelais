var  util   = require('util')
    ,https  = require('https')
    ,http   = require('http')
    ,url    = require('url');


var  RESET  = 'DELETE'
    ,GET    = 'GET'
    ,SET    = 'POST';

var Client = function( baseurl ) {
    this.baseurl  = baseurl;
    this.username = false;
    this.password = false;
};


Client.prototype.authenticate = function( username, password ) {
    this.username = username;
    this.password = password;
};

Client.prototype.needs_auth = function() {
    return (this.username && this.password);
};

Client.prototype.send_command = function( path, type, callback ) {

    var options     = url.parse(this.baseurl + path);
    options.method  = type;
    options.headers = {'Content-length': 0};

    if( this.needs_auth() ) {
        options['auth'] = this.username + ":" + this.password;
    }

    var http_s = options.protocol=='https:' ? https : http;

    // Set up the request
    var client = this;
    var req = http_s.request(options, function(res) {
        res.setEncoding('utf8');
        var resString = '';
        res.on('data', function( data ){
            resString += data;
        });
        res.on('end', function () {
            var reply;
            var error;
            try {
                reply = JSON.parse(resString);
                error = false;
            }
            catch( e ) {
                error = true;
                console.log( 'json parsing error: ' + e.message );
            }
            if(typeof(callback)=='function')
                callback();
        });
    });

    req.end();
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
