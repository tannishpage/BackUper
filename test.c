#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <arpa/inet.h>
#include <zlib.h>
#include <unistd.h>


int create_client_sock(char *ipaddress, int port)
/*
Creates a socket that connectes to a server which is ready for file transfer

Parameters:
	- ipaddress (*char): A string that contains the IP Address to connect to
	- port (int): An integer that represents the port number

Return:
	- The socket pointer
*/
{
	return 0;
}

int create_server_sock(char *ipaddress, int port)
/*

*/
{
	return 0;
}

int create_backup()
/*

*/
{
	return 0;
}

int zip_folder(char *path)
{
	//chdir(path);
	char cwd[1024];
	getcwd(cwd, sizeof(cwd));
	printf("Working Directory: %s\n\n", cwd);
	return 0;
}

int main()
{
	zip_folder("/Users/tannishpage/Documents/projects/BackUper/LApy");
	return 0;
}
