import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib import font_manager
import plotly.express as px
import plotly.graph_objects as go
import datetime

st.set_page_config(layout="wide")
st.title("📄 Visualization")
st.write("Upload your file and get visualized")


#่ส่วนของการ set ค่าเริ่มต้น
def open_file(path_data):
    data = pd.read_excel(path_data, sheet_name=None)
    head_data = list(data.keys())
    data_sheet_1 = data[head_data[0]].set_index('ลำดับ')  #กำหนด index 'ลำดับ'
    data_sheet_2 = data[head_data[1]]
    return data,data_sheet_1,data_sheet_2

def display_unique_items_with_else(column_data, label="รายการ", number=3, unit="unit"):
    unique_values = column_data.dropna().astype(str)
    value_counts = unique_values.value_counts()

    number_show = value_counts.head(number)
    others = value_counts.iloc[number:]

    total_number_column = column_data.count()
    col1, col2 = st.columns(2)

    number_front = number / 2
    count_loop = 0
    for val, count in number_show.items():
        text = f"""- <span style="color:pink;">{val}</span> : {count} {unit} 
                    <span style="color:skyblue;">({(count/total_number_column)*100:.2f}%)</span>"""
        if count_loop < number_front:
            with col1:
                st.markdown(text, unsafe_allow_html=True)
                count_loop += 1
        else:
            with col2:
                st.markdown(text, unsafe_allow_html=True)
                count_loop += 1

    if not others.empty:
        with st.expander("🔻 แสดงรายการอื่น ๆ (Else)"):
            for val, count in others.items():
                text = f"""- <span style="color:pink;">{val}</span> : {count} {unit} 
                            <span style="color:skyblue;">({(count/total_number_column)*100:.2f}%)</span>"""
                st.markdown(text, unsafe_allow_html=True)

def display_month_summary(month_series):
    gregorian_dates = []

    for date_str in month_series.dropna().astype(str):
        try:
            parts = date_str.split("-")
            if len(parts) == 3:
                year = int(parts[0]) - 543
                gregorian_dates.append(f"{year}-{parts[1]}-{parts[2]}")
        except:
            continue

    # แปลงเป็น datetime
    date_series_formatted = pd.to_datetime(pd.Series(gregorian_dates), errors='coerce').dropna()

    # เอา label แบบ "มกราคม 2024"
    date_labels = date_series_formatted.dt.to_period("M").dt.strftime("%B %Y")
    value_counts = date_labels.value_counts()
    total = value_counts.sum()

    # ปุ่มเลือกการเรียง
    sort_by_count = st.checkbox("🔄 เรียงตามจำนวน (มาก → น้อย)", value=False)

    if not sort_by_count:
        # เรียงตามลำดับเวลา
        value_counts = value_counts.sort_index(key=lambda x: pd.to_datetime(x, format="%B %Y"))

    col1, col2 = st.columns(2)
    half = (len(value_counts) + 1) // 2

    for i, (month, count) in enumerate(value_counts.items()):
        text = f"- <span style='color:pink;'>{month}</span> : <b>{count:,}</b> ครั้ง <span style='color:skyblue;'>({(count/total)*100:.2f}%)</span>"
        if i < half:
            with col1:
                st.markdown(text, unsafe_allow_html=True)
        else:
            with col2:
                st.markdown(text, unsafe_allow_html=True)

def part1_title(data_sheet_1='data_sheet_1'):
    st.title("🔍 ข้อมูลเบื้องต้น")

    st.subheader("รายละเอียดข้อมูล")
    st.write(f"ไฟล์นี้มีทั้งหมด **{data_sheet_1.shape[1]} คอลัมน์** คือ")
    # รายชื่อคอลัมน์ (แนวนอน ใช้ | คั่น)
    columns_list = list(data_sheet_1.columns)
    columns_str = " | ".join(columns_list)
    st.write(columns_str)

    #เดือน
    st.subheader("เดือน")
    display_month_summary(data_sheet_1["เดือน"])
    
    st.subheader("ผลิตภัณฑ์")
    display_unique_items_with_else(data_sheet_1["ผลิตภัณฑ์"], label="ผลิตภัณฑ์",number=4,unit='ผลิตภัณฑ์')

    st.subheader("ชนิดมิเตอร์")
    display_unique_items_with_else(data_sheet_1["ชนิดมิเตอร์"], label="ชนิดมิเตอร์",number=4,unit='อัน')

    st.subheader("สัญญา")
    display_unique_items_with_else(data_sheet_1["สัญญา"], label="สัญญา",number=4,unit='สัญญา')

    st.subheader("สาเหตุการชำรุด")
    display_unique_items_with_else(data_sheet_1["สาเหตุการชำรุด"], label="สาเหตุการชำรุด",number=8,unit='สาเหตุ')

