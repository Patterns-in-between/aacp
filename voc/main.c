#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdarg.h>
#include <string.h>
#include <math.h>
#include <assert.h>
#include <math.h>
#include <limits.h>
#include <time.h>
#include <unistd.h>

#include <pthread.h>
#include <lo/lo.h>

#include "voc_demo.h"

pthread_mutex_t vd_lock;
voc_demo_d vd;
int stop = 0;

void error(int num, const char *msg, const char *path) {
    printf("liblo server error %d in path %s: %s\n", num, path, msg);
}

/**/

int generic_handler(const char *path, const char *types, lo_arg **argv,
		    int argc, void *data, void *user_data) {
    int i;
    
    printf("path: <%s>\n", path);
    for (i=0; i<argc; i++) {
      printf("arg %d '%c' ", i, types[i]);
      lo_arg_pp(types[i], argv[i]);
      printf("\n");
    }
    printf("\n");

    return 1;
}

/**/

int voc_handler(const char *path, const char *types, lo_arg **argv,
		int argc, void *data, void *user_data) {

  //pthread_mutex_lock(&lock);
  vd.gain         = argv[0]->f;
  *vd.freq         = argv[1]->f;
  *vd.velum        = argv[2]->f;
  *vd.tenseness    = argv[3]->f;
  vd.tongue_pos   = argv[4]->f;
  vd.tongue_diam  = argv[5]->f;
  //pthread_mutex_unlock(&lock);
  return(0);
}

/**/

int stop_handler(const char *path, const char *types, lo_arg **argv,
		int argc, void *data, void *user_data) {

  stop = 1;
  return(0);
}

/**/

int osc_server_init(char *osc_port) {

  lo_server_thread st = lo_server_thread_new(osc_port, error);

  lo_server_thread_add_method(st, "/voc", "ffffff", voc_handler, NULL);
  lo_server_thread_add_method(st, "/stop", NULL, stop_handler, NULL);
  lo_server_thread_add_method(st, NULL, NULL, generic_handler, NULL);
  lo_server_thread_start(st);
  
  return(1);
}



int main(int argc, char *argv[]) {
    int i;

    voc_demo_setup(&vd);
    osc_server_init("6060");
    voc_demo_start(&vd);

    vd.mode = VOC_TONGUE;
  
    while (!stop) {
      sleep(5);
    }
    
    voc_demo_stop(&vd);
    voc_demo_destroy(&vd);
}

