<?php

class RelaisClient {

    const SET   = 'POST';
    const GET   = 'GET';
    const RESET = 'DELETE';

    const ON    = 1;
    const OFF   = 0;

    private $Host = '';

    /**
     * @param $Host
     * @param int $Port
     */

    public function __construct( $Host, $Port = 80 ) {
        $this->Host = sprintf("http://%s:%d", $Host, $Port );
    }

    /**
     * Sends command to REST-API
     *
     * @param string $Path
     * @param string $Type
     * @return mixed
     * @throws Exception
     */

    private function sendCommand( $Path, $Type ) {

        
        $ch = curl_init( $this->Host . $Path );

        curl_setopt( $ch, CURLOPT_RETURNTRANSFER,       true );
        curl_setopt( $ch, CURLOPT_USERAGENT,            'PHP RelaisClient v1');
        curl_setopt( $ch, CURLOPT_CUSTOMREQUEST,        $Type );

        $result = curl_exec( $ch );
        if( $result ) {

            $decode = @json_decode( $result, true );
            if( $decode === null ) {
                throw new Exception('Unable to parse result');    
            }

            return $decode;

        } else {

            throw new Exception('Unable to fullfill request');
        }

    }

    /**
     * Set Port to On or Off
     *
     * @param int $Port
     * @param int $Value
     * @return bool
     */

    public function setPort( $Port, $Value = 1 ) {

        if( $Value == 0 ) {
            return $this->resetPort( $Port );    
        }
        
        return $this->sendCommand( sprintf('/ports/%d', $Port ), RelaisClient::SET );
    }

    /**
     * Sets all Ports to On or Off
     *
     * @param int $Value
     * @return bool
     */

    public function setPorts( $Value = 1 ) {

        if( $Value == 0 ) {
            return $this->resetPorts();    
        }
        
        return $this->sendCommand( '/ports', RelaisClient::SET );
    }

    /**
     * Resets Port (set to Off)
     *
     * @param int $Port
     * @return bool
     */

    public function resetPort( $Port ) {
        return $this->sendCommand( sprintf('/ports/%d', $Port ), RelaisClient::RESET );
    }

    /**
     * Reset ALL THE PORTS
     *
     * @return bool
     */

    public function resetPorts() {
        return $this->sendCommand( '/ports', RelaisClient::RESET );
    }

    /**
     * Returns value of the Port
     *
     * @param $Port
     * @return bool
     */

    public function getPort( $Port ) {
        return $this->sendCommand( sprintf('/ports/%d', $Port ), RelaisClient::GET );
    }

    /**
     * Returns state of all ports
     *
     * @return bool
     */

    public function getPorts() {
        return $this->sendCommand( '/ports', RelaisClient::GET );
        
    }
    
    
}

