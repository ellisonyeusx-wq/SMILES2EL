import streamlit as st
from rdkit import Chem
from rdkit.Chem import Descriptors, Draw
import pandas as pd
import base64

# --- 1. 页面基本配置 ---
st.set_page_config(
    page_title="SMILES2EL 分子分析中心", 
    page_icon="🧪", 
    layout="wide"
)

# --- 2. 侧边栏设计 ---
st.sidebar.title("🧬 SMILES2EL")
st.sidebar.markdown(f"**开发者:** Ellison")
st.sidebar.write("---")
st.sidebar.subheader("📥 输入区域")

# 默认提供几个药学常用的例子：阿司匹林、咖啡因、姜黄素
default_smiles = (
    "CC(=O)OC1=CC=CC=C1C(=O)O\n"
    "CN1C=NC2=C1C(=O)N(C(=O)N2C)C\n"
    "COC1=C(C=CC(=C1)/C=C/C(=O)CC(=O)/C=C/C2=CC(=C(C=C2)OC)O)O"
)

input_text = st.sidebar.text_area(
    "请粘贴 SMILES 分子式 (每行一个):", 
    value=default_smiles, 
    height=200
)

analyze_btn = st.sidebar.button("🚀 执行批量分析")

# --- 3. 主界面显示 ---
st.title("🧪 SMILES2EL: 从结构到数据的转化中心")
st.markdown("""
本项目旨在帮助药学生和研究人员快速提取分子描述符。
这些数据可直接用于 **QSAR 建模**、**药物活性预测** 以及 **AI 筛选**。
""")

if analyze_btn:
    smiles_list = [s.strip() for s in input_text.strip().split('\n') if s.strip()]
    results = []
    
    if not smiles_list:
        st.error("请输入至少一个有效的 SMILES 字符串。")
    else:
        st.subheader("1️⃣ 分子结构可视化")
        # 自动计算列数，最多4列
        cols = st.columns(4)
        
        valid_mols = []
        for i, smy in enumerate(smiles_list):
            mol = Chem.MolFromSmiles(smy)
            if mol:
                # 绘制分子图
                img = Draw.MolToImage(mol, size=(300, 300))
                with cols[i % 4]:
                    st.image(img, caption=f"分子 {i+1}", use_container_width=True)
                
                # 计算描述符 (Descriptors)
                desc_data = {
                    "编号": i + 1,
                    "SMILES": smy,
                    "分子量 (MW)": round(Descriptors.MolWt(mol), 2),
                    "脂溶性 (LogP)": round(Descriptors.MolLogP(mol), 2),
                    "极性表面积 (TPSA)": round(Descriptors.TPSA(mol), 2),
                    "氢键供体 (HBD)": Descriptors.NumHDonors(mol),
                    "氢键受体 (HBA)": Descriptors.NumHAcceptors(mol),
                    "可旋转键数量": Descriptors.NumRotatableBonds(mol),
                    "摩尔折射率": round(Descriptors.MolMR(mol), 2)
                }
                results.append(desc_data)
                valid_mols.append(mol)
            else:
                st.sidebar.warning(f"⚠️ 无法解析第 {i+1} 行的 SMILES，已跳过。")

        # --- 4. 数据报表展示 ---
        if results:
            st.write("---")
            st.subheader("2️⃣ 描述符数据报表 (用于 AI 建模)")
            df = pd.DataFrame(results)
            
            # 在网页上显示表格
            st.dataframe(df, use_container_width=True)
            
            # --- 5. 下载功能 (修正中文乱码) ---
            # 使用 utf-8-sig 编码，确保 Excel 打开不乱码
            csv = df.to_csv(index=False).encode('utf-8-sig')
            
            st.download_button(
                label="📥 下载 CSV 分析数据",
                data=csv,
                file_name='SMILES2EL_Result.csv',
                mime='text/csv',
            )
            st.success(f"✅ 成功分析 {len(results)} 个分子！数据已就绪。")
        else:
            st.error("没有找到有效的分子数据。")

else:
    st.info("💡 提示：在左侧侧边栏输入分子的 SMILES 代码，然后点击“执行批量分析”按钮开始。")
    st.image("https://pubchem.ncbi.nlm.nih.gov/image/imgsrv.fcgi?cid=247&t=l", width=200, caption="示例：Aspirin 结构")

# --- 6. 页脚信息 ---
st.markdown("---")
st.caption("SMILES2EL v2.1 | Powered by RDKit & Streamlit | Created for Pharmacy Research")