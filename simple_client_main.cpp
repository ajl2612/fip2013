#include "ClientSocket.h"
#include "SocketException.h"
#include <iostream>
#include <string>

int main ( int argc, int argv[] )
{
  try
    {

      ClientSocket client_socket ( "129.21.58.247", 8090 );

      std::string reply;

      try
	{
	  client_socket << "Motha Flippin Banana Pancakes.";
	  //client_socket >> reply;
	}
      catch ( SocketException& ) {}

      std::cout << "We received this response from the server:\n\"" << reply << "\"\n";;

    }
  catch ( SocketException& e )
    {
      std::cout << "Exception was caught:" << e.description() << "\n";
    }

  return 0;
}
