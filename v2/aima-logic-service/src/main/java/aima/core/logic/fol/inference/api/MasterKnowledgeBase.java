package aima.core.logic.fol.inference.api;

import aima.core.logic.fol.kb.FOLKnowledgeBase;

public class MasterKnowledgeBase {

    private static FOLKnowledgeBase kb;

    public static FOLKnowledgeBase getKb() {        
        if(kb == null) {

            kb = new FOLKnowledgeBase(MasterDomain.getDomain());
    
            kb.tell("Subtype_Pred(Cat,Mammal)");
            kb.tell("Subtype_Pred(Dog,Mammal)");
            kb.tell("Subtype_Pred(Mammal,Animal)");

            // If something is yellow, plastic and bright, then it's ugly
            kb.tell("((AdjInstance(a,y,Yellow) AND AdjInstance(b,y,Plastic) AND AdjInstance(c,y,Bright)) => AdjInstance(Irrelevant_ID,y,Ugly))");

            // Things which are male.
            // kb.tell("((Instance_Pred(x,Male) OR Instance_Pred(x,Boy) OR Instance_Pred(x,Man) OR Instance_Pred(x,Guy) OR Instance_Pred(x,Bloke) OR Instance_Pred(x,Gentleman)) => Gender_Pred(x,Male))");
            kb.tell("((Instance_Pred(x,Male)) => Gender_Pred(x,Male))");
            kb.tell("((Instance_Pred(x,Boy)) => Gender_Pred(x,Male))");
            kb.tell("((Instance_Pred(x,Man)) => Gender_Pred(x,Male))");
            kb.tell("((Instance_Pred(x,Guy)) => Gender_Pred(x,Male))");
            kb.tell("((Instance_Pred(x,Dude)) => Gender_Pred(x,Male))");
            kb.tell("((Instance_Pred(x,Bloke)) => Gender_Pred(x,Male))");
            kb.tell("((Instance_Pred(x,Gentleman)) => Gender_Pred(x,Male))");

            // Things which are female.
            // kb.tell("((Instance_Pred(x,Female) OR Instance_Pred(x,Girl) OR Instance_Pred(x,Woman) OR Instance_Pred(x,Lady) OR Instance_Pred(x,Chick)) => Gender_Pred(x,Female))");
            kb.tell("((Instance_Pred(x,Female)) => Gender_Pred(x,Female))");
            kb.tell("((Instance_Pred(x,Girl)) => Gender_Pred(x,Female))");
            kb.tell("((Instance_Pred(x,Woman)) => Gender_Pred(x,Female))");
            kb.tell("((Instance_Pred(x,Lady)) => Gender_Pred(x,Female))");
            kb.tell("((Instance_Pred(x,Chick)) => Gender_Pred(x,Female))");

            kb.tell("((VerbInstance(x,Sleep,y) AND VerbTense(x,Present)) => AdjInstance(x,y,Asleep))");

            kb.tell("AdjInstance(A_12345,A_98765,Asleep)");
            kb.tell("AdjInstance(A_23456,A_87654,Asleep)");
            
            kb.retract("AdjInstance(A_23456,A_87654,Asleep)");
        }

        return kb;
    }

    public static void setKb(FOLKnowledgeBase kb) {
        MasterKnowledgeBase.kb = kb;
    }

}