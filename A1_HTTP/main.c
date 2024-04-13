#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void send_http(char* host, char* msg, char* resp, size_t len);

int main(int argc, char* argv[]) {
  if (argc != 4) {
    printf("Invalid arguments - %s <host> <GET|POST> <path>\n", argv[0]);
    return -1;
  }

  char* host = argv[1];
  char* verb = argv[2];
  char* path = argv[3];
  char response[4096];
  char str[90]={0};

  if(strcmp(verb,"GET") == 0){
    // GET / HTTP/1.0\r\nHost: www.example.com\r\n\r\n
    sprintf(str, "%s %s HTTP/1.1\r\nHost: %s\r\n\r\n",verb,path,host);
    send_http(host , str, response, 4096);
    printf("%s\n", response);
  }
  else if(strcmp(verb,"POST") == 0){
    //POST / HTTP/1.1\r\nHost: www.example.com\r\nContent-Length: 10\r\n\r\nThis is it\r\n\r\n
    sprintf(str, "%s %s HTTP/1.1\r\nHost: %s\r\nContent-Length: 10\r\n\r\nThis is it\r\n\r\n",verb,path,host);
    send_http(host , str, response, 4096);
    printf("%s\n", response);
  }
  else{
    printf("%s","Invalid HTTP function");
  }
  return 0;
}


