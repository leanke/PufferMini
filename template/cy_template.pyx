cimport numpy as cnp
from libc.stdlib cimport calloc, free
import os

cdef extern from "template.h":
    int LOG_BUFFER_SIZE

    ctypedef struct Log:
        # Should be identical to the Log struct in template.h
        # Add any things you want to keep track of here
        # These will be your 'infos' that are seen on the
        # dashboard as training runs, and on wandb or neptune
        float episode_return
        float episode_length
        float score

    ctypedef struct LogBuffer
    LogBuffer* allocate_logbuffer(int)
    void free_logbuffer(LogBuffer*)
    Log aggregate_and_clear(LogBuffer*)

    ctypedef struct Template:
        float* observations
        int* actions
        float* rewards
        unsigned char* terminals
        LogBuffer* log_buffer
        Log log
        unsigned int score
        float width
        float height
        unsigned int max_score
        int tick
        int win
        int frameskip

    ctypedef struct Client

    void init(Template* env)
    void c_reset(Template* env)
    void c_step(Template* env)

    Client* make_client(Template* env)
    void close_client(Client* client)
    void c_render(Client* client, Template* env)

cdef class CyTemplate:
    cdef:
        Template* envs
        Client* client
        LogBuffer* logs
        int num_envs
        float width
        float height

    def __init__(self, float[:, :] observations, int[:] actions, float[:] rewards, unsigned char[:] terminals, int num_envs, float width, float height, unsigned int max_score, int frameskip):
        self.num_envs = num_envs
        self.client = NULL
        self.envs = <Template*> calloc(num_envs, sizeof(Template))
        self.logs = allocate_logbuffer(LOG_BUFFER_SIZE)

        cdef int i
        for i in range(num_envs):
            self.envs[i] = Template(
                observations = &observations[i, 0],
                actions = &actions[i],
                rewards = &rewards[i],
                terminals = &terminals[i],
                log_buffer=self.logs,
                width=width,
                height=height,
                max_score=max_score,
                frameskip=frameskip,
            )
            init(&self.envs[i])

    def reset(self):
        cdef int i
        for i in range(self.num_envs):
            c_reset(&self.envs[i])

    def step(self):
        cdef int i
        for i in range(self.num_envs):
            c_step(&self.envs[i])

    def render(self):
        cdef Template* env = &self.envs[0]
        if self.client == NULL:
            import os
            cwd = os.getcwd()
            os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
            self.client = make_client(env)
            os.chdir(cwd)

        c_render(self.client, env)

    def close(self):
        if self.client != NULL:
            close_client(self.client)
            self.client = NULL

        free(self.envs)
        free(self.logs)

    def log(self):
        cdef Log log = aggregate_and_clear(self.logs)
        return log