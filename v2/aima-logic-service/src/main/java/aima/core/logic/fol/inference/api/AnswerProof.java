package aima.core.logic.fol.inference.api;

import java.util.List;

public class AnswerProof {
    
    private List<VariableBinding> variableBindings;

    public void setVariableBindings(List<VariableBinding> bindings) {        
        variableBindings = bindings;
    }

    public List<VariableBinding> getVariableBindings() {        
        return variableBindings;
    }

}