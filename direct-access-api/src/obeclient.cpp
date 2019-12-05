#include "obeclient.hpp"
#include "common.hpp"

int sockfd;
const char *obe_server_ip = "127.0.0.1";  //"192.168.3.40"; //
int obe_port = 6786;
int connection_status;

pthread_mutex_t deque_mutex;
deque<string> obe_deque;


e_result obe_client_init() {
  pthread_t obe_thread;
  pthread_t obe_queue_thread;


  struct sockaddr_in serv_addr;

  // create socket
  sockfd = socket(AF_INET, SOCK_STREAM, 0);
  if (sockfd < 0) {
    printf("Failed to create socket\n");
    return FAILURE;
  }

  memset(&serv_addr, '0', sizeof(serv_addr));
  inet_pton(AF_INET, obe_server_ip, &serv_addr.sin_addr);
  serv_addr.sin_family = AF_INET;
  serv_addr.sin_port = htons(obe_port);

  // connect
  connection_status =
      connect(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr));
  if (connection_status < 0) {
    printf("Failed to connect to server %s\n", obe_server_ip);
    return FAILURE;
  }
  printf("Connected to server\n");



  if (pthread_create(&obe_queue_thread, NULL, parse_obe_queue, (void *)1) != 0) {
    perror("obe_queue_thread thread creation failure !");
    return FAILURE;
  }else{
      printf("obe_queue_thread created\n");
  }


  if (pthread_create(&obe_thread, NULL, obe_listen, (void *)1) != 0) {
    perror("obe_thread thread creation failure !");
    return FAILURE;
  }else{
    printf("obe_thread created\n");

  }



  return SUCCESS;
}

e_result obe_client_connect() {
  struct sockaddr_in serv_addr;

  // create socket
  sockfd = socket(AF_INET, SOCK_STREAM, 0);
  if (sockfd < 0) {
    printf("Failed to create socket\n");
    return FAILURE;
  }

  memset(&serv_addr, '0', sizeof(serv_addr));
  inet_pton(AF_INET, obe_server_ip, &serv_addr.sin_addr);
  serv_addr.sin_family = AF_INET;
  serv_addr.sin_port = htons(obe_port);

  // connect
  connection_status =
      connect(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr));
  if (connection_status < 0) {
    printf("Failed to connect to server\n");
    return FAILURE;
  }
  printf("Connected to server\n");

  return SUCCESS;
}

void *obe_listen(void *notused) {
  char buffer[BUFFER_SIZE] = {};
  char temp_buffer[BUFFER_SIZE] = {};

  int counter = 1;
  while (1) {
    memset(&buffer, '\0', sizeof(buffer));

    // check connection, try to reconnect if needed
    while (connection_status < 0) {
      sleep(10);
      printf("Trying to reconnect....");
      if (obe_client_connect() == SUCCESS) {
        break;
      }
    }

    // read
    int r = read(sockfd, buffer, BUFFER_SIZE);
    if (r < 0) {
      printf("Failed to read from daa_obe server\n");
    } else if (r == 0) {
      printf("Disconnected from daa_obe server \n");
      connection_status = -1;
    } else {
      //printf("daa_obe: %s\n", buffer);

      // handle msg
      pthread_mutex_lock(&deque_mutex);
      string bufferstr(buffer);
      obe_deque.push_back(bufferstr);
      pthread_mutex_unlock(&deque_mutex);

      memset(&buffer, '\0', sizeof(buffer));

      //printf("i %i\n",  counter++);
    }
  }
}

