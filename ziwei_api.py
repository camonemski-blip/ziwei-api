# -*- coding: utf-8 -*-
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn

app = FastAPI(title="紫微斗數推理引擎")

# ========== 命盤資料 ==========
benming = {
    "命宮": {
        "干支": "辛丑", "主星": [("武曲", "廟"), ("貪狼", "廟")], "自化": [], "輔星": [], "小星": ["蜚廉"],
        "大限": "5~14"
    },
    "兄弟宮": {
        "干支": "庚子", "主星": [("天同", "旺", "↓忌"), ("太陰", "廟", "↓科")], "自化": ["天同忌(離心)", "太陰科(離心)"],
        "輔星": [], "小星": ["天才","天壽","臺輔","解神","天空","咸池"], "大限": "115~124"
    },
    "夫妻宮": {
        "干支": "己亥", "主星": [("天府", "得")], "自化": [], "輔星": [], "小星": ["鳳閣","年解"], "大限": "105~114"
    },
    "子女宮": {
        "干支": "戊戌", "主星": [], "自化": [], "輔星": [("文曲", "陷", "生年科"), ("擎羊", "廟")],
        "小星": ["天喜","八座","恩光","寡宿"], "大限": "95~104"
    },
    "財帛宮": {
        "干支": "丁酉", "主星": [("廉貞", "平"), ("破軍", "陷")], "自化": [], "輔星": [("左輔", "陷"), ("祿存", "廟")],
        "小星": ["天官","破碎"], "大限": "85~94"
    },
    "疾厄宮": {
        "干支": "丙申", "主星": [], "自化": [], "輔星": [("陀羅", "陷")], "小星": ["天使","封誥","天巫","劫煞","天德"],
        "大限": "75~84"
    },
    "遷移宮": {
        "干支": "乙未", "主星": [], "自化": [], "輔星": [], "小星": ["天哭","華蓋"], "大限": "65~74"
    },
    "交友宮": {
        "干支": "甲午", "主星": [], "自化": [], "輔星": [("天鉞", "旺")], "小星": ["天姚","天傷","天廚","龍德"],
        "大限": "55~64"
    },
    "官祿宮": {
        "干支": "癸巳", "主星": [("紫微", "旺"), ("七殺", "平")], "自化": [], "輔星": [("右弼", "平"), ("地劫", "不"), ("地空", "廟"), ("天馬", "平")],
        "小星": ["天福","截空","天虛"], "大限": "45~54"
    },
    "田宅宮": {
        "干支": "壬辰", "主星": [("天機", "利", "↑忌"), ("天梁", "廟", "↓祿")], "自化": ["天機忌(向心)", "天梁祿(離心)"],
        "輔星": [("文昌", "得", "生年忌"), ("鈴星", "陷")],
        "小星": ["紅鸞","三臺","天貴","截空","陰煞","大耗","月德"], "大限": "35~44"
    },
    "福德宮": {
        "干支": "辛卯", "主星": [("天相", "陷")], "自化": [], "輔星": [("火星", "利")], "小星": ["龍池","天月","旬空"],
        "大限": "25~34", "來因宮": True
    },
    "父母宮": {
        "干支": "庚寅", "主星": [("太陽", "旺", "生年權", "↓祿"), ("巨門", "廟", "生年祿")], "自化": ["太陽祿(離心)"],
        "輔星": [("天魁", "旺")], "小星": ["天刑","旬空","孤辰"], "大限": "15~24"
    }
}
# ========== 十天干四化表 ==========
si_hua_table = {
    "甲": {"祿": "廉貞", "權": "破軍", "科": "武曲", "忌": "太陽"},
    "乙": {"祿": "天機", "權": "天梁", "科": "紫微", "忌": "太陰"},
    "丙": {"祿": "天同", "權": "天機", "科": "文昌", "忌": "廉貞"},
    "丁": {"祿": "太陰", "權": "天同", "科": "天機", "忌": "巨門"},
    "戊": {"祿": "貪狼", "權": "太陰", "科": "右弼", "忌": "天機"},
    "己": {"祿": "武曲", "權": "貪狼", "科": "天梁", "忌": "文曲"},
    "庚": {"祿": "太陽", "權": "武曲", "科": "太陰", "忌": "天同"},
    "辛": {"祿": "巨門", "權": "太陽", "科": "文曲", "忌": "文昌"},
    "壬": {"祿": "天梁", "權": "紫微", "科": "左輔", "忌": "武曲"},
    "癸": {"祿": "破軍", "權": "巨門", "科": "太陰", "忌": "貪狼"}
}

palace_order = ["命宮", "兄弟宮", "夫妻宮", "子女宮", "財帛宮", "疾厄宮", "遷移宮", "交友宮", "官祿宮", "田宅宮", "福德宮", "父母宮"]

def find_star_location(star_name, benming):
    for palace, info in benming.items():
        for s in info["主星"]:
            if s[0] == star_name:
                return palace
        if info.get("輔星"):
            for aux in info["輔星"]:
                if aux[0] == star_name:
                    return palace
    return None

def get_daxian_by_age(age, benming):
    for palace, info in benming.items():
        if "大限" not in info:
            continue
        range_str = info["大限"]
        if "~" not in range_str:
            continue
        start, end = map(int, range_str.split("~"))
        if start <= age <= end:
            return palace
    return None

def get_daxian_map(ming_palace):
    idx = palace_order.index(ming_palace)
    mapping = {}
    for i, p in enumerate(palace_order):
        mapping[p] = palace_order[(idx + i) % 12]
    return mapping

def feixing(palace_name, benming, si_hua_table):
    gan = benming[palace_name]["干支"][0]
    si_hua = si_hua_table.get(gan, {})
    result = {}
    for t, star in si_hua.items():
        locate = find_star_location(star, benming)
        result[t] = {"星": star, "落宮": locate}
    return result

class AgeRequest(BaseModel):
    age: int

class AnalysisResponse(BaseModel):
    age: int
    daxian_ming: str
    daxian_guanlu: str
    daxian_caibo: str
    daxian_fuqi: str
    ganlu_gan: str
    sihua: Dict[str, Any]
    fei_ji_luo_is_fuqi: bool

@app.post("/analyze")
def analyze(request: AgeRequest):
    age = request.age
    daxian_ming = get_daxian_by_age(age, benming)
    if not daxian_ming:
        raise HTTPException(status_code=404, detail=f"找不到年齡 {age} 的大限")
    
    daxian_map = get_daxian_map(daxian_ming)
    daxian_guanlu = daxian_map["官祿宮"]
    daxian_caibo = daxian_map["財帛宮"]
    daxian_fuqi = daxian_map["夫妻宮"]
    
    ganlu_gan = benming[daxian_guanlu]["干支"][0]
    fei = feixing(daxian_guanlu, benming, si_hua_table)
    
    fei_ji_luo_is_fuqi = False
    if "忌" in fei:
        fei_ji_luo_is_fuqi = (fei["忌"]["落宮"] == daxian_fuqi)
    
    return AnalysisResponse(
        age=age,
        daxian_ming=daxian_ming,
        daxian_guanlu=daxian_guanlu,
        daxian_caibo=daxian_caibo,
        daxian_fuqi=daxian_fuqi,
        ganlu_gan=ganlu_gan,
        sihua=fei,
        fei_ji_luo_is_fuqi=fei_ji_luo_is_fuqi
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)