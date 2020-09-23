from ser_encodings.tc1 import TC1
from ser_encodings.tc3 import TC3
from ser_encodings.tc import TC
from ser_encodings.topo import TopoBitVec, TopoInt
from ser_encodings.axiom import Axiomatic
from ser_encodings.mono import Mono
from ser_encodings.tree import TreeBV
from ser_encodings.binary import (
    BinaryLabelMinisat, BinaryLabelZ3, BinaryLabelYices
)
from ser_encodings.unary import (
    UnaryLabelMinisat, UnaryLabelZ3, UnaryLabelYices
)

ENCODING_CLASSES = [TC1, TC3, TC, 
                    TopoBitVec, TopoInt, 
                    Axiomatic, Mono, TreeBV,
                    BinaryLabelMinisat, BinaryLabelZ3,
                    UnaryLabelMinisat, UnaryLabelZ3, UnaryLabelYices
                    ]
