from pynq import Overlay
import pynq.lib as lib

class FPGABitstream:
    overlay = None
    i2c = None
    def init_hw(self, filepath):
        self.overlay = Overlay(filepath)
        self.overlay.download()

    def __init__(self, bitstream_file):
        # Initializing bitstream
        self.init_hw(bitstream_file)
        self.i2c = lib.AxiIIC(self.overlay.ip_dict['axi_iic_0'])

