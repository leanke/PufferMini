#include <stdlib.h>
#include <stdbool.h>
#include <math.h>
#include "raylib.h"

#define LOG_BUFFER_SIZE 1024

typedef struct Log Log;
struct Log {
    // Add any things you want to keep track of here
    // These will be your 'infos' that are seen on the
    // dashboard as training runs, and on wandb or neptune
    float episode_return;
    float episode_length;
    float score;
};

typedef struct LogBuffer LogBuffer;
struct LogBuffer {
    Log* logs;
    int length;
    int idx;
};

LogBuffer* allocate_logbuffer(int size) {
    LogBuffer* logs = (LogBuffer*)calloc(1, sizeof(LogBuffer));
    logs->logs = (Log*)calloc(size, sizeof(Log));
    logs->length = size;
    logs->idx = 0;
    return logs;
}

void free_logbuffer(LogBuffer* buffer) {
    free(buffer->logs);
    free(buffer);
}

void add_log(LogBuffer* logs, Log* log) {
    if (logs->idx == logs->length) {
        return;
    }
    logs->logs[logs->idx] = *log;
    logs->idx += 1;
    //printf("Log: %f, %f, %f\n", log->episode_return, log->episode_length, log->score);
}

Log aggregate_and_clear(LogBuffer* logs) {
    Log log = {0};
    if (logs->idx == 0) {
        return log;
    }
    for (int i = 0; i < logs->idx; i++) {
        log.episode_return += logs->logs[i].episode_return;
        log.episode_length += logs->logs[i].episode_length;
        log.score += logs->logs[i].score;
    }
    log.episode_return /= logs->idx;
    log.episode_length /= logs->idx;
    log.score /= logs->idx;
    logs->idx = 0;
    return log;
}
 
typedef struct Template Template;
struct Template {
    float* observations;
    int* actions;
    float* rewards;
    unsigned char* terminals;
    LogBuffer* log_buffer;
    Log log;
    float width;
    float height;
    int score;
    int max_score;
    int tick;
    int win;
    int frameskip;
};

void init(Template* env) {
    // logging
    env->tick = 0;
    env->win = 0;

}

void allocate(Template* env) {
    init(env);
    env->observations = (float*)calloc(8, sizeof(float));
    env->actions = (int*)calloc(2, sizeof(int));
    env->rewards = (float*)calloc(1, sizeof(float));
    env->terminals = (unsigned char*)calloc(1, sizeof(unsigned char));
    env->log_buffer = allocate_logbuffer(LOG_BUFFER_SIZE);
}

void free_allocated(Template* env) {
    free(env->observations);
    free(env->actions);
    free(env->rewards);
    free(env->terminals);
    free_logbuffer(env->log_buffer);
}

void compute_observations(Template* env) {
    // Add any observations (what the agent can 'see') here
    // env->observations[0] = 
    // env->observations[1] = 
    // env->observations[2] = 
    // env->observations[3] = 
    // env->observations[4] = 
    // env->observations[5] = 
    // env->observations[6] = 
    // env->observations[7] = 
}

void c_reset(Template* env) {
    // Add any reset logic here
    env->log = (Log){0};
    env->score = 0;
    compute_observations(env);
}

// Reset the round but not the entire episode
void reset_round(Template* env) {
    // Add whatever would make sense to reset for the round
    // e.g. for pong,
    // env->n_bounces = 0;
    env->tick = 0;
}

void c_step(Template* env) {
    env->tick += 1;
    env->log.episode_length += 1;
    env->rewards[0] = 0;
    env->terminals[0] = 0;

    env->score += 1;
    env->rewards[0] = 1; // agent wins
    env->log.episode_return += 1;
    env->log.score += 1.0;

    if (env->score == env->max_score) {
        env->terminals[0] = 1;
        add_log(env->log_buffer, &env->log);
        c_reset(env);
        return;
    } else {
        reset_round(env);
        return;
    }
    compute_observations(env);
    }


typedef struct Client Client;
struct Client {
    float width;
    float height;
};

Client* make_client(Template* env) {
    Client* client = (Client*)calloc(1, sizeof(Client));
    client->width = env->width;
    client->height = env->height;
    return client;
}

void close_client(Client* client) {
    free(client);
}

void c_render(Client* client, Template* env) {
    // Add any rendering logic here
}