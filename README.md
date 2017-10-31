# synapse_reviewer
Neuroglancer project to allow a reviewer to classify putative synapses as real or false-negative

This project runs Neuroglancer with Python callbacks to review synapses.
The user runs `synapse-reviewer` and is presented with synapses in Neuroglancer
to rate as true positives or false negatives. There are several keyboard
commands within Neuroglancer:

- *Y*: yes, it is a synapse
- *N*: no, it is not a synapse
- *S*: skip to next synapse
- *R*: refresh the display

