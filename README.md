## Instructions
# Important step: star PufferLib on github! This is an open-source project and the stars really help us out! https://github.com/PufferAI/PufferLib
# (You will see a Star that says Starred 2k on the right-hand side near the top of the page. Click it; thanks!)

## TLDR:
git clone https://github.com/leanke/PufferMini.git
# All commands should be run from the PufferMini top dir - the project's root directory, so we cd PufferMini
cd PufferMini
# Run pip install command
pip install -e .
# Make your custom environment. We'll name it 'kewl_env' for now.
./create.sh kewl_env
# Compile. I could have had the create.sh script do this but it's good to do manually just so you're aware:
python setup.py build_ext --inplace
# Run training on your new env!
python demo.py --mode train --env kewl_env
# Know that, while it appears to be 'doing something,' it is actually doing nothing. You will need to actually add code to the kewl_env.h file at the very least to fully describe the environment (using code, generally in the step function), determine what the environment can 'see' (typically added to the compute_observations function), any rendering logic if you want to actually be able to eval trained policies visually (add to the c_render function), and any additional logging info you want to keep track of for training (added in both the cy_kewl_env.pyx and kewl_env.h files, in the Log struct)

## END TLDR SECTION

## Below is a more-in-depth introduction:
# Try to run pong training (if you want to see if it works):
python demo.py --mode train --env pong
# or, if you want to use the convenient run script:
./run

# To watch the dummy policy play:
python demo.py --mode eval --env pong

# When training, your env will save a policy ('model') file every checkpoint_interval epochs. The default setting is 25. 
# Policies are, by default, saved in the PufferMini/experiments/ directory. Here is an example path of a policy I just trained (actual file *not* included): PufferMini/experiments/pong-14c770b5/model_000025.pt

# To evaluate the above trained policy:
python demo.py --mode eval --env pong --eval-model-path experiments/pong-14c770b5/model_000025.pt

## Env structure
# For pong, the environment's directory is found in PufferMini/pong
# Critical files are:
# PufferMini/pong/pong.py
# PufferMini/pong/cy_pong.pyx
# PufferMini/pong/pong.h
# PufferMini/pong/pong.c
# PufferMini/config/pong.ini
# PufferMini/setup.py

## How to add your own environment (called 'cats' in this example)
./create.sh cats

# This will create the above requisite files and add your env to setup.py.

# NOTE: if you make changes to the .pyx, .h, or .c files, you will need to recompile. To recompile:
python setup.py build_ext --inplace

# Q and A
Q: Are LSTM wrappers a requirement? 
A: Several envs work without LSTM. LSTM provides a nice kind of 'context window,' and this one is pretty lightweight.
It's generally worth. And, if you need to capture, say, temporal changes, without using e.g. LSTM, you'd need to explicitly design for it, e.g. by using framestacking. The default Puffer LSTM ('Recurrent') is very sample-efficient as well, often being faster in wall-clock time vs the Default network alone.

# Further questions can be asked in the support thread "New to pufferlib help thread ask whatever" in the pufferlib discord channel. https://discord.com/channels/1019421966429593712/1324143625994502165
# There are a bunch of other questions and answers in there as well.

# Documentation on pufferlib and a link to join the Discord can be found at https://puffer.ai/

## Authors:
# PufferLib and puffer.ai: Joseph Suarez
# PufferMini: Leanke (https://github.com/leanke/PufferMini.git)
# README.md: xinpw8 (https://github.com/xinpw8)