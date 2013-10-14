#!/usr/bin/env python
# Written by: DGC

# python imports
import sys
import unittest

# local imports
import test_utils

sys.path.append("..")
import ImageConverter

#==============================================================================
class utest_ImageConverter(unittest.TestCase):
    DATA = [
        (test_utils.data_dir() + "/Images/bold.png", "iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAiEgAAIhIBv2R/3AAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAUySURBVHic7ZtfiFRVHMe/v3NnZm+uaxphsGolbVFkuzPduwstCM1LBfbQvwdFgiDIQA2lh9QgfAn0QQiVKH0xowiLKCF7a4NqdeeeWdhloyyywDIRMmvNdoa98+1hXbEZd+bec+/O3Ck/jzPn+zvnfrnnd+85v3OFJP7PqFYPoNVcN6DVA2g1qeofRESy2eyNzR5IZ2en393dfenIkSN+M/uV6iSYy+UWW5b1ezMHUUUZwF8ALgH4CcCYiIyTPKq1/jXuzpJowFxMAThQqVR2j46OnokraDvlABvAC0qpHxzH2ZfNZpfFEbSdDJjFFpFNqVTqG9d1H4sarMYAy7LKAL6LGrgJdAH40HXdV6IEqckBsziO4wB4RkQ2RemgSazXWr9rIpzTgFlc190MYK9J8CYyqZTKFgqFU2GFDXOA1nofgI+MhjXDYaVUDsA9AHp8379LKfUgyacB7ABwCDOPvCh0kdxsImx4BwCA4zgbRWS/SQcAdmutt9Vr0NfXtzSdTm8FsBEzc9uEc11dXcuGhoamw4gCPQVIDpmNKRhjY2PntNbblVIPAPjTMMzSyclJJ6woqAGxvXjUo1AofC0i6wBUDEPcGlaQuPcAz/OOichbhvIVYQWJM+AyXxrqJKwgkQb4vn/CREfybFhNIg2wbTv0hQCAiITOVYk0oFQqDRjIpgCMhBUl0gARGTSQfaa1Dv1ClTgDREQBeNhAZ/SiljgDXNfdAyDUFCB51PO8T036S5QB/f39m0huCSmbSqVSYTVXqNkUbQWu694H4CUA68JqSe4aGRn50bTvlhiQy+UWi0i3iNwhIhsArDEMdXjRokWvRhlLoNVgxI3S0yRPiYgF4BYAywAsMIx1NXuLxeIWRqztNeMOWCEiod/R6/AHyZ3FYvG1OIIlIgeE4INyufzc+Ph4bNv2iXoKNILkbZlM5lnHcVbn83k7jpjNyAHzxXmSezs6OvYNDw+fNw3SzgbMchHAmwD2mJTO2moKzMFCAC8C+N5xnMfDiptxBxwkuT+VSk2RnCa5oFKpLMfM02G5iKwguRpAj2H8qyGA7Vrr3UEF8/4UEJEzWuvxqp8nqtoox3GeBLANwP1RugOwy3Xds1rrQNtqiZgCJCta6/e11o6IrMHMvI7C6wMDA/cGaZgIA67G87xjANYCiHJQYgHJQ0EaJs4AANBafwJga5QYJN3+/v6Gy+pEGgBcKcl9FTHM840aJNYAACAZyQCSa/P5fN1En2gDYLDJWcUNFy5cWF6vQaIN8H0/qgEQkbrlskQbYNt2qErvtWhrA6anp/tiCHNzvT8TbQDJOAyou0BKtAFKqdD1/mosyzpdt4+oHcwXjuOsJvlUDKHaz4De3t4lIvIOACtiqDOe5/1Sr0HiDBgcHLwpk8m8DYPDDtWQPECy7mmTQMthEemNOphGrFq1KmPb9mYALwNYEkPIaRE50KhRIAMsy3rUdPud5OJcLnd7Tcep1EKSPQB6RORO27YfAlDTLgIHg2yRBTkoeTeAzzFT1GgLSA6XSqX8xMREuVHbOXPA5V2aRwB8gTa6eAA/p9PpJ4JcPHCNO8B13bSI7Lx8kjPOis68Q/KoZVkbCoVC4CM2NTnA9/1Oy7J2xDu0eee8iGzVWh8OK2y30ti/IOkppd4g+Z7neUbnjdvNgIskT4jIMICPi8XiaNSASTOAAEoA/gbwG4CTAL4leVIppVeuXDke91dlNUmwFZ/NWZbFTCZTPn78+FTUen9YAlWG/sskbi3QbK4b0OoBtJp/AFEizfwdD5OPAAAAAElFTkSuQmCC"),
        ]

    def test_non_existant_image(self):
        self.assertRaises(
            IOError,
            ImageConverter.image_to_base_64_bytes,
            "non_existant_file.no_extension"
            )
        
    def test_images(self):
        """
        This tests the bytes from some images in Resources.
        """
        for data in self.DATA:
            self.assertEqual(
                ImageConverter.image_to_base_64_bytes(data[0]),
                data[1]
                )
        
    def test_html(self):
        for data in self.DATA:
            html = ImageConverter.path_to_image_tag(data[0])
            self.assertIn("<img ", html)
            self.assertIn("src", html)
            self.assertIn("alt", html)
            self.assertIn(data[1], html)

#==============================================================================
if (__name__ == "__main__"):
    unittest.main(verbosity=2)
