# Transforming Conjunctions
## "I eat pizza and drink beer"

If two nodes are cc/conj under a verb, 

e.g. "I eat pizza and drink beer"
https://explosion.ai/demos/displacy?text=I%20eat%20pizza%20and%20drink%20beer&model=en_core_web_sm&cpu=0&cph=0

Pos_Pron(C0,I,Prp)
Dep_Nsubj(C0,C1)
Pos_Verb(C1,Eat,Vbp)
Pos_Noun(C2,Pizza,Nn)
Dep_Dobj(C2,C1)
Pos_Cconj(C3,And,Cc)
Dep_Cc(C3,C1)
Pos_Verb(C4,Drink,Vb)
Dep_Conj(C4,C1)
Pos_Noun(C5,Beer,Nn)
Dep_Dobj(C5,C4)

This should be transformed to 

(I eat pizza) AND (I drink beer)

Pos_Pron(C0,I,Prp)
Dep_Nsubj(C0,C1)

Pos_Verb(C1,Eat,Vbp)
Pos_Noun(C2,Pizza,Nn)
Dep_Dobj(C2,C1)

AND 

Pos_Verb(C4,Drink,Vb)
Pos_Noun(C5,Beer,Nn)
Dep_Dobj(C5,C4)

## "I drink water or beer"

Pos_Pron(C0,I,Prp)
Dep_Nsubj(C0,C1)

Pos_Verb(C1,Drink,Vbp)
Pos_Noun(C2,Water,Nn)
Dep_Dobj(C2,C1)

Pos_Cconj(C3,Or,Cc)
Dep_Cc(C3,C2)

Pos_Noun(C4,Beer,Nn)
Dep_Conj(C4,C2)

## A but B

Treat "but" as "and"

# Transforming Neg

"I drink water but not beer"

Pos_Pron(C0,I,Prp)
Dep_Nsubj(C0,C1)
Pos_Verb(C1,Drink,Vbp)
Pos_Noun(C2,Water,Nn)
Dep_Dobj(C2,C1)
Pos_Cconj(C3,But,Cc)
Dep_Cc(C3,C2)
Pos_Adv(C4,Not,Rb)
Dep_Neg(C4,C5)
Pos_Verb(C5,Beer,Vb)
Dep_Conj(C5,C2)

Looks like we might be able to just negate the matching verb

"I don't drink beer"

Pos_Pron(C0,I,Prp)
Dep_Nsubj(C0,C3)
Pos_Verb(C1,Do,Vbp)
Dep_Aux(C1,C3)
Pos_Adv(C2,Not,Rb)
Dep_Neg(C2,C3)
Pos_Verb(C3,Drink,Vb)
Pos_Noun(C4,Beer,Nn)
Dep_Dobj(C4,C3)