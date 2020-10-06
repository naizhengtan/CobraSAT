from serializability.tc1 import TC1
from serializability.tc3 import TC3
from serializability.tc import TC
from serializability.topo import TopoBitVec, TopoInt
from serializability.axiom import Axiomatic
from serializability.mono import Mono
from serializability.tree import TreeBV
from serializability.binary import (
    BinaryLabelMinisat, BinaryLabelZ3, BinaryLabelYices
)
from serializability.unary import (
    UnaryLabelMinisat, UnaryLabelZ3, UnaryLabelYices
)

ENCODING_CLASSES = [TC1, TC3, TC,
                    TopoBitVec, TopoInt,
                    Axiomatic, Mono, TreeBV,
                    BinaryLabelMinisat, BinaryLabelZ3,
                    UnaryLabelMinisat, UnaryLabelZ3, UnaryLabelYices
                    ]
