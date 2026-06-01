<html>
<head>
<title>app.py</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<style type="text/css">
.s0 { color: #0033b3;}
.s1 { color: #080808;}
.s2 { color: #8c8c8c; font-style: italic;}
.s3 { color: #067d17;}
.s4 { color: #1750eb;}
.s5 { color: #0037a6;}
</style>
</head>
<body bgcolor="#ffffff">
<table CELLSPACING=0 CELLPADDING=5 COLS=1 WIDTH="100%" BGCOLOR="#c0c0c0" >
<tr><td><center>
<font face="Arial, Helvetica" color="#000000">
app.py</font>
</center></td></tr></table>
<pre><span class="s0">import </span><span class="s1">streamlit </span><span class="s0">as </span><span class="s1">st</span>
<span class="s0">import </span><span class="s1">pandas </span><span class="s0">as </span><span class="s1">pd</span>
<span class="s0">import </span><span class="s1">numpy </span><span class="s0">as </span><span class="s1">np</span>
<span class="s0">import </span><span class="s1">seaborn </span><span class="s0">as </span><span class="s1">sns</span>
<span class="s0">import </span><span class="s1">matplotlib.pyplot </span><span class="s0">as </span><span class="s1">plt</span>
<span class="s0">from </span><span class="s1">sklearn.ensemble </span><span class="s0">import </span><span class="s1">RandomForestClassifier</span>

<span class="s2"># 设置页面</span>
<span class="s1">st.set_page_config(page_title=</span><span class="s3">&quot;老年肌少症数字孪生系统&quot;</span><span class="s1">, layout=</span><span class="s3">&quot;wide&quot;</span><span class="s1">)</span>


<span class="s2"># 1. 加载数据并训练模型 (因为你没存模型文件，我们网页启动时临时训练一个，保证能用)</span>
<span class="s1">@st.cache_resource</span>
<span class="s0">def </span><span class="s1">get_model_and_data():</span>
    <span class="s1">df = pd.read_csv(</span><span class="s3">'老年肌少症数字孪生专题数据集_已标注.csv'</span><span class="s1">)</span>

    <span class="s2"># 【新增：清洗数据】</span>
    <span class="s2"># 1. 自动填补所有空值（用中位数填充，这在医学数据处理里最稳妥）</span>
    <span class="s1">df = df.fillna(df.median())</span>

    <span class="s2"># 2. 检查一下标签列有没有缺失值，如果有，直接删掉那一行</span>
    <span class="s0">if </span><span class="s1">df[</span><span class="s3">'Sarcopenia_Label'</span><span class="s1">].isnull().any():</span>
        <span class="s1">df = df.dropna(subset=[</span><span class="s3">'Sarcopenia_Label'</span><span class="s1">])</span>

    <span class="s1">exclude_cols = [</span><span class="s3">'ID'</span><span class="s1">, </span><span class="s3">'ivy'</span><span class="s1">, </span><span class="s3">'bloodweight'</span><span class="s1">, </span><span class="s3">'lgrip'</span><span class="s1">, </span><span class="s3">'rgrip'</span><span class="s1">, </span><span class="s3">'wspeed'</span><span class="s1">, </span><span class="s3">'max_grip'</span><span class="s1">, </span><span class="s3">'Sarcopenia_Label'</span><span class="s1">]</span>
    <span class="s1">X_cols = [c </span><span class="s0">for </span><span class="s1">c </span><span class="s0">in </span><span class="s1">df.columns </span><span class="s0">if </span><span class="s1">c </span><span class="s0">not in </span><span class="s1">exclude_cols]</span>

    <span class="s2"># 临时训练模型</span>
    <span class="s1">X = df[X_cols]</span>
    <span class="s1">y = df[</span><span class="s3">'Sarcopenia_Label'</span><span class="s1">]</span>
    <span class="s1">model = RandomForestClassifier().fit(X, y)</span>
    <span class="s0">return </span><span class="s1">model, X_cols, df[X_cols].median().to_dict()</span>

<span class="s0">with </span><span class="s1">st.spinner(</span><span class="s3">'正在激活数字孪生系统计算引擎，请稍后...'</span><span class="s1">):</span>
    <span class="s1">rf_model, X_cols_base, feature_medians = get_model_and_data()</span>
<span class="s1">st.success(</span><span class="s3">'数字孪生模拟系统已准备就绪'</span><span class="s1">)</span>

<span class="s2"># 2. 侧边栏 UI 输入区</span>
<span class="s1">st.sidebar.header(</span><span class="s3">&quot; 人口学基本表型&quot;</span><span class="s1">)</span>
<span class="s1">gender = st.sidebar.selectbox(</span><span class="s3">&quot;性别&quot;</span><span class="s1">, [(</span><span class="s3">&quot;男性&quot;</span><span class="s1">, </span><span class="s4">1.0</span><span class="s1">), (</span><span class="s3">&quot;女性&quot;</span><span class="s1">, </span><span class="s4">2.0</span><span class="s1">)], format_func=</span><span class="s0">lambda </span><span class="s1">x: x[</span><span class="s4">0</span><span class="s1">])[</span><span class="s4">1</span><span class="s1">]</span>
<span class="s1">age = st.sidebar.slider(</span><span class="s3">&quot;年龄(岁)&quot;</span><span class="s1">, </span><span class="s4">60</span><span class="s1">, </span><span class="s4">95</span><span class="s1">, </span><span class="s4">82</span><span class="s1">)</span>
<span class="s1">bmi = st.sidebar.slider(</span><span class="s3">&quot;BMI&quot;</span><span class="s1">, </span><span class="s4">14.0</span><span class="s1">, </span><span class="s4">35.0</span><span class="s1">, </span><span class="s4">15.8</span><span class="s1">)</span>

<span class="s1">st.sidebar.header(</span><span class="s3">&quot; 行为与身体功能&quot;</span><span class="s1">)</span>
<span class="s1">sleep = st.sidebar.slider(</span><span class="s3">&quot;睡眠时间(h)&quot;</span><span class="s1">, </span><span class="s4">3.0</span><span class="s1">, </span><span class="s4">10.0</span><span class="s1">, </span><span class="s4">4.0</span><span class="s1">)</span>
<span class="s1">iadl = st.sidebar.slider(</span><span class="s3">&quot;IADL评分&quot;</span><span class="s1">, </span><span class="s4">0.0</span><span class="s1">, </span><span class="s4">10.0</span><span class="s1">, </span><span class="s4">5.0</span><span class="s1">)</span>
<span class="s1">smokev = st.sidebar.selectbox(</span><span class="s3">&quot;吸烟史&quot;</span><span class="s1">, [(</span><span class="s3">&quot;否&quot;</span><span class="s1">, </span><span class="s4">0.0</span><span class="s1">), (</span><span class="s3">&quot;是&quot;</span><span class="s1">, </span><span class="s4">1.0</span><span class="s1">)], format_func=</span><span class="s0">lambda </span><span class="s1">x: x[</span><span class="s4">0</span><span class="s1">])[</span><span class="s4">1</span><span class="s1">]</span>
<span class="s1">chronic = st.sidebar.slider(</span><span class="s3">&quot;慢性病种数&quot;</span><span class="s1">, </span><span class="s4">0</span><span class="s1">, </span><span class="s4">8</span><span class="s1">, </span><span class="s4">3</span><span class="s1">)</span>
<span class="s1">fall = st.sidebar.selectbox(</span><span class="s3">&quot;两年跌倒史&quot;</span><span class="s1">, [(</span><span class="s3">&quot;无&quot;</span><span class="s1">, </span><span class="s4">0.0</span><span class="s1">), (</span><span class="s3">&quot;有&quot;</span><span class="s1">, </span><span class="s4">1.0</span><span class="s1">)], format_func=</span><span class="s0">lambda </span><span class="s1">x: x[</span><span class="s4">0</span><span class="s1">])[</span><span class="s4">1</span><span class="s1">]</span>

<span class="s1">st.sidebar.header(</span><span class="s3">&quot; 微观生化指标&quot;</span><span class="s1">)</span>
<span class="s1">crea = st.sidebar.slider(</span><span class="s3">&quot;初始血肌酐&quot;</span><span class="s1">, </span><span class="s4">0.2</span><span class="s1">, </span><span class="s4">1.5</span><span class="s1">, </span><span class="s4">0.45</span><span class="s1">)</span>
<span class="s1">cysc = st.sidebar.slider(</span><span class="s3">&quot;C胱抑素C&quot;</span><span class="s1">, </span><span class="s4">0.5</span><span class="s1">, </span><span class="s4">2.5</span><span class="s1">, </span><span class="s4">1.65</span><span class="s1">)</span>
<span class="s1">hgb = st.sidebar.slider(</span><span class="s3">&quot;血红蛋白&quot;</span><span class="s1">, </span><span class="s4">8.0</span><span class="s1">, </span><span class="s4">18.0</span><span class="s1">, </span><span class="s4">10.5</span><span class="s1">)</span>
<span class="s1">glu = st.sidebar.slider(</span><span class="s3">&quot;空腹血糖&quot;</span><span class="s1">, </span><span class="s4">3.0</span><span class="s1">, </span><span class="s4">12.0</span><span class="s1">, </span><span class="s4">5.5</span><span class="s1">)</span>
<span class="s1">crp = st.sidebar.slider(</span><span class="s3">&quot;C反应蛋白&quot;</span><span class="s1">, </span><span class="s4">0.1</span><span class="s1">, </span><span class="s4">15.0</span><span class="s1">, </span><span class="s4">6.2</span><span class="s1">)</span>
<span class="s1">wbc = st.sidebar.slider(</span><span class="s3">&quot;白细胞计数&quot;</span><span class="s1">, </span><span class="s4">3.0</span><span class="s1">, </span><span class="s4">15.0</span><span class="s1">, </span><span class="s4">7.0</span><span class="s1">)</span>

<span class="s2"># 3. 干预决策区</span>
<span class="s1">st.subheader(</span><span class="s3">&quot; 临床虚拟管理策略&quot;</span><span class="s1">)</span>
<span class="s1">chk_exercise = st.checkbox(</span><span class="s3">&quot;处方 A：定制化抗阻功能训练&quot;</span><span class="s1">)</span>
<span class="s1">chk_nutrition = st.checkbox(</span><span class="s3">&quot;处方 B：高蛋白膳食与纠正贫血&quot;</span><span class="s1">)</span>
<span class="s1">chk_biomed = st.checkbox(</span><span class="s3">&quot;处方 C：微观代谢纠正与抗炎调理&quot;</span><span class="s1">)</span>

<span class="s2"># 4. 计算引擎</span>
<span class="s0">if </span><span class="s1">st.button(</span><span class="s3">&quot; 启动临床机制推演&quot;</span><span class="s1">):</span>
    <span class="s2"># 构建 twin_v0</span>
    <span class="s1">twin_v0 = {col: feature_medians[col] </span><span class="s0">for </span><span class="s1">col </span><span class="s0">in </span><span class="s1">X_cols_base}</span>
    <span class="s1">twin_v0.update({</span><span class="s3">'gender'</span><span class="s1">: gender, </span><span class="s3">'age'</span><span class="s1">: age, </span><span class="s3">'bmi'</span><span class="s1">: bmi, </span><span class="s3">'sleep'</span><span class="s1">: sleep, </span><span class="s3">'iadl'</span><span class="s1">: iadl,</span>
                    <span class="s3">'smokev'</span><span class="s1">: smokev, </span><span class="s3">'chronic'</span><span class="s1">: chronic, </span><span class="s3">'fall_down'</span><span class="s1">: fall, </span><span class="s3">'bl_crea'</span><span class="s1">: crea,</span>
                    <span class="s3">'bl_cysc'</span><span class="s1">: cysc, </span><span class="s3">'bl_hgb'</span><span class="s1">: hgb, </span><span class="s3">'bl_glu'</span><span class="s1">: glu, </span><span class="s3">'bl_crp'</span><span class="s1">: crp, </span><span class="s3">'bl_wbc'</span><span class="s1">: wbc, </span><span class="s3">'exercise'</span><span class="s1">: </span><span class="s4">0.0</span><span class="s1">})</span>

    <span class="s1">prob_v0 = rf_model.predict_proba(pd.DataFrame([twin_v0]))[</span><span class="s4">0</span><span class="s1">, </span><span class="s4">1</span><span class="s1">]</span>

    <span class="s2"># 模拟干预</span>
    <span class="s1">twin_v1 = twin_v0.copy()</span>
    <span class="s1">synergy = </span><span class="s4">1.25 </span><span class="s0">if </span><span class="s1">(chk_exercise </span><span class="s0">and </span><span class="s1">chk_nutrition) </span><span class="s0">else </span><span class="s4">1.0</span>

    <span class="s0">if </span><span class="s1">chk_exercise:</span>
        <span class="s1">twin_v1.update({</span><span class="s3">'exercise'</span><span class="s1">: </span><span class="s4">1.0</span><span class="s1">, </span><span class="s3">'bl_crea'</span><span class="s1">: twin_v1[</span><span class="s3">'bl_crea'</span><span class="s1">] * (</span><span class="s4">1 </span><span class="s1">+ </span><span class="s4">0.2 </span><span class="s1">* synergy),</span>
                        <span class="s3">'iadl'</span><span class="s1">: max(</span><span class="s4">0</span><span class="s1">, twin_v1[</span><span class="s3">'iadl'</span><span class="s1">] - </span><span class="s4">2 </span><span class="s1">* synergy)})</span>
    <span class="s0">if </span><span class="s1">chk_nutrition:</span>
        <span class="s1">twin_v1[</span><span class="s3">'bl_hgb'</span><span class="s1">] = min(twin_v1[</span><span class="s3">'bl_hgb'</span><span class="s1">] * (</span><span class="s4">1 </span><span class="s1">+ </span><span class="s4">0.15 </span><span class="s1">* synergy), feature_medians[</span><span class="s3">'bl_hgb'</span><span class="s1">])</span>
    <span class="s0">if </span><span class="s1">chk_biomed:</span>
        <span class="s1">twin_v1.update({</span><span class="s3">'bl_crp'</span><span class="s1">: twin_v1[</span><span class="s3">'bl_crp'</span><span class="s1">] * </span><span class="s4">0.6</span><span class="s1">, </span><span class="s3">'bl_cysc'</span><span class="s1">: twin_v1[</span><span class="s3">'bl_cysc'</span><span class="s1">] * </span><span class="s4">0.85</span><span class="s1">, </span><span class="s3">'sleep'</span><span class="s1">: </span><span class="s4">7.0</span><span class="s1">,</span>
                        <span class="s3">'bl_glu'</span><span class="s1">: feature_medians[</span><span class="s3">'bl_glu'</span><span class="s1">], </span><span class="s3">'bl_wbc'</span><span class="s1">: feature_medians[</span><span class="s3">'bl_wbc'</span><span class="s1">], </span><span class="s3">'smokev'</span><span class="s1">: </span><span class="s4">0.0</span><span class="s1">})</span>

    <span class="s1">prob_v1 = rf_model.predict_proba(pd.DataFrame([twin_v1]))[</span><span class="s4">0</span><span class="s1">, </span><span class="s4">1</span><span class="s1">]</span>

    <span class="s2"># 展示图表</span>
    <span class="s1">fig, ax = plt.subplots(figsize=(</span><span class="s4">6</span><span class="s1">, </span><span class="s4">4</span><span class="s1">))</span>
    <span class="s1">sns.barplot(x=[</span><span class="s3">'干预前'</span><span class="s1">, </span><span class="s3">'干预后'</span><span class="s1">], y=[prob_v0, prob_v1], palette=[</span><span class="s3">'#e74c3c'</span><span class="s1">, </span><span class="s3">'#2ecc71'</span><span class="s1">])</span>
    <span class="s1">plt.rcParams[</span><span class="s3">'font.sans-serif'</span><span class="s1">] = [</span><span class="s3">'SimHei'</span><span class="s1">]</span>
    <span class="s1">plt.rcParams[</span><span class="s3">'axes.unicode_minus'</span><span class="s1">] = </span><span class="s0">False</span>
    <span class="s1">st.pyplot(fig)</span>

    <span class="s1">st.write(</span><span class="s3">f&quot;### 评估结果: 风险概率从 </span><span class="s5">{</span><span class="s1">prob_v0</span><span class="s5">:</span><span class="s3">.2%</span><span class="s5">} </span><span class="s3">降至 </span><span class="s5">{</span><span class="s1">prob_v1</span><span class="s5">:</span><span class="s3">.2%</span><span class="s5">}</span><span class="s3">&quot;</span><span class="s1">)</span>

</pre>
</body>
</html>
