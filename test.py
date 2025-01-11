import pytest
from Proyek_UAS_Asamny import *

def test_place_chips1(): #Success test
    B = BlackChip()
    W = WhiteChip()
    assert B.place_chip("C",5)
    assert W.place_chip("C",6)
    assert B.place_chip("D",6)
    assert W.place_chip("C",4)
    assert B.place_chip("C",3)
    assert W.place_chip("E",6)
    assert B.place_chip("C",7)
    assert W.place_chip("B",8)
    assert B.place_chip("D",7)
    assert W.place_chip("E",7)
    assert B.place_chip("F",8)
    assert W.place_chip("C",2)
    assert B.place_chip("E",3)
    assert W.place_chip("D",3)
    assert B.place_chip("B",3)
    assert W.place_chip("B",4)
    assert B.place_chip("A",5)
    assert W.place_chip("F",7)
    assert B.place_chip("G",8)
    assert W.place_chip("F",6)
    assert B.place_chip("B",7)
    assert W.place_chip("B",2)
    assert B.place_chip("G",6)
    assert W.place_chip("G",7)
    assert B.place_chip("C",1)
    assert W.place_chip("A",7)
    assert B.place_chip("A",1)
    assert W.place_chip("E",2)
    assert B.place_chip("H",8)
    assert W.place_chip("A",2)
    assert B.place_chip("A",3)
    assert W.place_chip("A",4)
    assert B.place_chip("A",8)
    assert W.place_chip("D",2)
    assert B.place_chip("F",2)
    assert W.place_chip("E",1)
    assert B.place_chip("F",3)
    assert W.place_chip("G",4)
    assert B.place_chip("F",4)
    assert W.place_chip("D",1)
    assert B.place_chip("F",1)
    assert W.place_chip("B",1)
    assert B.place_chip("B",5)
    assert W.place_chip("B",6)
    assert B.place_chip("A",6)
    assert W.place_chip("H",7)
    assert B.place_chip("H",4)
    assert W.place_chip("F",5)
    assert B.place_chip("G",5)
    assert W.place_chip("H",5)
    assert B.place_chip("E",8)
    assert W.place_chip("G",3)
    assert B.place_chip("D",8)
    assert W.place_chip("H",3)
    assert B.place_chip("G",2)
    assert W.place_chip("C",8)
    assert B.place_chip("H",6)
    assert W.place_chip("G",1)
    assert B.place_chip("H",2)
    assert B.place_chip("H",1)

def test_place_chips_same_tile(): #Failed test, reason : placement on the same tile 
    B = BlackChip()
    W = WhiteChip()
    Board().reset(BoardGame)
    assert B.place_chip("C",5)
    assert W.place_chip("C",5)

def test_place_chips_wrong_tiles(): #Failed test, reason : placing on the unsupported tile
    B = BlackChip()
    W = WhiteChip()
    Board().reset(BoardGame)
    assert B.place_chip("C",7)

def test_place_chips_wrong_coordinate(): #Failed test, reason : placing on the unsupported tile
    B = BlackChip()
    W = WhiteChip()
    Board().reset(BoardGame)
    assert B.place_chip("I",9)