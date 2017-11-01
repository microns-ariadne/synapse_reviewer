import argparse
import copy
import json
import neuroglancer
import os
import sys
import time
import webbrowser

DEFAULT_STATIC_CONTENT_SOURCE = "http://localhost:8080"
DEFAULT_IMAGE_URL = \
    "ndstore://https://dojo.rc.fas.harvard.edu/R0::2017_08_23::88_88_14/1_1_1_raw"
DEFAULT_SEGMENTATION_URL = \
    "ndstore://https://dojo.rc.fas.harvard.edu/R0::2017_08_23::88_88_14/1_1_1_ids"
DEFAULT_SYNAPSE_FILE = \
    "/n/coxfs01/leek/results/2017-08-23_100um_cube/88_88_14/synapse-connections.json"

class Synapse(object):
    def __init__(self, neuron_1, neuron_2, x, y, z):
        self.neuron_1 = neuron_1
        self.neuron_2 = neuron_2
        self.x = x
        self.y = y
        self.z = z
        
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port",
                        default="8081",
                        help="The webserver's port")
    parser.add_argument(
        "--static-content-source",
        default=DEFAULT_STATIC_CONTENT_SOURCE,
        help="The URL of the webserver serving static content")
    parser.add_argument("--image-url",
                        default=DEFAULT_IMAGE_URL,
                        help="The Neuroglancer URL for the image data")
    parser.add_argument("--segmentation-url",
                        default=DEFAULT_SEGMENTATION_URL,
                        help="The Neuroglancer URL for the segmentation data")
    parser.add_argument("--synapses",
                        default = DEFAULT_SYNAPSE_FILE,
                        help="The .json file with synapse locations")
    parser.add_argument("--output",
                        help="The output file for the user classifications")
    return parser.parse_args()

current_segment_idx = 0
output_file_name = None
synapses = []
viewer = None

def set_viewer_state():
    synapse = synapses[current_segment_idx]
    viewer_state = copy.deepcopy(viewer.state)
    viewer_state.position.voxel_coordinates = [synapse.x, synapse.y, synapse.z]
    for layer in viewer_state.layers:
        if layer.name == "segmentation":
            if not hasattr(layer, "segments"):
                layer = layer.layer
            layer.segments.clear()
            layer.segments.add(synapse.neuron_1)
            layer.segments.add(synapse.neuron_2)
    viewer.set_state(viewer_state)
    
def skip():
    global current_segment_idx, synapses
    current_segment_idx += 1
    synapse = synapses[current_segment_idx]
    set_viewer_state()

def write(result):
    if not os.path.exists(output_file_name):
        with open(output_file_name, "w") as fd:
            fd.write(
                '"synapse_id","neuron_1","neuron_2","x","y","z","class"\n')
    with open(output_file_name, "a") as fd:
        synapse = synapses[current_segment_idx]
        fd.write('%d,%d,%d,%.1f,%.1f,%.1f,"%s"\n' % 
                 (current_segment_idx, synapse.neuron_1, synapse.neuron_2,
                  synapse.x, synapse.y, synapse.z, result))
    
def yes():
    write("yes")
    skip()

def no():
    write("no")
    skip()

def back():
    global current_segment_idx
    current_segment_idx = max(0, current_segment_idx-1)
    set_viewer_state()
            
def main():
    global output_file_name
    global synapses
    global viewer
    args = parse_args()
    neuroglancer.set_static_content_source(url=args.static_content_source)
    neuroglancer.set_server_bind_address(bind_port=int(args.port))
    image_url = args.image_url
    segmentation_url = args.segmentation_url
    output_file_name = args.output
    
    synapse_dict = json.load(open(args.synapses))
    
    for n1, n2, x, y, z in zip(
        synapse_dict["neuron_1"], synapse_dict["neuron_2"],
        synapse_dict["synapse_center"]["x"],
        synapse_dict["synapse_center"]["y"],
        synapse_dict["synapse_center"]["z"]):
        synapses.append(Synapse(n1, n2, x, y, z))
    
    viewer = neuroglancer.Viewer()
    with viewer.txn() as s:
        s.layers['image'] = neuroglancer.ImageLayer(
            source = image_url)
        s.layers['segmentation'] = neuroglancer.SegmentationLayer(
            source = segmentation_url)
    viewer.actions.add("yes", lambda _: yes())
    viewer.actions.add("no", lambda _: no())
    viewer.actions.add("skip", lambda _: skip())
    viewer.actions.add("back", lambda _: back())
    viewer.actions.add("revert", lambda _: set_viewer_state())
    with viewer.config_state.txn() as s:
        s.input_event_bindings.viewer['shift+keyy'] = 'yes'
        s.input_event_bindings.viewer["shift+keyn"] = "no"
        s.input_event_bindings.viewer["shift+keys"] = "skip"
        s.input_event_bindings.viewer["shift+keyr"] = "revert"
        s.input_event_bindings.viewer["shift+keyb"] = "back"
    set_viewer_state()
    webbrowser.open_new(viewer.get_viewer_url())
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
    