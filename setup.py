import setuptools

VERSION = "1.0.0"
setuptools.setup(
    description="Neuroglancer project to allow a reviewer to classify synapses",
    entry_points={
        "console_scripts": [
            "synapse-reviewer=synapse_reviewer:main" ]
        },
    name="synapse_reviewer",
    version=VERSION,
    url="https://github.com/microns-ariadne/synapse_reviewer",
    install_requires=[
        "neuroglancer",
        "numpy"])
    