package aima.core.logic.fol.inference.api;

import java.util.List;

public class AskRequest {
    
    private String query;
    private String value;
    private List<String> predicates;
    private List<String> functions;
    private List<String> constants;

    public void setQuery(String query) {        
        this.query = query;
    }

    public String getQuery() {        
        return query;
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