def thai_year_to_gregorian_for_title(date_series):
    """รับ Series ของวันที่เป็น พ.ศ. แล้วแปลงเป็น ค.ศ. แบบสวยงาม"""
    gregorian_dates = []

    for date_str in date_series.dropna():
        try:
            parts = str(date_str).split("-")
            if len(parts) == 3:
                year = int(parts[0]) - 543 
                month = int(parts[1])
                # ใช้ชื่อเดือนภาษาไทยสวยงาม
                thai_months = [
                    "", "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
                    "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"
                ]
                month_name = thai_months[month]
                formatted_date = f"{month_name} {year}"
                gregorian_dates.append(formatted_date)
            else:
                gregorian_dates.append(None)
        except:
            gregorian_dates.append(None)

    return pd.Series(gregorian_dates)

def plot_grouped_stacked_bar_streamlit(
    data_sheet_1=
    'a', 
    month_col='ผลิตภัณฑ์', 
    claim_col='เคลม', 
    cause_col='สาเหตุการชำรุด'
    ):
    # st.subheader("Grouped Stacked Bar Chart of Brands per Claimable per Causes")

    # --- Read data ---
    df = data_sheet_1.copy()

    # --- Count records per (month, claim, cause) ---
    grouped = (
        df
        .groupby([month_col, claim_col, cause_col])
        .size()
        .reset_index(name='count')
    )
    product_totals = grouped.groupby(month_col)['count'].sum()

    # --- Pivot directly without any top-80% logic ---
    pivot_df = grouped.pivot_table(
        index=[month_col, claim_col],
        columns=cause_col,
        values='count',
        fill_value=0
    ).reset_index()

    # --- Ensure all combos are present ---
    claim_order = ["เคลมได้", "เคลมไม่ได้", "ปกติ"]
    all_months = sorted(df[month_col].unique())
    all_combos = pd.MultiIndex.from_product(
        [all_months, claim_order],
        names=[month_col, claim_col]
    )
    pivot_df = (
        pivot_df
        .set_index([month_col, claim_col])
        .reindex(all_combos, fill_value=0)
        .reset_index()
    )

    # --- Final list of causes ---
    damage_causes = [c for c in pivot_df.columns if c not in [month_col, claim_col]]

    # --- Build grouped & stacked bar chart ---
    fig = go.Figure()
    bar_width = 0.25
    n_claims = len(claim_order)
    offsets = np.linspace(-bar_width, bar_width, n_claims)
    month_positions = {m: i for i, m in enumerate(all_months)}

    for i, cl in enumerate(claim_order):
        df_cl = pivot_df[pivot_df[claim_col] == cl]
        x_vals = [month_positions[m] + offsets[i] for m in df_cl[month_col]]

        bottom = np.zeros(len(df_cl))
        for cause in damage_causes:
            y_vals = df_cl[cause].values
            total_for_brand = df_cl[month_col].map(product_totals).values
            pct_vals = (y_vals / total_for_brand) * 100

            # pack product-name and percent into customdata
            custom = np.stack([
                df_cl[month_col].astype(str).values,
                pct_vals
            ], axis=-1)

            fig.add_trace(go.Bar(
                x=x_vals,
                y=y_vals,
                name=cause if i == 0 else None,
                customdata=custom,            # <-- new
                hovertemplate=(
                    "Product: %{customdata[0]}<br>"
                    f"Claim: {cl}<br>"
                    f"Cause: {cause}<br>"
                    "Count: %{y}<br>"
                    "Pct of Brand: %{customdata[1]:.1f}%<extra></extra>"
                ),
                base=bottom,
                width=bar_width
            ))
            bottom += y_vals


    fig.update_layout(
        barmode='stack',
        xaxis=dict(
            tickmode='array',
            tickvals=[month_positions[m] for m in all_months],
            ticktext=all_months
        ),
        title="Grouped Stacked Bar Chart by Brands per Claimable per Causes",
        xaxis_title=month_col,
        yaxis_title="จำนวน",
        font=dict(family="TH Sarabun New, sans-serif", size=16),
        height=600,
        showlegend=False,
    )

    fig.add_annotation(
        text="📊   1️⃣= เคลมได้    2️⃣ = เคลมไม่ได้    3️⃣ = ปกติ",
        xref="paper", yref="paper",
        x=0.5, y=1.08,           # 0.5 = กลางแนวนอน, 1.08 = เหนือ title เล็กน้อย
        showarrow=False,
        font=dict(family="TH Sarabun New, sans-serif", size=14),
        align="center"
    )

    st.plotly_chart(fig, use_container_width=True)

