package aima.core.logic.fol.inference.api;

import aima.core.logic.fol.domain.FOLDomain;

public class MasterDomain {

    private static FOLDomain domain;

    public static void setDomain(FOLDomain domain) {
        MasterDomain.domain = domain;
    }

    public static FOLDomain getDomain() {        
        if(domain == null) {
            
            domain = new FOLDomain();
        }

        
      
        domain.addConstant("Cat");
        domain.addConstant("Dog");
        domain.addConstant("Mammal");
        domain.addConstant("Animal");
        domain.addConstant("Yellow");
        domain.addConstant("Plastic");
        domain.addConstant("Bright");
        domain.addConstant("Ugly");
        domain.addConstant("Noun");
        domain.addConstant("Adjective");
        domain.addConstant("Verb");
        domain.addConstant("Past");
        domain.addConstant("Irrelevant_ID");
        domain.addConstant("Male");
        domain.addConstant("Female");

        domain.addConstant("Boy");
        domain.addConstant("Man");
        domain.addConstant("Guy");
        domain.addConstant("Dude");
        domain.addConstant("Bloke");
        domain.addConstant("Gentleman");
        domain.addConstant("Female");
        domain.addConstant("Girl");
        domain.addConstant("Woman");
        domain.addConstant("Lady");
        domain.addConstant("Chick");
        domain.addConstant("Sleep");
        domain.addConstant("Asleep");
        domain.addConstant("Present");

        domain.addConstant("A_12345");
        domain.addConstant("A_98765");
        domain.addConstant("A_23456");
        domain.addConstant("A_87654");
        
        domain.addPredicate("VerbInstance");
        domain.addPredicate("VerbTense");
        domain.addPredicate("AdjInstance");
        domain.addPredicate("Verb_Pred");
        domain.addPredicate("Adjective_Pred");
        domain.addPredicate("Subtype_Pred");
        domain.addPredicate("Instance_Pred");
        domain.addPredicate("Own_Pred");
        domain.addPredicate("CollectionInstance_Pred");

        domain.addPredicate("Gender_Pred");


        return domain;
    }

}