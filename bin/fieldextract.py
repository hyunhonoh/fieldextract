#!/bin/python
#-*- coding: utf-8 -*-
import splunk.Intersplunk, splunk.util
import itertools

def fieldextract(results, settings):

    try:
        fields, argvals = splunk.Intersplunk.getKeywordsAndOptions()
        keyfield      = argvals.get("keyfield",True)
        resultsplit=[]
        for r in results:
            result=[]
            if r[keyfield].split() == 1:
                keyfieldmax=1
            else:
                keyfieldmax=len(r[keyfield].split())
            for f in fields:
                if f in r:
                    # multivalue 필드인지 확인 후 단일값 필드이면 중복으로 저장
                    if len(r[f].split())==1:
                        field = []
                        for i in range(keyfieldmax):
                            field.append(r[f])
                        r[f]=field
                    else:
                        r[f]=r[f].split()
                    result.append(r[f])
            # 모아서 나눠주는 형식
            resultsplit.append([splunk.util.OrderedDict(zip(fields, a)) for a in zip(*result)])
        # 결과 분리 출력 https://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python
        results = list(itertools.chain.from_iterable(resultsplit))
        # results = [item for sublist in resultsplit for item in sublist]
        splunk.Intersplunk.outputResults(results)
    except:
        import traceback
        stack =  traceback.format_exc()
        results = splunk.Intersplunk.generateErrorResults("Error : Traceback: " + str(stack))

results, dummyresults, settings = splunk.Intersplunk.getOrganizedResults()
results = fieldextract(results, settings)

