# -*- coding: utf-8 -*-
from logic_service import LogicService
LOGIC_SERVICE_BASE_URL = "http://localhost:8081"
logicService = LogicService(LOGIC_SERVICE_BASE_URL)

sentences = [
"Det(Const_icxz_0,Your,Prp)",
"Poss(Const_icxz_0,Const_icxz_1)",
"Noun(Const_icxz_1,Dog,Nn)",
"Nsubj(Const_icxz_1,Const_icxz_2)",
"Verb(Const_icxz_2,Chase,Vbd)",
"Pron(Const_icxz_3,Me,Prp)",
"Dobj(Const_icxz_3,Const_icxz_2)"]

logicService.tell(sentences)

result = logicService.ask("Dobj(Const_icxz_3,x)")

print(result)