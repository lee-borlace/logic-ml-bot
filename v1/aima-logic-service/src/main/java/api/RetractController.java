package api;

import java.util.List;
import java.util.Set;

import org.springframework.web.bind.annotation.*;

import aima.core.logic.fol.domain.FOLDomain;
import aima.core.logic.fol.inference.api.*;
import aima.core.logic.fol.kb.FOLKnowledgeBase;

@RestController
@RequestMapping(path = "/api/retract")
public class RetractController {

    @RequestMapping(method = RequestMethod.POST)
    public TellResponse retract(@RequestBody TellRequest request) {

        try {

            Boolean needToUpdateDomain = false;

            FOLKnowledgeBase kb = MasterKnowledgeBase.getKb();
            FOLDomain domain = MasterDomain.getDomain();

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

            List<String> sentences = request.getSentences();
          
            if(sentences != null && sentences.size() > 0) {
                for (String sentence : sentences) {
                    kb.retract(sentence);
                }

                MasterKnowledgeBase.setKb(kb);
            }

            TellResponse response = new TellResponse();
            response.setSuccess(true);
            response.setMessage(null);
            return response;
        }
        catch(Exception ex) {
            TellResponse response = new TellResponse();
            response.setSuccess(false);
            response.setMessage(ex.getMessage());
            return response;
        }
    }
}
