#include "template.h"
#include "../pufferlib/puffernet.h"

int main() {
    Weights* weights = load_weights("resources/template_weights.bin", 133764);
    LinearLSTM* net = make_linearlstm(weights, 1, 8, 3);

    Template env = {
        .width = 500,
        .height = 640,
        .score = 0,
        .max_score = 21,
        .frameskip = 1,
    };
    allocate(&env);

    Client* client = make_client(&env);

    c_reset(&env);
    while (!WindowShouldClose()) {
        // User can take control of the paddle
        if (IsKeyDown(KEY_LEFT_SHIFT)) {
            env.actions[0] = 0;
            if (IsKeyDown(KEY_UP)    || IsKeyDown(KEY_W)) env.actions[0] = 1;
            if (IsKeyDown(KEY_DOWN)  || IsKeyDown(KEY_S)) env.actions[0] = 2;
        } else {
            forward_linearlstm(net, env.observations, env.actions);
        }

        c_step(&env);
        c_render(client, &env);
    }
    free_linearlstm(net);
    free(weights);
    free_allocated(&env);
    close_client(client);
}
