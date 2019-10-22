package aima.core.logic.fol.inference.api;

import java.util.List;

public class TellRequest {
    
    private List<String> sentences;
    private List<String> predicates;
    private List<String> functions;
    private List<String> constants;

	public List<String> getSentences() {
		return sentences;
	}
	
	public void setSentences(List<String> sentences) {
		this.sentences = sentences;
	}

	public List<String> getConstants() {
		return constants;
	}

	public void setConstants(List<String> constants) {
		this.constants = constants;
	}

	public List<String> getFunctions() {
		return functions;
	}
	
	public void setFunctions(List<String> functions) {
		this.functions = functions;
	}

	public List<String> getPredicates() {
		return predicates;
	}
	
	public void setPredicates(List<String> predicates) {
		this.predicates = predicates;
	}

}