def summarize_top3_by_brand(df):
    if df.empty:
        st.subheader("📋 ตารางสรุป")
        st.warning("ไม่มีข้อมูลสำหรับการสรุป")
        return pd.DataFrame()  # ส่งคืน DataFrame ว่าง

    # รวมจำนวนทั้งหมด
    total_count = df.groupby("ผลิตภัณฑ์").size().rename("จำนวนทั้งหมด")

    # นับแต่ละประเภทเคลม
    claimable = df[df["เคลม"] == "เคลมได้"].groupby("ผลิตภัณฑ์").size().rename("เคลมได้")
    unclaimable = df[df["เคลม"] == "เคลมไม่ได้"].groupby("ผลิตภัณฑ์").size().rename("เคลมไม่ได้")
    normal = df[df["เคลม"] == "ปกติ"].groupby("ผลิตภัณฑ์").size().rename("ปกติ")

    # สาเหตุ top 3 ต่อแบรนด์ พร้อมจำนวน
    top_causes = (
        df.groupby(["ผลิตภัณฑ์", "สาเหตุการชำรุด"])
        .size()
        .reset_index(name="count")
        .sort_values(["ผลิตภัณฑ์", "count"], ascending=[True, False])
    )

    # ดึง top 3
    top3 = (
        top_causes.groupby("ผลิตภัณฑ์")
        .head(3)
        .groupby("ผลิตภัณฑ์")[["สาเหตุการชำรุด", "count"]]
        .apply(lambda x: list(zip(x["สาเหตุการชำรุด"], x["count"])))
        .reset_index(name="cause_count_list")
    )

    # สร้างคอลัมน์ สาเหตุ Top 1, 2, 3 พร้อมจำนวน
    def format_top3(cause_list):
        cause_list = cause_list + [("", 0)] * (3 - len(cause_list))  # เติมให้ครบ 3 อันดับ
        return [f"{cause} ({count})" if cause else "" for cause, count in cause_list]

    top3[["สาเหตุอันดับ 1", "สาเหตุอันดับ 2", "สาเหตุอันดับ 3"]] = pd.DataFrame(
        top3["cause_count_list"].apply(format_top3).to_list(), index=top3.index
    )
    top3.drop(columns="cause_count_list", inplace=True)

    # รวมข้อมูล
    result_df = pd.DataFrame(total_count).join([claimable, unclaimable, normal])
    result_df = result_df.fillna(0).astype({"จำนวนทั้งหมด": int, "เคลมได้": int, "เคลมไม่ได้": int, "ปกติ": int})

    # ✅ เพิ่มคอลัมน์ "จำนวนที่ชำรุด"
    result_df["จำนวนที่ชำรุด"] = result_df["เคลมได้"] + result_df["เคลมไม่ได้"]

    # จัดลำดับคอลัมน์
    cols = result_df.columns.tolist()
    cols.insert(1, cols.pop(cols.index("จำนวนที่ชำรุด")))  # ย้าย "จำนวนที่ชำรุด" ไปถัดจาก "จำนวนทั้งหมด"
    result_df = result_df[cols]

    # รวมกับ Top 3
    result_df = result_df.reset_index().merge(top3, on="ผลิตภัณฑ์", how="left")

    # เรียงลำดับตาม "จำนวนทั้งหมด"
    result_df_sorted = result_df.sort_values(by="จำนวนทั้งหมด", ascending=False).reset_index(drop=True)

    # เพิ่มคอลัมน์ลำดับ
    result_df_sorted.insert(0, 'ลำดับ', range(1, len(result_df_sorted) + 1))

    # แสดงผลบน Streamlit
    st.subheader("📋 ตารางสรุปสาเหตุการชำรุด Top 3 พร้อมจำนวนเคลมและจำนวนสาเหตุ")
    st.dataframe(result_df_sorted, use_container_width=True)

    return result_df_sorted

