from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

saidA = {}
saidB = {}
saidC = {}

p0= """
Puzzle 0
***********************
A says "I am both a knight and a knave." 
***********************"""

knowledge0 = And(
      # A is a knight if and only if A is a knight and a knave
        Implication(AKnight, And(AKnight, AKnave)),
      # A is a knight or A is a knave
        Biconditional(AKnave, Not(AKnight))
    )

p1= """
Puzzle 1
***********************
# A says "We are both knaves."
# B says nothing.
***********************"""

knowledge1 = And(

    Implication(AKnight, And(AKnave, BKnave)),
    Implication(AKnave, Or(Not(AKnave), Not(BKnave))),
#    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    Biconditional(AKnave, Not(AKnight)),
#    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave)))
    Biconditional(BKnave, Not(BKnight))
)

p2= """
Puzzle 2
***********************
A says "We are the same kind."
B says "We are of different kinds."
***********************"""
knowledge2 = And(
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    Implication(AKnave, And(Or(Not(AKnight), Not(BKnight)), Or(Not(AKnave), Not(BKnave)))),
    Implication(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),
    Implication(BKnave, And(Or(Not(AKnight), Not(BKnave)), Or(Not(AKnave), Not(BKnight)))),
    # And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    # And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    Biconditional(AKnave, Not(AKnight)),
    Biconditional(BKnave, Not(BKnight))
)

p3= """
Puzzle 3
***********************
A says either "I am a knight." or "I am a knave.", but you don't know which.
B says "A said 'I am a knave'."
B says "C is a knave."
C says "A is a knight."
***********************"""

knowledge3 = And(
    Implication(AKnight, AKnight), 
    Implication(AKnave, Not(AKnave)),
    Implication(BKnight, And(AKnave, CKnave)),
    Implication(BKnave, Not(And(AKnave, CKnave))),
    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight)),

    Biconditional(AKnave, Not(AKnight)),
    Biconditional(BKnave, Not(BKnight)),
    Biconditional(CKnave, Not(CKnight))
)
 

def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        (p0, knowledge0),
        (p1, knowledge1),
        (p2, knowledge2),
        (p3, knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        # print(knowledge)
        print("Solution:")
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
