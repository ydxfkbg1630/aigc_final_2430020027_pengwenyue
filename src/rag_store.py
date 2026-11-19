from __future__ import annotations
import math, re
from pathlib import Path
from .base import ROOT, read_json, stable_seed, write_json

STOPWORDS = set("的 了 和 在 是 一个 一起 我们 他们 这 那 到 把 请 让 有 会 里 从 与 及".split())
def tokenize(text: str) -> list[str]:
    chunks = re.findall(r"[\u4e00-\u9fff]|[A-Za-z0-9]+", text.lower())
    return [item for item in chunks if item not in STOPWORDS]
def text_vector(text: str, vocabulary: list[str]) -> list[float]:
    tokens = tokenize(text); total = max(1, len(tokens)); return [tokens.count(term) / total for term in vocabulary]
def cosine(left: list[float], right: list[float]) -> float:
    dot = sum(a*b for a,b in zip(left,right)); la=math.sqrt(sum(a*a for a in left)); lb=math.sqrt(sum(b*b for b in right)); return dot/(la*lb) if la and lb else 0.0
class StoryMaterialStore:
    def __init__(self, root: Path | None = None):
        self.root = root or ROOT / "data"; self.records = self._load_records(); self.vocab = sorted(set(term for record in self.records for term in tokenize(record["text"])))
        self.vectors = [text_vector(record["text"], self.vocab) for record in self.records]
    def _load_records(self):
        records=[]
        for path in sorted((self.root / "templates").glob("*.json")):
            item=read_json(path); records.append({"id": path.stem, "type":"template", "text": item["title"]+" "+item["description"], "payload":item})
        for path in sorted((self.root / "characters").glob("*.json")):
            item=read_json(path); records.append({"id": path.stem, "type":"character", "text": item["name"]+" "+item["traits"]+" "+item["appearance"], "payload":item})
        for path in sorted((self.root / "scenes").glob("*.json")):
            item=read_json(path); records.append({"id": path.stem, "type":"scene", "text": item["name"]+" "+item["description"], "payload":item})
        return records
    def search(self, query: str, top_k: int = 8) -> list[dict]:
        vector=text_vector(query,self.vocab); ranked=sorted(((cosine(vector,v),record) for v,record in zip(self.vectors,self.records)), key=lambda pair: pair[0], reverse=True)
        return [{"score":round(score,4), **record} for score,record in ranked[:top_k]]
    def recommend(self, query: str) -> dict:
        hits=self.search(query, 8); return {"query":query, "template_ids":[x["id"] for x in hits if x["type"]=="template"][:3], "character_candidates":[x["id"] for x in hits if x["type"]=="character"][:3], "scene_candidates":[x["id"] for x in hits if x["type"]=="scene"][:3], "image_ids":[f"scene_{i:02d}" for i in range(1,4)], "sound_ids":["forest_night","magic_chime","water_ripple"], "generation_hints":[x["payload"].get("description","") for x in hits[:3]], "results":hits}
if __name__ == "__main__":
    store=StoryMaterialStore(); write_json(ROOT/"outputs/retrieval/recommendation.json", store.recommend("太空森林里的勇气冒险")); print(len(store.records))
