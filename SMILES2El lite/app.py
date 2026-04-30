import streamlit as st
from rdkit import Chem
from rdkit.Chem import Descriptors
# 🚨 暂时不引入 Draw，因为它在云端环境非常不稳定
import pandas as pd

st.set_page_config(page_title="SMILES2EL", page_icon="🧪", layout="wide")

st.sidebar.title("🧬 SMILES2EL")
st.sidebar.write("开发者: Ellison")

input_text = st.sidebar.text_area("输入 SMILES (每行一个):", "CC(=O)OC1=CC=CC=C1C(=O)O")

st.title("🧪 SMILES2EL 药学数据中心")

if st.sidebar.button("分析数据"):
    smiles_list = [s.strip() for s in input_text.split('\n') if s.strip()]
    results = []
    
    for i, smy in enumerate(smiles_list):
        mol = Chem.MolFromSmiles(smy)
        if mol:
            # 只计算数值，不画图
            results.append({
                "编号": i + 1,
                "SMILES": smy,
                "分子量": round(Descriptors.MolWt(mol), 2),
                "LogP": round(Descriptors.MolLogP(mol), 2),
                "TPSA": round(Descriptors.TPSA(mol), 2)
            })
    
    if results:
        df = pd.DataFrame(results)
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 下载 CSV 数据", csv, "results.csv", "text/csv")
        st.success("数据计算成功！")