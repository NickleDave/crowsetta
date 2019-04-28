"""module with functions to work with Audacity project (.aup) files"""
import xml.etree.ElementTree as ET

import numpy as np

from .sequence import Sequence
from . import csv

AUP_NAMESPACE = {
    "aup": "http://audacity.sourceforge.net/xml/"
}


def aup2seq(aup_file):
    tree = ET.parse(aup_file)
    root = tree.getroot()
    wavetrack = root.findall(
        "aup:wavetrack", namespaces=AUP_NAMESPACE
    )
    if len(wavetrack) > 1:
        raise ValueError(
            f"Found more than one wavetrack in {aup_file}, unclear which to associate with label tracks"
        )
    else:
        wavetrack = wavetrack[0]
        audio_file = wavetrack.attrib['name']

    labeltracks = root.findall(
        "aup:labeltrack", namespaces=AUP_NAMESPACE
    )

    seq_list_out = []
    for labeltrack in labeltracks:
        labels = labeltrack.findall(
        "aup:label", namespaces=AUP_NAMESPACE
        )

        onsets_s = np.asarray(
            [float(label.attrib['t']) for label in labels]
        )
        offsets_s = np.asarray(
            [float(label.attrib['t1'] for label in labels)]
        )
        labels = [label.attrib['title'] for label in labels]

        seq_obj = Sequence.from_keyword(
            file=audio_file,
            onsets_s=onsets_s,
            offsets_s=offsets_s,
            labels=labels
        )
        seq_list_out.append(seq_obj)

    return seq_list_out
