#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "relais_client.h"

enum rclient_command_type {
    GET,
    POST,
    DELETE
};

static const char format_raw[] = "?format=raw";

static size_t writer(char *ptr, size_t size, size_t nmemb, void *userdata)
{
    struct rclient *rc = userdata;
    size_t len = size * nmemb;

    if (rc->buf_idx + len < rc->buf_idx || rc->buf_idx + len > BUF_MAXLEN)
        return len - 1;

    memcpy(rc->buf + rc->buf_idx, ptr, len);
    rc->buf_idx += len;
    return len;
}

int rclient_init(struct rclient *rc, const char *host, unsigned short port)
{
    size_t url_alloc;
    /* build url buffer */
    rc->url_len = snprintf(NULL, 0, "http://%s:%u/ports", host, port);
    url_alloc = rc->url_len + strlen("/X") + strlen(format_raw) + 1;
    rc->url_free = url_alloc - rc->url_len;
    if ((rc->url = malloc(url_alloc)) == NULL)
        return -1;
    snprintf(rc->url, rc->url_len + 1, "http://%s:%u/ports", host, port);
    rc->buf_idx = 0;

    /* initialize libcurl */
    if (curl_global_init(CURL_GLOBAL_ALL & (~CURL_GLOBAL_SSL)) != 0)
        return -1;
    if ((rc->curl = curl_easy_init()) == NULL)
        return -1;
    curl_easy_setopt(rc->curl, CURLOPT_WRITEFUNCTION, writer);
    curl_easy_setopt(rc->curl, CURLOPT_WRITEDATA, rc);
    return 0;
}

void rclient_cleanup(struct rclient *rc)
{
    curl_easy_cleanup(rc->curl);
    curl_global_cleanup();
    free(rc->url);
}

/**
 * send_command() - send command to py-webrelais using specified type and port
 * @type:   type of http request to use
 * @port:   pointer to port number or NULL if action shall affect all ports
 *
 * Returns 0 for success and -1 in case of error
 */
static int send_command(struct rclient *rc, enum rclient_command_type type,
                                                        const uint8_t *port)
{
    if (port && *port > 7)
        return -1;
    if (port) /* append port number to base url */
        snprintf(rc->url + rc->url_len, rc->url_free, "/%u%s", *port, format_raw);
    else
        strncpy(rc->url + rc->url_len, format_raw, rc->url_free);
    curl_easy_setopt(rc->curl, CURLOPT_URL, rc->url);

    switch (type) {
    case POST:
        curl_easy_setopt(rc->curl, CURLOPT_POST, 1);
        break;
    case DELETE:
        curl_easy_setopt(rc->curl, CURLOPT_CUSTOMREQUEST, "DELETE"); 
        break;
    default:
        curl_easy_setopt(rc->curl, CURLOPT_HTTPGET, 1L);
        break;
    }
    rc->buf_idx = 0;
    if (curl_easy_perform(rc->curl) != 0)
        return -1;
    rc->buf[rc->buf_idx] = '\0';
    return 0;
}

static inline int parse_response(const char r)
{
    if (r == '0' || r == '1')
        return r - '0';
    return -1;
}

static int parse_multi_response(const char *r, uint8_t res[NUM_PORTS])
{
    int i, ret;
    for (i = 0; i < NUM_PORTS; i++, r++) {
        if ((ret = parse_response(*r)) < 0)
            return -1;
        res[i] = ret;
    }
    return 0;
}

int rclient_get_port(struct rclient *rc, uint8_t port)
{
    if (send_command(rc, GET, &port) == -1)
        return -1;
    return parse_response(rc->buf[0]);
}

int rclient_get_ports(struct rclient *rc, uint8_t ports[NUM_PORTS])
{
    if (send_command(rc, GET, NULL) == -1)
        return -1;
    return parse_multi_response(rc->buf, ports);
}

int rclient_set_port(struct rclient *rc, uint8_t port)
{
    return send_command(rc, POST, &port);
}

int rclient_set_ports(struct rclient *rc)
{
    return send_command(rc, POST, NULL);
}

int rclient_reset_port(struct rclient *rc, uint8_t port)
{
    return send_command(rc, DELETE, &port);
}

int rclient_reset_ports(struct rclient *rc)
{
    return send_command(rc, DELETE, NULL);
}
