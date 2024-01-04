import pandas as pd
import streamlit as st
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib import font_manager as fm
from datetime import datetime

pd.options.display.max_colwidth = 2000
pd.set_option('mode.chained_assignment', None)

font_path = 'SKYBORI.ttf'
fm.fontManager.addfont(font_path)
font_name = fm.FontProperties(fname=font_path).get_name()
plt.rcParams['axes.unicode_minus'] = False
matplotlib.rc("font", family=font_name)

st.set_page_config(layout="wide")

def draw_table(df_detail_title, index_type):

    dict_type = {
        "대학구분" : 7,
        "학년구분" : 14,
        "학과구분" : 10
    }

    dict_type_for_list = {
        "대학구분" : list_type_college,
        "학년구분" : list_type_year,
        "학과구분" : list_type_deparment
    }

    list_type_index = [None] * dict_type[index_type]

    for i, value in enumerate(df_detail_title[index_type][df_detail_title.index].values[0]):
        list_type_index[int(value)] = 1

    axs = plt.figure(figsize=(14, 1), layout="constrained").subplots(1, dict_type[index_type])

    for i, ax in enumerate(axs):
        ax.set(title= dict_type_for_list[index_type][i])
        if list_type_index[i] is not None:
            ax.add_patch(Rectangle((0, 0), 2, 2, fill=True))
        ax.axis('equal')
        ax.axis('off')    

    return plt

df = pd.read_csv("./한국장학재단_학자금지원정보(대학생)_20231222.csv", encoding='CP949')

df["기준날짜"] = pd.to_datetime(datetime.now().strftime("%Y-%m-%d"))
df["모집종료일"] = pd.to_datetime(df["모집종료일"])
df["남은 일자"] = (df["모집종료일"] - df["기준날짜"]).dt.days
df["모집일"] = df["모집시작일"].astype(str) + " ~ " + df["모집종료일"].astype(str)

df_part = df[df["남은 일자"] > 0]\
    .drop(["번호", "모집시작일", "모집종료일", "기준날짜"], axis = 1)\
    .sort_values(by = ["남은 일자", "상품명"]).reset_index()\
    .drop(["index"], axis = 1)
df_part.insert(0, "선택", False)

df_part["대학구분"] = df_part["대학구분"].str.replace("전문대(2~3년제)", "0")
df_part["대학구분"] = df_part["대학구분"].str.replace("4년제(5~6년제포함)", "1")
df_part["대학구분"] = df_part["대학구분"].str.replace("기술대학", "2")
df_part["대학구분"] = df_part["대학구분"].str.replace("해외대학", "3")
df_part["대학구분"] = df_part["대학구분"].str.replace("일반대학원", "4")
df_part["대학구분"] = df_part["대학구분"].str.replace("전문대학원", "5")
df_part["대학구분"] = df_part["대학구분"].str.replace("해당없음", "6")
df_part["대학구분"] = df_part["대학구분"].str.split("/").apply(lambda x: sorted(x))
list_type_college = ["전문대(2~3년제)", "4년제(5~6년제포함)", "기술대학", "해외대학", "일반대학원", "전문대학원", "해당없음"]

df_part["학년구분"] = df_part["학년구분"].str.replace("대학신입생", "0")
df_part["학년구분"] = df_part["학년구분"].str.replace("대학2학기", "1")
df_part["학년구분"] = df_part["학년구분"].str.replace("대학3학기", "2")
df_part["학년구분"] = df_part["학년구분"].str.replace("대학4학기", "3")
df_part["학년구분"] = df_part["학년구분"].str.replace("대학5학기", "4")
df_part["학년구분"] = df_part["학년구분"].str.replace("대학6학기", "5")
df_part["학년구분"] = df_part["학년구분"].str.replace("대학7학기", "6")
df_part["학년구분"] = df_part["학년구분"].str.replace("대학8학기이상", "7")
df_part["학년구분"] = df_part["학년구분"].str.replace("석사신입생\(1학기\)", "8", regex=True)
df_part["학년구분"] = df_part["학년구분"].str.replace("석사2학기이상", "9")
df_part["학년구분"] = df_part["학년구분"].str.replace("박사과정", "10")
df_part["학년구분"] = df_part["학년구분"].str.replace("연령제한", "11")
df_part["학년구분"] = df_part["학년구분"].str.replace("제한없음", "12")
df_part["학년구분"] = df_part["학년구분"].str.replace("해당없음", "13")
df_part["학년구분"] = df_part["학년구분"].str.split("/").apply(lambda x: sorted(x))
list_type_year = ["대학신입생", "대학2학기", "대학3학기", "대학4학기", "대학5학기", "대학6학기", "대학7학기", "대학8학기이상", "석사신입생(1학기)", "석사2학기이상", "박사과정", "연령제한", "제한없음", "해당없음"]

