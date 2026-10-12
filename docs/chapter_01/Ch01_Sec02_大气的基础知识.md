---
chapter: 1
section: 1.2
title: 大气的基础知识
date: 2026-10-12
status: completed
source_doc_id: 1CxpOg81Hg58HKBeu8BNTwGQDPvAosu8ZfbTexmr7l9w
---

# 第 1 章 行星大气与地球大气的成分及结构
## 1.2 大气的基础知识（全公式族谱与物理机制精讲）

> **教材基准**：银燕等编著《大气物理学》（气象出版社）第 1 章  
> **核心主题**：干空气与湿空气状态方程推导、分压定律、水汽参量体系、虚温 $T_v$ 物理本质与应用

---

## 一、干空气的状态方程

### 1.1 理想气体状态方程（微观到宏观）
从分子动理论与热力学基本定律出发，对于单组分理想气体，其状态方程满足克拉珀龙方程：
$$p V = n R^* T = \frac{m}{M} R^* T$$

其中：
- $p$：气体压强 $(\text{Pa})$
- $V$：体积 $(\text{m}^3)$
- $m$：气体质量 $(\text{kg})$
- $M$：气体摩尔质量 $(\text{kg}\cdot\text{mol}^{-1})$
- $T$：绝对热力学温度 $(\text{K})$
- $R^* = 8.31446\,\text{J}\cdot\text{mol}^{-1}\cdot\text{K}^{-1}$：普适通用气体常数

引入**气体的比气体常数（特定气体常数）** $R$：
$$R = \frac{R^*}{M}$$

定义气体密度 $\rho = \frac{m}{V}$（或比容 $\alpha = \frac{1}{\rho}$），则状态方程化为大气学最常用的形式：
$$p = \rho R T \quad \Longleftrightarrow \quad p \alpha = R T$$

### 1.2 干空气有效平均摩尔质量与干空气比气体常数 $R_d$
低层大气（85~90 km 以下的均质层内），湍流混合十分剧烈，干空气主要成分（$\text{N}_2, \text{O}_2, \text{Ar}, \text{CO}_2$ 等）的体积混合比保持高度恒定。

设干空气各组分的体积分数（摩尔分数）为 $x_i = \frac{V_i}{V} = \frac{n_i}{n}$，则干空气的平均视摩尔质量 $M_d$ 为：
$$M_d = \sum_{i} x_i M_i \approx 0.78084 \times 28.0134 + 0.20946 \times 31.9988 + 0.00934 \times 39.948 + 0.00041 \times 44.01 \approx 28.966 \times 10^{-3}\,\text{kg}\cdot\text{mol}^{-1}$$

由此可精确导出**干空气比气体常数** $R_d$：
$$R_d = \frac{R^*}{M_d} = \frac{8.31446}{28.966 \times 10^{-3}} \approx 287.05\,\text{J}\cdot\text{kg}^{-1}\cdot\text{K}^{-1}$$

**干空气状态方程**表述为：
$$p_d = \rho_d R_d T$$

---

## 二、水汽的状态方程与常数推导

### 2.1 水汽比气体常数 $R_v$
纯水分子由氢和氧构成，其分子式为 $\text{H}_2\text{O}$，摩尔质量为：
$$M_v \approx 18.0153 \times 10^{-3}\,\text{kg}\cdot\text{mol}^{-1}$$

因此水汽的特定气体常数 $R_v$ 为：
$$R_v = \frac{R^*}{M_v} = \frac{8.31446}{18.0153 \times 10^{-3}} \approx 461.51\,\text{J}\cdot\text{kg}^{-1}\cdot\text{K}^{-1}$$

### 2.2 气象学核心无量纲常数 $\varepsilon$
定义干空气分子量与水汽分子量（或比气体常数之比）的比值为常数 $\varepsilon$：
$$\varepsilon = \frac{M_v}{M_d} = \frac{R_d}{R_v} = \frac{287.05}{461.51} \approx 0.622$$

水汽分压 $e$、水汽密度 $\rho_v$ 与温度 $T$ 的状态方程为：
$$e = \rho_v R_v T$$

