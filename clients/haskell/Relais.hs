module Relais where

import Network.HTTP
import Network.URI (parseURI)

sendCommand method url path = simpleHTTP req >>= getResponseBody >>= return . decode . lines
  where
    urlString = url ++ path
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
decode x@(x1:x2:xs)
    | x1 == "{" = sequence $ if last x2 == '['
                              then map (decode' . getBoolString) (init $ init xs)
                              else [decode' $ drop 2 $ dropWhile (/= ':') x2]
    | otherwise = Left $ "decode: Invalid response:\n" ++ (unlines x)
  where
    getBoolString   = takeWhile (/= ',') . dropWhile (==' ')
    decode' "false" = Right False
    decode' "true"  = Right True
    decode' wrong   = Left $ "decode': Not a boolean: " ++ wrong
