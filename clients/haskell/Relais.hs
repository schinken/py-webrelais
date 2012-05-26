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


-- Haskell's JSON library is overkill for this, so I implemented my own decode function
decode [] = []
decode (x:xs)
    | x == '0' = Right False : decode xs
    | x == '1' = Right True : decode xs
    | otherwise = [Left $ "decode: Invalid response: " ++ [x]]
