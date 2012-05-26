module Relais where

import Network.HTTP
import Network.URI (parseURI)

url = "http://10.1.20.6:5000"

sendCommand method path = simpleHTTP req >>= getResponseBody >>= return . decode . lines
  where
    urlString = url ++ path
    req = case parseURI urlString of
            Nothing -> error ("sendCommand: Not a valid URL - " ++ urlString)
            Just u  -> mkRequest method u


setPort port val = if val
                     then sendCommand POST $ "/ports/" ++ port
                     else resetPort port

setPorts val = if val
                then sendCommand POST "/ports"
                else resetPorts

resetPort port = sendCommand DELETE $ "/ports/" ++ port

resetPorts = sendCommand DELETE "/ports"

getPort port = sendCommand GET $ "/ports/" ++ port

getPorts = sendCommand GET "/ports"


decode :: [String] -> Either String [Bool]
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
