-- Usage: sendCommand "http://localhost:5000" (Req (Just '5') (Set True))
-- Req Nothing Get to get the state of all ports
-- Will return a Right with a list of Bools inside on success or a Left errormessage on failure

module Relais where


import Network.HTTP
import Network.URI (parseURI)


data Action = Set Bool | Get deriving (Show,Eq)
data Req = Req { port :: Maybe Char, action :: Action } deriving (Show, Eq)


sendCommand :: String -> Req -> IO (Either String [Bool])
sendCommand url (Req p a) = simpleHTTP req >>= getResponseBody >>= return . decode
  where
    urlString = url ++ "/ports" ++ port ++ "?format=raw"
    port = maybe "" (('/':) . (:[])) p
    method = case a of
              Get       -> GET
              Set True  -> POST
              Set False -> DELETE
    req = case parseURI urlString of
            Nothing -> error ("sendCommand: Invalid URL: " ++ urlString)
            Just u  -> mkRequest method u


decode xs = if all (\x -> x == '1' || x == '0') xs
              then Right $ map decode' xs
              else Left $ "decode: Invalid repsonse: " ++ xs
  where
    decode' '0' = False
    decode' '1' = True
