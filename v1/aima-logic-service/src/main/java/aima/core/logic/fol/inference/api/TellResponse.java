package aima.core.logic.fol.inference.api;

import aima.core.logic.fol.inference.InferenceResult;
import aima.core.logic.fol.inference.proof.Proof;
import aima.core.logic.fol.parsing.ast.Term;
import aima.core.logic.fol.parsing.ast.Variable;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class TellResponse {
    
    private Boolean success;
    private String message;

    public TellResponse() {
        
    }

    public Boolean getSuccess() {        
        return success;
    }

    public void setSuccess(Boolean success) {        
        this.success = success;
    }

    public String getMessage() {        
        return message;
    }

    public void setMessage(String message) {        
        this.message = message;
    }

   

    

}