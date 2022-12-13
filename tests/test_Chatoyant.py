# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 10:26:53 2022

@author: Sylvain
Tests written for Chatoyant
"""

import pytest
import Chatoyant

class TestEmptyColorMap:
    
    @pytest.fixture(scope="class")
    def empty_cmap(self):
        return Chatoyant.ColorMap('empty')
    
    def test_empty(self, empty_cmap):
        assert len(empty_cmap) == 0
        assert empty_cmap.name == 'empty'
        
@pytest.fixture(scope='module')
def simpleCMap():
    return Chatoyant.ColorMap('simple1', [(255, 0, 0), (0, 0, 0)])

@pytest.fixture(scope='module')
def CMap():
    return Chatoyant.ColorMap('cmap2').from_matplotlib('inferno', n=10)

class TestSimpleBuild:
    
    def test_simple(self, simpleCMap):
        assert len(simpleCMap) == 2
        assert simpleCMap.to_tuple_list() == [(255, 0, 0), (0, 0, 0)]
    
    def test_name(self, simpleCMap):
        assert simpleCMap.name == 'simple1'
        assert simpleCMap.set_name('simple2').name == 'simple2'

class TestImporters:
    
    @pytest.fixture(scope="class")
    def mplCMap(self):
        return Chatoyant.ColorMap().from_matplotlib('RdBu', n=3)
    
    @pytest.fixture(scope="class")
    def bkhCMap(self):
        return Chatoyant.ColorMap().from_matplotlib('RdBu', n=3)
    
    @pytest.fixture(scope="class")
    def listCMap(self):
        return Chatoyant.ColorMap().from_list([(255, 0, 0), 'black'])
    
    def test_mplcmap(self, mplCMap):
        assert len(mplCMap) == 3
        assert mplCMap.to_tuple_list() == [(103, 0, 31), (247, 247, 247), (5, 48, 97)]
        
    def test_bkhcmap(self, bkhCMap):
        assert len(bkhCMap) == 3
        assert bkhCMap.to_tuple_list() == [(103, 0, 31), (247, 247, 247), (5, 48, 97)]
        
    def test_identity(self, mplCMap, bkhCMap):
        assert mplCMap == bkhCMap
        
    def test_listcmap(self, listCMap):
        assert len(listCMap) == 2
        assert listCMap.to_tuple_list() == [(255, 0, 0), (0, 0, 0)]
    
class TestOperations:
    
    def test_add(self, simpleCMap):
        assert len(simpleCMap + simpleCMap) == 4
        assert (simpleCMap + simpleCMap).to_tuple_list() == [(255, 0, 0), (0, 0, 0),
                                                             (255, 0, 0), (0, 0, 0)]
    def test_loop(self, simpleCMap):
        
        assert len(simpleCMap.loop(2)) == 6
        assert simpleCMap.loop(1).to_tuple_list() == [(255, 0, 0), (0, 0, 0),
                                                      (255, 0, 0), (0, 0, 0)]
    def test_extend(self, simpleCMap):
        
        assert len(simpleCMap.extend(3)) == 3
        # Extend will insert a 'middle' color
        assert simpleCMap.extend(3).to_tuple_list() == [(255, 0, 0), (127, 0, 0), (0, 0, 0)]
        # Extension then opposite should give the identity result.
        assert simpleCMap.extend(10).extend(2) == simpleCMap
    
    def test_invert(self, simpleCMap):
        
        assert len(simpleCMap + simpleCMap.invert()) == 4
        assert (simpleCMap + simpleCMap.invert()).to_tuple_list() == [(255, 0, 0), (0, 0, 0), 
                                                                      (0, 0, 0), (255, 0, 0)]
        
    def test_HLS_RGB(self, simpleCMap):
        # Should be absolutely identical (255, 0, 0) 
        # but the multiple /255 and *255 introduce errors. Should have used floats
        assert simpleCMap.to_HLS().to_RGB().to_tuple_list() == [(254, 0, 0), (0, 0, 0)]
        
    def test_shift(self, simpleCMap):
        assert simpleCMap.shift(by=(0, 20, 20)).to_tuple_list() == [(255, 20, 20), (0, 20, 20)]
        
    def test_shift_hue(self, simpleCMap):
        assert simpleCMap.shift_hue().to_tuple_list() == [(254, 119, 0), (0, 0, 0)]
                


        
        


    