char *prepare_outgoing_msg(char *daa_msg, struct can_frame *frame) {
  //"{can_id|can_dlc|data[0]|data[1]}"  - can frame data
  char hex_str[50];

  strcat(daa_msg, "{");
  sprintf(hex_str, "%x", frame->can_id);
  strcat(daa_msg, hex_str);
  strcat(daa_msg, "|");
  sprintf(hex_str, "%x", frame->can_dlc);
  strcat(daa_msg, hex_str);
  strcat(daa_msg, "|");
  sprintf(hex_str, "%x", frame->data[0]);
  strcat(daa_msg, hex_str);
  strcat(daa_msg, "|");
  sprintf(hex_str, "%x", frame->data[1]);
  strcat(daa_msg, hex_str);
  strcat(daa_msg, "|");
  sprintf(hex_str, "%x", frame->data[2]);
  strcat(daa_msg, hex_str);
  strcat(daa_msg, "|");
  sprintf(hex_str, "%x", frame->data[3]);
  strcat(daa_msg, hex_str);
  strcat(daa_msg, "|");
  sprintf(hex_str, "%x", frame->data[4]);
  strcat(daa_msg, hex_str);
  strcat(daa_msg, "|");
  sprintf(hex_str, "%x", frame->data[5]);
  strcat(daa_msg, hex_str);
  strcat(daa_msg, "|");
  sprintf(hex_str, "%x", frame->data[6]);
  strcat(daa_msg, hex_str);
  strcat(daa_msg, "|");
  sprintf(hex_str, "%x", frame->data[7]);
  strcat(daa_msg, hex_str);

  strcat(daa_msg, "}");

  // printf("outgoing %s\n", daa_msg);

  return daa_msg;
}

void handle_incoming_msg(char *framestr) {

  const char *delimiter = "|";
  struct can_frame frame;

  char *tempstr = strdup(framestr);

  frame.can_id = strtol(strsep(&tempstr, delimiter), NULL, 16);
  frame.can_dlc = 8;
  frame.data[0] = strtol(strsep(&tempstr, delimiter), NULL, 16);
  frame.data[1] = strtol(strsep(&tempstr, delimiter), NULL, 16);
  frame.data[2] = strtol(strsep(&tempstr, delimiter), NULL, 16);
  frame.data[3] = strtol(strsep(&tempstr, delimiter), NULL, 16);
  frame.data[4] = strtol(strsep(&tempstr, delimiter), NULL, 16);
  frame.data[5] = strtol(strsep(&tempstr, delimiter), NULL, 16);
  frame.data[6] = strtol(strsep(&tempstr, delimiter), NULL, 16);
  frame.data[7] = strtol(strsep(&tempstr, delimiter), NULL, 16);


    //printf("handle inc: %i\n", counter++);
    // check which vcans have read permissions
    //  dbmanager db;
    //  vector<string> vcan_list =
    //      db.select_vcans_from_read_table(frame.can_id & 0x1FFFFFFF);
    //for (string vcan : vcan_list) {
    // write to vcan;
    // cout << "write to vcan: " << vcan << endl;
    // vcanlistener listener(vcan);
    // listener.vcan_socket_init();
    // listener.vcan_write_frame(&frame);

    vcanwriter::vcan_write_frame("vcanh0", &frame);
    usleep(1000);

  //}
}

void handle_incoming_msgs(string daa_msgs) {

  const char *delimiter = ",";
  char *framestr;
  char *tempstr = strdup(daa_msgs.c_str());

  while( (framestr = strsep(&tempstr,delimiter)) != NULL ){
    handle_incoming_msg(framestr);
  }
}
void *parse_obe_queue(void *notused){

    string buffer;

    while(1){

        if(obe_deque.empty() == 0){

            pthread_mutex_lock(&deque_mutex);
            buffer = obe_deque.front();
            obe_deque.pop_front();
            pthread_mutex_unlock(&deque_mutex);

            printf("b %i\n", buffer.size());
            parse_buffer(buffer);

        }
        usleep(100);
    }

}


void parse_buffer(string buffer) {

  size_t sindex = -1;
  size_t eindex = -1;


  // locate msg start-endpoints
  sindex = buffer.find_first_of("{");
  eindex = buffer.find_first_of("}");


  // check endpoints
  if (sindex >= 0 && eindex > 2) {

    string daa_msgs = buffer.substr(sindex+1, eindex-sindex-1);

    handle_incoming_msgs(daa_msgs);

    if (eindex + 1 != buffer.size())
      parse_buffer(buffer.substr(eindex+1));
    else {
      // printf("...\n");
      return;
    }
  } else {
    // printf("...\n");
    return;
  }
}

