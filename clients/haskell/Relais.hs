module Relais where

import Network.HTTP
import Network.URI (parseURI)

sendCommand method url path = simpleHTTP req >>= getResponseBody >>= return . sequence . decode
  where
    urlString = url ++ path ++ "?format=raw"
    req = case parseURI urlString of
            Nothing -> error ("sendCommand: Not a valid URL - " ++ urlString)
            Just u  -> mkRequest method u


setPort url port val = if val
                        then sendCommand POST url $ "/ports/" ++ port
                        else resetPort url port

setPorts url val = if val
                    then sendCommand POST url "/ports"
                    else resetPorts url

resetPort url port = sendCommand DELETE url $ "/ports/" ++ port

resetPorts url = sendCommand DELETE url "/ports"

getPort url port = sendCommand GET url $ "/ports/" ++ port

getPorts url = sendCommand GET url "/ports"


decode = map (decode')
  where
    decode' '0' = Right False
    decode' '1' = Right True
    decode'  x  = Left $ "decode: Invalid response: " ++ [x]
