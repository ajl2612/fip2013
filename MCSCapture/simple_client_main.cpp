#include "ClientSocket.h"
#include "SocketException.h"
#include <iostream>
#include <string>
#include <sstream>



int main ( int argc, int argv[] )
{
for(int i = 0; i<10; i++){

  try
    {
	ClientSocket client_socket ( "129.21.58.247", 8090 );
	std::string reply;

	std::ostringstream stringStream;
	stringStream <<  "hello... " << i ;
	reply = stringStream.str();
	

      try
	{
	client_socket << reply;
	 //client_socket >> reply;
	}
      catch ( SocketException& ) {}

      std::cout << "We received this response from the server:\n\"" << reply << "\"\n";;

    }
  catch ( SocketException& e )
    {
      std::cout << "Exception was caught:" << e.description() << "\n";
    }
}
  return 0;
}