def main():

    #setting files
    #รองรับได้ 2 sheet 
    #path_data = st.file_uploader("อัปโหลดไฟล์ Excel", type=["xlsx"])
    path_data = "meter_data.xlsx"

    if path_data is not None:
        data, data_sheet_1, data_sheet_2 = open_file(path_data)
        # st.dataframe(data_sheet_1.head())
        part1_title(data_sheet_1)
        st.markdown("---")

        plot_grouped_stacked_bar_streamlit(data_sheet_1=data_sheet_1)

        ## Part 2 ##
        st.subheader(":balloon: :blue-background[**Charts**]")
        claimable = st.multiselect("Select claimable:",
                                    options=data_sheet_1["เคลม"].unique(),
                                    default=data_sheet_1["เคลม"].unique()
        )
        brand = st.multiselect("Select brand:",
                               options=data_sheet_1["ผลิตภัณฑ์"].unique(),
                               default=data_sheet_1["ผลิตภัณฑ์"].unique()
        )
        df_selection = data_sheet_1.query(
        "เคลม == @claimable & ผลิตภัณฑ์ == @brand"
        )
        
        total_meters = int(df_selection["เคลม"].count())
        brand_names = df_selection["ผลิตภัณฑ์"].unique()
        brand_names_str = ', '.join(brand_names)

        left_column, middle_column = st.columns(2)
        with left_column:
            st.markdown("**Selected Brand :**")
            st.markdown(f"{brand_names_str}")

        with middle_column:
            st.markdown("**Total meters :**")
            st.markdown(f"{total_meters}")
        
        ### Graph 1 ##############
        agg = (
            df_selection
            .groupby(['เคลม', 'ผลิตภัณฑ์', 'สาเหตุการชำรุด'])
            .size()
            .reset_index(name='count')
        )
        agg['percent'] = (
            agg['count']
            / agg.groupby('ผลิตภัณฑ์')['count']
                .transform('sum')
            * 100
        )
        brand_order = (
            agg
            .groupby('ผลิตภัณฑ์')['count']
            .sum()
            .sort_values(ascending=False)
            .index
            .tolist()
        )
        
        # เลือกสี
        if len(claimable) == 1:
            color_dim = 'สาเหตุการชำรุด'
            chart_title = f'Breakdown of "{claimable[0]}" by Causes per Brand'
            color_map = None 
        else:
            color_dim = 'เคลม'
            chart_title = 'Claim Status by Brand'
            color_map = {
                'ปกติ': 'aqua',
                'เคลมได้': 'palegreen',
                'เคลมไม่ได้': 'red'
            }

        fig = px.bar(
            agg,
            y='ผลิตภัณฑ์',
            x='count',
            color=color_dim,           
            orientation='h',
            barmode='stack',
            title=chart_title,
            hover_data={
                'สาเหตุการชำรุด': True,
                'percent': ':.1f'
            },
            labels={
                'count': 'Total meters',
                'ผลิตภัณฑ์': 'Brands',
                'เคลม': 'Status',
                'สาเหตุการชำรุด': 'Cause',
                'percent': ' % '
            },
            color_discrete_map=color_map,
            category_orders={'ผลิตภัณฑ์': brand_order},
            template='plotly_white'
        )

        totals = agg.groupby('ผลิตภัณฑ์')['count'].sum().reindex(brand_order)
        for brand, total in totals.items():
            fig.add_annotation(
                y=brand,
                x=total,
                text=str(total),
                showarrow=False,
                xanchor='left',
                xshift=5,
                font=dict(size=12)
            )

        if len(claimable) > 1:
            #หลายสถานะ
            breakdown = (
                agg
                .pivot_table(
                    index='ผลิตภัณฑ์',
                    columns='เคลม',
                    values='count',
                    aggfunc='sum',
                    fill_value=0
                )
                .reindex(index=brand_order, columns=claimable, fill_value=0)
            )
            for b in brand_order:
                texts = [f"{status}: {breakdown.loc[b, status]}" for status in claimable]
                fig.add_annotation(
                    xref='paper', x=-0.24,
                    y=b,
                    text="<br>".join(texts),
                    showarrow=False,
                    align='right',
                    font=dict(size=11)
                )

        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=True,
            yaxis=dict(autorange='reversed'),
            xaxis=dict(showgrid=False),
            margin=dict(l=180, r=40, t=80, b=80)
        )

        st.plotly_chart(fig)

        st.markdown("---")

        ## Graph 2 #####################################################################################

        contract_brand_df = (
            data_sheet_1
            .groupby(["สัญญา", "ผลิตภัณฑ์"])
            .size()
            .reset_index(name="meter_count")
        )
        contract_brand_df["label"] = (
            contract_brand_df["ผลิตภัณฑ์"]
            + ": "
            + contract_brand_df["meter_count"].astype(str)
        )
        # 2) draw vertical grouped bar
        fig = px.bar(
            contract_brand_df,
            x="สัญญา",          # <-- contracts go on the *x* categorical axis
            y="meter_count",    # <-- meter counts on the numeric *y* axis
            # color="ผลิตภัณฑ์",  # <-- one trace per brand
            barmode="group",    # <-- side-by-side grouping
            # text="label",
            hover_data="ผลิตภัณฑ์",
            title="Meters per Contract per Brand",
            labels={
                "สัญญา": "สัญญา",
                "meter_count": "Total meters",
                "ผลิตภัณฑ์": "แบรนด์"
            },
            template="plotly_white"
        )
        fig.update_traces(width=0.2)
        fig.update_layout(
            bargap=0.5,      # gap between *contract* groups
            bargroupgap=0.1  # gap between bars *within* each contract
        )
        contract_totals = (
            contract_brand_df
            .groupby("สัญญา", as_index=False)["meter_count"]
            .sum()
            .rename(columns={"meter_count": "total_meters"})
        )

        max_total = contract_totals["total_meters"].max()
        fig.update_yaxes(range=[0, max_total * 1.15])

        # วน loop สร้าง annotation
        for _, row in contract_totals.iterrows():
            fig.add_annotation(
                x=row["สัญญา"],
                y=row["total_meters"] * 1.02,   # เลื่อนขึ้นเล็กน้อยเหนือ bar
                text=f"{row['total_meters']}",
                showarrow=False,
                font=dict(size=12, color="white"),
                xanchor="center",
                yanchor="bottom"
            )

        # 5) แสดงกราฟพร้อม annotation
        st.plotly_chart(fig)
        st.markdown("### รายละเอียดของแต่ละสัญญา")


        contract_totals = (
            contract_brand_df
            .groupby("สัญญา")["meter_count"]
            .sum()
            .sort_values(ascending=False)
        )
        contracts_sorted = sorted(
    contract_brand_df["สัญญา"].astype(str).unique()
)

        tabs = st.tabs(contracts_sorted)
        
        for contract_label, tab in zip(contracts_sorted, tabs):
            with tab:
                st.markdown(f"### สัญญา: {contract_label}")
                df_c = (
                    contract_brand_df[
                        contract_brand_df["สัญญา"].astype(str) == contract_label
                    ]
                    .sort_values("meter_count", ascending=False)
                )
                st.table(
                    df_c[["ผลิตภัณฑ์", "meter_count"]]
                    .rename(columns={
                        "ผลิตภัณฑ์": "Brand",
                        "meter_count": "Meters"
                    })
                    .set_index("Brand")
                )

        #### Graph 3 #####
        st.markdown("## เลือกตัวแปรสำหรับ Radar Chart")
        col1, col2 = st.columns(2)
        with col1:
            show_claim = st.checkbox("เคลม", value=True)
        with col2:
            show_brand = st.checkbox("ผลิตภัณฑ์", value=False)

        if show_claim and show_brand:
            st.error("❌ กรุณาเลือกอย่างใดอย่างหนึ่ง")
            st.stop()
        if not show_claim and not show_brand:
            st.error("❌ กรุณาเลือก เคลม หรือ ผลิตภัณฑ์ อย่างน้อยหนึ่งตัว")
            st.stop()

        group_col = "เคลม" if show_claim else "ผลิตภัณฑ์"

        def extract_month(val):
            if pd.isna(val):
                return None
            if isinstance(val, (datetime.datetime, datetime.date)):
                return val.month
            try:
                return pd.to_datetime(val).month
            except:
                return None

        data_sheet_1["month_num"] = data_sheet_1["เดือน"].apply(extract_month)

        thai_month_map = {
            1: "ม.ค.", 2: "ก.พ.", 3: "มี.ค.", 4: "เม.ย.",
            5: "พ.ค.", 6: "มิ.ย.", 7: "ก.ค.", 8: "ส.ค.",
            9: "ก.ย.", 10: "ต.ค.", 11: "พ.ย.", 12: "ธ.ค."
        }
        data_sheet_1["เดือน_str"] = data_sheet_1["month_num"].map(thai_month_map)

        months_order = [
            thai_month_map[m]
            for m in range(1, 13)
            if thai_month_map[m] in data_sheet_1["เดือน_str"].unique()
        ]

        pivot = (
            data_sheet_1
            .groupby(["เดือน_str", group_col])
            .size()
            .unstack(fill_value=0)
            .reindex(months_order, fill_value=0)
        )

        ## radar chart ##
        fig = go.Figure()
        for category in pivot.columns:
            fig.add_trace(go.Scatterpolar(
                r=pivot[category].tolist(),
                theta=months_order,
                fill="toself",
                name=str(category),
                opacity=0.6
            ))

        fig.update_layout(
            title=f"Monthly Counts by {group_col}",
            polar=dict(
                radialaxis=dict(visible=True)
            ),
            showlegend=True
        )
        st.plotly_chart(fig, use_container_width=True)
        
        ## Part 3 ##
  
        summarize_top3_by_brand(df_selection)



        

main()
