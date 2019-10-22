package aima.core.logic.fol.inference.api;

import aima.core.logic.fol.inference.InferenceResult;
import aima.core.logic.fol.inference.proof.Proof;
import aima.core.logic.fol.parsing.ast.Term;
import aima.core.logic.fol.parsing.ast.Variable;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Set;

public class AskResponse {

    private Boolean isTrue;
    private Boolean isPossiblyFalse;
    private List<AnswerProof> proofs;
    private Boolean success;
    private String message;

    public AskResponse() {

    }

    public AskResponse(InferenceResult inferenceResult) {
        isTrue = inferenceResult.isTrue();
        isPossiblyFalse = inferenceResult.isPossiblyFalse();
        proofs = new ArrayList<AnswerProof>();

        for (Proof proof : inferenceResult.getProofs()) {

            AnswerProof answerProof = new AnswerProof();
            List<VariableBinding> bindings = new ArrayList<VariableBinding>();

            Map<Variable, Term> answerBindings = proof.getAnswerBindings();

            Set<Variable> keySet = answerBindings.keySet();

            for (Variable variable : keySet) {

                Term value = answerBindings.get(variable);

                if(value != null) {
                    VariableBinding binding = new VariableBinding();
                    binding.setName(variable.getValue());
                    binding.setValue(value.toString());
                    bindings.add(binding);
                }

            }

            answerProof.setVariableBindings(bindings);

            // TODO : This is a workaround for erroneous proofs coming back with no variable bindings.
            if(answerProof.getVariableBindings().size() > 0 ){
                proofs.add(answerProof);
            }
        }
    }

    public Boolean getIsTrue() {
        return isTrue;
    }

    public Boolean getIsPossiblyFalse() {
        return isPossiblyFalse;
    }

    public List<AnswerProof> getProofs() {
        return proofs;
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