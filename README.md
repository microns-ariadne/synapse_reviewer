# synapse_reviewer
Neuroglancer project to allow a reviewer to classify putative synapses as real or false-negative

This project runs Neuroglancer with Python callbacks to review synapses.
The user runs `synapse-reviewer` and is presented with synapses in Neuroglancer
to rate as true positives or false negatives. There are several keyboard
commands within Neuroglancer:

- **Y**: yes, it is a synapse
- **N**: no, it is not a synapse
- **S**: skip to next synapse
- **R**: refresh the display

## Installation

To install the Python dependencies
```
> git clone https://github.com/google/neuroglancer
> cd neuroglancer/python
> pip install --editable .
> git clone https://github.com/microns-ariadne/synapse_reviewer
> cd synapse_reviewer
> pip install --editable .
```
In addition, you have to install the Python dev server on your machine.
Follow steps 1-3 here: https://github.com/google/neuroglancer#building
Then start the webserver using the command, `npm run dev-server-python`

The Python install should install the `synapse-reviewer` program into your
environment. Running `synapse-reviewer` will start a webserver serving the Python
application.


## Command-line arguments.


Invoke the reader like this:

```synapse-reviewer` \
     [--port <PORT>] \
     [--static-content-source <SOURCE>] \
     [--image-url <IMAGE_URL>] \
     [--segmentation-url <SEGMENTATION_URL>] \
     [--synapses <SYNAPSE_CONNECTIONS_FILE>] \
     --output <RESULTS_FILE>
```
where:

* **PORT** is the port that the Python webserver runs on (default is 8081).
* **SOURCE** is the URL of the static content webserver. (default is
http://localhost:8080 which would be the webserver that is started on your
local machine with the `npm run dev-server-python` command).
* **IMAGE_URL** is the Neuroglancer / Butterfly / Dojo url of your image datasource.
The default is `ndstore://https://dojo.rc.fas.harvard.edu/R0::2017_08_23::88_88_14/1_1_1_raw`
which is the URL within Harvard of our 100um cube. If you are within Harvard,
you can ask one of the Dojo / Butterfly admins to host your image datasource
there. If you're outside of Harvard, you can make your own arrangements to
host a datasource serving one of the Neuroglancer-supported formats.
* **SEGMENTATION_URL** is the Neuroglancer / Butterfly / Dojo url of your
segmentation datasource. By default, this is a matching segmentation to
the R0 image datasource. See **IMAGE_URL** above for setting up your own.
* **SYNAPSE_CONNECTIONS_FILE** is the path to a JSON file containing the
segment IDs of the pre- and post- synaptic neurons and the X, Y and Z locations
of the synapse in voxel coordinates. See https://github.com/microns-ariadne/pipeline_engine#synapse-connectionsjson-file-format
for a description of this file format. The segment IDs should match those in
the volume named by the *SEGMENTATION_URL*.
* **OUTPUT** This is the filename that will hold the results of the user's
classification. See below for file format. Results are appended to the end
of the output file, allowing multiple users to classify different sections
or allowing a single user to edit the same file across sessions.

## Format of output file.

The output file is a CSV file with the following fields:

* **synapse_id** The index of the synapse within the **SYNAPSE_CONNECTIONS_FILE**
* **neuron_1** The segment ID of the presynaptic neuron.
* **neuron_2** The segment ID of the postsynaptic neuron.
* **x** The voxel coordinate of the synapse in the X direction
* **y** The voxel coordinate of the synapse in the Y direction
* **z** The voxel coordinate of the synapse in the Z direction
* **class** Either "yes" or "no" depending on whether the user accepted or
rejected the synapse.
