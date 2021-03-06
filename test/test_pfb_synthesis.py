import logging
import unittest

import numpy as np

from pfb.pfb_synthesis import (
    pfb_synthesize,
    calc_input_tsamp)


class TestPFBSynthesis(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ndat = int(1e4)
        nchan = 8
        sample_data = (np.random.rand(ndat*nchan) +
                       1j*np.random.rand(ndat*nchan))
        sample_data = sample_data.reshape((ndat, nchan))

        cls.ndat = ndat
        cls.nchan = nchan
        cls.sample_data = sample_data
        cls.filter_coeff = np.random.rand(88)
        cls.os_factor = "8/7"

    def test_pfb_synthesize(self):
        synthesizer = pfb_synthesize(os_factor=self.os_factor,
                                     apply_deripple=False,
                                     fir_filter_coeff=self.filter_coeff)
        synthesizer(self.sample_data)

    def test_pfb_synthesize_deripple(self):
        synthesizer = pfb_synthesize(os_factor=self.os_factor,
                                     apply_deripple=True,
                                     fir_filter_coeff=self.filter_coeff)
        synthesizer(self.sample_data)

    def test_pfb_synthesize_fft_window(self):
        synthesizer = pfb_synthesize(os_factor=self.os_factor,
                                     apply_deripple=True,
                                     input_fft_length=1024,
                                     fft_window=(np.random.rand(1024)
                                                 .reshape((-1, 1))),
                                     fir_filter_coeff=self.filter_coeff)
        synthesizer(self.sample_data)

    def test_calc_input_tsamp(self):
        output_tsamp = 0.175
        output_tsamp = calc_input_tsamp(output_tsamp,
                                        nchan=8,
                                        os_factor="8/7")
        input_tsamp_expected = 0.025
        self.assertTrue(np.allclose(output_tsamp, input_tsamp_expected))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
