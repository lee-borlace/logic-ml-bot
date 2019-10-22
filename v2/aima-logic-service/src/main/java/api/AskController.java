package api;

import java.util.List;
import java.util.Set;

import org.springframework.web.bind.annotation.*;

import aima.core.logic.common.Parser;
import aima.core.logic.fol.domain.FOLDomain;
import aima.core.logic.fol.inference.InferenceResult;
import aima.core.logic.fol.inference.api.*;
import aima.core.logic.fol.kb.FOLKnowledgeBase;
import aima.core.logic.fol.parsing.*;
import aima.core.logic.fol.parsing.ast.Sentence;


@RestController
@RequestMapping(path = "/api/ask")
public class AskController {

    @RequestMapping(method = RequestMethod.POST)
    public AskResponse ask(@RequestBody AskRequest request) {
        try {
            FOLKnowledgeBase kb = MasterKnowledgeBase.getKb();
            FOLDomain domain = MasterDomain.getDomain();
            Boolean needToUpdateDomain = false;

            List<String> newPredicates = request.getPredicates();
            if(newPredicates != null && newPredicates.size() > 0){
                needToUpdateDomain = true;
                Set<String> existingPredicates = domain.getPredicates();
                for (String item : newPredicates) {
                    if(!existingPredicates.contains(item)){
                        existingPredicates.add(item);
                    }
                }
            }

            List<String> newConstants = request.getConstants();
            if(newConstants != null && newConstants.size() > 0){
                needToUpdateDomain = true;
                Set<String> existingConstants = domain.getConstants();
                for (String item : newConstants) {
                    if(!existingConstants.contains(item)){
                        existingConstants.add(item);
                    }
                }
            }

            List<String> newFunctions = request.getFunctions();
            if(newFunctions != null && newFunctions.size() > 0){
                needToUpdateDomain = true;
                Set<String> existingFunctions = domain.getFunctions();
                for (String item : newFunctions) {
                    if(!existingFunctions.contains(item)){
                        existingFunctions.add(item);
                    }
                }
            }

            if(needToUpdateDomain) {
                MasterDomain.setDomain(domain);
                kb.setDomain(domain);
            }

            FOLParser parser = kb.getParser();
            Sentence sentence = parser.parse(request.getQuery());
            InferenceResult inferenceResult = kb.ask(sentence);
            
            AskResponse response = new AskResponse(inferenceResult);
            response.setSuccess(true);
            response.setMessage(null);

            return response;
        } catch (Exception ex) {
            AskResponse response = new AskResponse();
            response.setSuccess(false);
            response.setMessage(ex.toString());
            return response;
        }
    }
}
