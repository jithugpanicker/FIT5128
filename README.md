# FIT5128 - README File

1. The FGACP_Security_Validation.hlpsl file contains the security validation code of the protocol.

2. Port_Listener.py and Port_Transmitter.py are the socket programs written for listening and transmitting the authentication requests and response. The Port_Listener.py programs can send the attribute-embedded certificates signed by the trusted authority. The Port_Transmitter.py verifies the signed certificate and further verifies the attributes. 
