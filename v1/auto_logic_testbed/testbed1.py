# -*- coding: utf-8 -*-
INPUT = "Instance(Const1,Cilantro) AND Instance   (Const2,server)  AND  Verb(Const3,Say ,  Const1)  AND  VerbLink(Const3,  amidst2, Const2 )"
# INPUT = "Noun(Const_tdlg_1,a,Doggy,b,c,Broggy,Foggy,Blah,hrah,Nn)"
from logic_service import LogicService
LOGIC_SERVICE_BASE_URL = "http://localhost:8081"
logicService = LogicService(LOGIC_SERVICE_BASE_URL)
logicService.tell(INPUT)