df_part["학과구분"] = df_part["학과구분"].str.replace("공학계열", "0")
df_part["학과구분"] = df_part["학과구분"].str.replace("교육계열", "1")
df_part["학과구분"] = df_part["학과구분"].str.replace("사회계열", "2")
df_part["학과구분"] = df_part["학과구분"].str.replace("예체능계열", "3")
df_part["학과구분"] = df_part["학과구분"].str.replace("의약계열", "4")
df_part["학과구분"] = df_part["학과구분"].str.replace("인문계열", "5")
df_part["학과구분"] = df_part["학과구분"].str.replace("자연계열", "6")
df_part["학과구분"] = df_part["학과구분"].str.replace("특정학과", "7")
df_part["학과구분"] = df_part["학과구분"].str.replace("제한없음", "8")
df_part["학과구분"] = df_part["학과구분"].str.replace("해당없음", "9")
df_part["학과구분"] = df_part["학과구분"].str.split("/").apply(lambda x: sorted(x))
list_type_deparment = ["공학계열", "교육계열", "사회계열", "예체능계열", "의약계열", "인문계열", "자연계열", "특정학과", "제한없음", "해당없음"]

st.title("한국장학재단_학자금지원정보(대학생)")
st.header("데이터 기준 : 2023년 12월 29일 / " + "조회 기준 : " + datetime.now().strftime("%Y년 %m월 %d일"))
st.info("""이 데이터는 공공데이터포털(www.data.go.kr)에 공개된 한국장학재단 학자금지원정보(대학생)을
처리한 결과입니다.
        
데이터는 월 주기로 업데이트되며 해당 페이지의 데이터도 매월 1일에 업데이트할 예정입니다.

전국 지자체, 민간장학재단, 대학 등에서 대학생 및 대학원생을 대상으로 지원하는 학자금 정보
(운영기관, 상품명, 상품구분, 학자금 지원 유형, 신청대상, 신청기간, 지원금액, 지원인원 등)를 제공합니다.

오류나 추가 기능이 있으면, fermat39@naver.com로 알려주시면 수정 및 반영하겠습니다.
        
streamlit, pandas, matplotlib로 만든 소스코드는 

https://github.com/fermat39/data_with_me_001 에 공개하였습니다!

출처 : https://www.data.go.kr/data/15028252/fileData.do
""")

df_selections = st.data_editor(
    df_part[[ "선택", "모집일", "남은 일자", "상품구분", "상품명", "학자금유형구분", "운영기관구분", "운영기관명", "홈페이지주소"]],
    disabled= ["모집일", "남은 일자", "상품구분", "상품명", "학자금유형구분", "운영기관구분", "운영기관명", "홈페이지주소"],
    hide_index=True, 
    column_config={
        "홈페이지주소": st.column_config.LinkColumn(),
        "선택": st.column_config.CheckboxColumn(required=True)
    }
)

st.warning("""선택을 체크하면 아래에 자세한 내용이 보여집니다!
""")

st.divider()

for i, name in enumerate(df_selections[df_selections["선택"]]["상품명"].unique()):    
    st.header(str(len(df_selections[df_selections["선택"]]["상품명"].unique())) + "개 선택 중 " + str(i + 1) + "번째")
    df_detail = df_part[df_part["상품명"] == name]

    st.header(df_detail["상품명"].to_string(index = False))

    st.subheader("대학구분")
    st.pyplot(draw_table(df_detail, "대학구분"))

    st.subheader("학년구분")
    st.pyplot(draw_table(df_detail, "학년구분"))

    st.subheader("학과구분")
    st.pyplot(draw_table(df_detail, "학과구분"))

    st.subheader("상세내용")
    detail_content = \
        "성적기준 상세내용 : " + df_detail["성적기준 상세내용"].to_string(index = False) + "\n" + \
        "소득기준 상세내용 : " + df_detail["소득기준 상세내용"].to_string(index = False) + "\n" + \
        "지원내역 상세내용 : " + df_detail["지원내역 상세내용"].to_string(index = False) + "\n" + \
        "특정자격 상세내용 : " + df_detail["특정자격 상세내용"].to_string(index = False) + "\n" + \
        "지역거주여부 상세내용 : " + df_detail["지역거주여부 상세내용"].to_string(index = False) + "\n" + \
        "선발방법 상세내용 : " + df_detail["선발방법 상세내용"].to_string(index = False) + "\n" + \
        "선발인원 상세내용 : " + df_detail["선발인원 상세내용"].to_string(index = False) + "\n" + \
        "자격제한 상세내용 : " + df_detail["자격제한 상세내용"].to_string(index = False) + "\n" + \
        "추천필요여부 상세내용 : " + df_detail["추천필요여부 상세내용"].to_string(index = False) + "\n" + \
        "제출서류 상세내용 : " + df_detail["제출서류 상세내용"].to_string(index = False) + "\n"                        
    st.text(detail_content)    

    st.divider()
