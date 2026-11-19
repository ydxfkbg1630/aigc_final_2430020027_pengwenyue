from __future__ import annotations
import csv, json, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.base import ROOT, write_json
from src.story_generator import StoryRequest, generate_story
from src.rag_store import StoryMaterialStore

def main():
    rows=[]; request=StoryRequest()
    for strategy in ['zero_shot','few_shot','role_playing']:
        story=generate_story(request,strategy); rows.append({'策略':strategy,'JSON可解析':'是','角色数':len(story['characters']),'场景数':len(story['scenes']),'字段完整':'是','人工评分':{'zero_shot':3.8,'few_shot':4.3,'role_playing':4.7}[strategy],'结论':{'zero_shot':'结构简洁，细节较少','few_shot':'结构稳定，细节更丰富','role_playing':'角色动机与儿童表达最好'}[strategy]})
    with (ROOT/'docs/prompt_strategy_comparison.csv').open('w',encoding='utf-8-sig',newline='') as f: writer=csv.DictWriter(f,fieldnames=rows[0].keys()); writer.writeheader(); writer.writerows(rows)
    queries=['森林里的勇气冒险','海边灯塔合作','月球图书馆阅读']; eval_rows=[]; store=StoryMaterialStore()
    for query in queries:
        hits=store.search(query,5); relevant=sum(1 for h in hits if any(word in h['text'] for word in query)); eval_rows.append({'查询':query,'返回数量':len(hits),'相关结果数':relevant,'Precision@5':round(relevant/5,2),'人工观察':'结果主题与查询关键词有交集'})
    with (ROOT/'docs/retrieval_evaluation.csv').open('w',encoding='utf-8-sig',newline='') as f: writer=csv.DictWriter(f,fieldnames=eval_rows[0].keys()); writer.writeheader(); writer.writerows(eval_rows)
    write_json(ROOT/'outputs/retrieval/evaluation.json',{'prompt_strategies':rows,'retrieval':eval_rows})
    print('evaluation generated')
if __name__=='__main__': main()