---

## 三、湿空气的状态方程与道尔顿分压定律

### 3.1 道尔顿分压定律（Dalton's Law）
真实大气为干空气与水汽构成的多组分混合气体。根据道尔顿分压定律：
1. 混合气体的总压强等于各组分单独存在并占据相同体积、相同温度时所产生的气体分压之和：
   $$p = p_d + e$$
2. 湿空气的总密度等于干空气分密度与水汽分密度之和：
   $$\rho = \rho_d + \rho_v$$

### 3.2 湿空气比气体常数推导
将分密度代入：
$$\rho = \frac{p_d}{R_d T} + \frac{e}{R_v T} = \frac{p - e}{R_d T} + \frac{e}{R_v T}$$

整理得：
$$\rho = \frac{p}{R_d T} \left( 1 - \frac{e}{p} + \frac{R_d}{R_v} \frac{e}{p} \right) = \frac{p}{R_d T} \left[ 1 - (1 - \varepsilon)\frac{e}{p} \right]$$

代入数值 $1 - \varepsilon = 1 - 0.622 = 0.378$：
$$\rho = \frac{p}{R_d T} \left( 1 - 0.378 \frac{e}{p} \right)$$

---

## 四、核心物理量：虚温（Virtual Temperature $T_v$）

### 4.1 虚温的定义初衷与数学构建
在气象动力学与气象物理学计算中，湿空气的成分比随地点、时间和高度不断变化（水汽含量具有剧烈时空非均一性），导致湿空气的比气体常数 $R_m$ 不是一个固定常数。

为了**保留干空气比气体常数 $R_d$ 的形式不变**，使得所有静力学、热力学公式能够直接复用干空气的常数，气象学引入了**虚温 $T_v$**。

**定义**：在相同气压下，密度与该湿空气相同的**假想干空气所具有的温度**，称为该湿空气的虚温 $T_v$。

数学形式要求：
$$p = \rho R_d T_v$$

与前述湿空气状态方程 $p = \rho R_d T \big[ 1 - 0.378 \frac{e}{p} \big]^{-1}$ 对比，立得：
$$T_v = \frac{T}{1 - (1 - \varepsilon)\frac{e}{p}} = \frac{T}{1 - 0.378 \frac{e}{p}}$$

### 4.2 级数展开与实用工程近似
在大气实际条件下，水汽压通常远小于总气压，即 $\frac{e}{p} \ll 1$（通常 $\frac{e}{p} < 0.03$）。利用泰勒一阶展开 $(1-x)^{-1} \approx 1 + x$：
$$T_v \approx T \left( 1 + 0.378 \frac{e}{p} \right)$$

### 4.3 虚温用比湿 $q$ 和混合比 $w$ 表示
气象观测中常用水汽混合比 $w = \frac{m_v}{m_d} = \frac{\rho_v}{\rho_d} = \varepsilon \frac{e}{p-e}$，以及比湿 $q = \frac{m_v}{m} = \frac{\rho_v}{\rho} = \varepsilon \frac{e}{p}$：
$$T_v \approx T (1 + 0.608 q) \approx T (1 + 0.608 w)$$

> **物理本质剖析**：
> 1. 因为水汽分子量（$18\,\text{g/mol}$）显著轻于干空气平均分子量（$28.97\,\text{g/mol}$），相同温压条件下，**水汽越多，湿空气密度越小**（即“湿空气比干空气轻”）。
> 2. 要让相同气压下的干空气达到如此轻的密度，必须将干空气加热膨胀。因此在相同物理温度下，**虚温总是高于（或等于）真实物理温度**：
>    $$T_v \ge T$$
> 3. 在浮力分析中，虚温直接决定了气块受到的阿基米德浮力，虚温的梯度直接对应浮力加速度。

---

## 五、水汽参量完整族谱及相互换算

