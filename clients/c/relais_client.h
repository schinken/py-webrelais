#ifndef RELAIS_CLIENT_H
#define RELAIS_CLIENT_H

#include <stddef.h>
#include <stdint.h>
#include <curl/curl.h>

#define BUF_MAXLEN 512
#define NUM_PORTS 8

struct rclient {
    CURL *curl;
    char *url;
    char buf[BUF_MAXLEN + 1];
    size_t url_len;
    size_t url_free;
    size_t buf_idx;
};

/**
 * rclient_init() - initialize a new relais client
 * @rc:     relais client to initialize
 * @host:   hostname or ip address of py-webrelais server
 * @port:   port to use (e.g. 80)
 *
 * returns 0 for success, -1 for error
 */
int rclient_init(struct rclient *rc, const char *host, unsigned short port);

/**
 * rclient_cleanup() - free resources used to communicate with py-webrelais
 * @rc:     handle initialized using rclient_init()
 */
void rclient_cleanup(struct rclient *rc);

/**
 * rclient_set/get/reset_ports() - manipulate state of port
 * @port:   0...NUM_PORTS-1
 * @ports:  ports array to fill with state (0 or 1)
 *
 * returns 0 (or 1 in rclient_get_port()) for success, -1 for error
 */
int rclient_get_port(struct rclient *rc, uint8_t port);
int rclient_get_ports(struct rclient *rc, uint8_t ports[NUM_PORTS]);

int rclient_set_port(struct rclient *rc, uint8_t port);
int rclient_set_ports(struct rclient *rc);

int rclient_reset_port(struct rclient *rc, uint8_t port);
int rclient_reset_ports(struct rclient *rc);
#endif
