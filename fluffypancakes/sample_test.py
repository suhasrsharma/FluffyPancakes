# -*- coding: utf-8 -*-
"""
@authors: Suhas Sharma and Rahul P
"""
import pytest
import fluffypancakes

def test_fluffypancakes(url):
    return fluffypancakes.serve(url, progressBar=False)

def test_answer():
    assert test_fluffypancakes('pes.edu') == -1