| 水汽参量名称 | 符号 | 物理定义式 | 常用单位 | 相互转换核心公式 |
| :--- | :--- | :--- | :--- | :--- |
| **水汽压** | $e$ | 湿空气中水汽产生的独立分压 | $\text{hPa}$ 或 $\text{Pa}$ | $e = \frac{p \cdot w}{\varepsilon + w} \approx \frac{p \cdot q}{\varepsilon}$ |
| **水汽密度 (绝对湿度)** | $\rho_v$ | 单位体积湿空气中所含水汽质量 | $\text{g}\cdot\text{m}^{-3}$ 或 $\text{kg}\cdot\text{m}^{-3}$ | $\rho_v = \frac{e}{R_v T} = 217 \frac{e\,(\text{hPa})}{T\,(\text{K})}$ |
| **混合比** | $w$ | 水汽质量与干空气质量之比 | $\text{g}\cdot\text{kg}^{-1}$ | $w = \varepsilon \frac{e}{p - e} \approx 0.622 \frac{e}{p}$ |
| **比湿** | $q$ | 水汽质量与湿空气总质量之比 | $\text{g}\cdot\text{kg}^{-1}$ | $q = \frac{w}{1 + w} \approx \varepsilon \frac{e}{p}$ |
| **相对湿度** | $RH$ | 实际水汽压与同温度饱和水汽压之比 | $\%$ | $RH = \frac{e}{E(T)} \times 100\%$ |
| **露点温度** | $T_d$ | 气压和水汽含量不变时冷却至饱和的温度 | ${}^\circ\text{C}$ 或 $\text{K}$ | $E(T_d) = e$ |

---

## 六、典型例题与期末考点剖析

### 【例题 1】气块虚温与密度精确计算
**题目**：某测站测得地面气压 $p = 1000\,\text{hPa}$，气温 $t = 27\,{}^\circ\text{C}$，相对湿度 $RH = 80\%$。已知该温度下的饱和水汽压 $E(27\,{}^\circ\text{C}) = 35.67\,\text{hPa}$。
求：
1. 该地空气的实际水汽压 $e$；
2. 湿空气的虚温 $T_v$；
3. 该湿空气的实际密度 $\rho$。

**【详细推导与求解】**：
1. **求实际水汽压 $e$**：
   $$e = RH \times E(T) = 0.80 \times 35.67\,\text{hPa} = 28.536\,\text{hPa}$$
2. **求绝对温度与虚温 $T_v$**：
   绝对温度 $T = 27 + 273.15 = 300.15\,\text{K}$。
   代入虚温公式：
   $$T_v = T \left( 1 + 0.378 \frac{e}{p} \right) = 300.15 \times \left( 1 + 0.378 \times \frac{28.536}{1000} \right)$$
   $$T_v = 300.15 \times (1 + 0.010787) \approx 303.39\,\text{K} \quad (30.24\,{}^\circ\text{C})$$
   虚温修正量 $\Delta T = T_v - T = 3.24\,\text{K}$，在热带与低空高温高湿环境下，虚温修正显著不可忽略！
3. **求湿空气密度 $\rho$**：
   直接利用虚温状态方程：
   $$\rho = \frac{p}{R_d T_v} = \frac{1000 \times 10^2\,\text{Pa}}{287.05\,\text{J}\cdot\text{kg}^{-1}\cdot\text{K}^{-1} \times 303.39\,\text{K}} \approx 1.1482\,\text{kg}\cdot\text{m}^{-3}$$

---

## 习题与思考题（课后巩固）
1. 试从微观分子量差异出发，定性解释为什么夏季雷雨前闷热潮湿的天气，高尔夫球或棒球飞行的空气阻力反而略微变小？
2. 证明：比湿 $q$ 与混合比 $w$ 的关系式为 $q = \frac{w}{1+w}$，并在什么条件下可以近似认为 $q \approx w$？
3. 若某气层上界气压为 $850\,\text{hPa}$，下界气压为 $1000\,\text{hPa}$，平均温度为 $15\,{}^\circ\text{C}$，平均比湿为 $10\,\text{g/kg}$，计算该气层的平均虚温及考虑虚温修正对厚度计算的影响。
