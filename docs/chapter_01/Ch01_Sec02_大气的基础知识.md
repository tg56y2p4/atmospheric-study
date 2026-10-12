---
chapter: 1
section: 1.2
title: 大气的基础知识
date: 2026-10-12
status: completed
source_doc_id: 1CxpOg81Hg58HKBeu8BNTwGQDPvAosu8ZfbTexmr7l9w
target_course: 南京信息工程大学本科期末 / 806 大气物理学考研高分强化
textbook: 银燕、刁一伟等编著《大气物理学》（气象出版社，2018年版）
---

# 南京信息工程大学《大气物理学》精讲讲义

## 第 1 章 绪论与大气基础知识 · 1.2 大气的基础知识（全本深度讲义）

> **课程目标**：南京信息工程大学本科期末考试 / 806 大气物理学考研高分强化  
> **教材依据**：银燕、刁一伟等编著《大气物理学》（气象出版社，2018年版）

---

## 一、知识框架与重点

本小节覆盖 1.2.1 至 1.2.5 全部子节：
- 大气的化学构成与质量分布
- 气体状态方程全族与虚温严密推导
- 大气湿度的全部表示方法及相互转换
- 克劳修斯-克拉佩龙方程与相变平衡
- 大气的垂直分层与物理特性

---

## 二、核心物理机制与严密公式推导

#### 1. 气体状态方程全族 (State Equation Family)

大气在通常温压条件下可精确视为理想气体。状态方程具有多种表达形式：

- **微观分子形式**：
  $$p = n k_B T$$
  其中 $n$ 为数密度 $(\text{m}^{-3})$，玻尔兹曼常数 $k_B = 1.38065 \times 10^{-23}\,\text{J/K}$。

- **摩尔形式**：
  $$p V = n_m R^* T$$
  摩尔数 $n_m = \frac{m}{M}$，通用气体常数 $R^* = 8.31447\,\text{J/(mol}\cdot\text{K)}$。

- **比容形式**：
  $$p \alpha = R T$$
  比容 $\alpha = \frac{1}{\rho}\,(\text{m}^3/\text{kg})$，特定气体常数 $R = \frac{R^*}{M}$。

- **密度形式**：
  $$p = \rho R T$$

**具体大气成分常数**：
- 干空气平均分子量 $M_d \approx 28.966\,\text{g/mol}$，干空气比气体常数：
  $$R_d = \frac{R^*}{M_d} = 287.05\,\text{J/(kg}\cdot\text{K)}$$
- 水汽分子量 $M_v = 18.015\,\text{g/mol}$，水汽气体常数：
  $$R_v = \frac{R^*}{M_v} = 461.51\,\text{J/(kg}\cdot\text{K)}$$
- 两气体常数之比（无量纲常数）：
  $$\varepsilon = \frac{M_v}{M_d} = \frac{R_d}{R_v} \approx 0.622$$
  倒数：
  $$\frac{1}{\varepsilon} = \frac{M_d}{M_v} \approx 1.608$$

---

#### 2. 湿空气表观气体常数与虚温 (Virtual Temperature) 全套严密推导

湿空气是干空气与水汽的混合气体。根据道尔顿分压定律：总压 $p = p_d + e$，总密度 $\rho = \rho_d + \rho_v$。

展开总密度：
$$\rho = \frac{p_d}{R_d T} + \frac{e}{R_v T} = \frac{p - e}{R_d T} + \frac{e}{R_v T} = \frac{p - (1 - \varepsilon)e}{R_d T}$$

若将湿空气当作具有表观气体常数 $R_m$ 的气体：$p = \rho R_m T$，可求得：
$$R_m = R_d (1 + 0.608 q)$$

为保持干空气气体常数 $R_d$ 不变，引入**虚温** $T_v$ 使得：
$$p = \rho R_d T_v$$

- **精确解析解**：
  $$T_v = \frac{T}{1 - (1 - \varepsilon)\frac{e}{p}} = \frac{T}{1 - 0.378 \frac{e}{p}}$$

- **一阶级数展开（基于水汽压 $e$）**：  
  因 $e \ll p$，利用 $(1 - x)^{-1} \approx 1 + x$，得：
  $$T_v \approx T \left( 1 + 0.378 \frac{e}{p} \right)$$

- **比湿 $q$ 表达形式**：  
  代入 $q \approx \varepsilon \frac{e}{p}$，计算系数：
  $$\frac{1 - \varepsilon}{\varepsilon} = \frac{1}{\varepsilon} - 1 = \frac{28.966 - 18.015}{18.015} = 0.608$$
  因此：
  $$T_v = T (1 + 0.608 q)$$

- **混合比 $w$ 表达形式**：  
  因 $q = \frac{w}{1 + w} \approx w$，故：
  $$T_v \approx T (1 + 0.608 w)$$

- **虚温增量 $\Delta T_v$**：
  $$\Delta T_v = T_v - T = 0.608 q T$$
  常温（$q \approx 15\,\text{g/kg}$，$T \approx 300\,\text{K}$）下，$\Delta T_v$ 可达 $2 \sim 3\,\text{K}$，在浮力计算与静力学方程中不可忽略。

---

#### 3. 大气湿度参数方程全集与相互转换

- **水汽压 $e$ 与饱和水汽压 $E$**：水汽产生的分压 $(\text{hPa})$。
- **绝对湿度 $a\,(\text{g/m}^3)$**：
  $$a = \rho_v = \frac{e}{R_v T}$$
  单位换算推导：
  $$a = \left[ \frac{e \cdot 10^2}{461.51 \cdot T} \right] \cdot 10^3 = \frac{10^5}{461.51} \cdot \frac{e}{T} = 216.7 \frac{e}{T}$$
- **比湿 $q\,(\text{g/g}$ 或 $\text{g/kg})$**：
  $$q = \frac{m_v}{m_d + m_v} = \frac{\rho_v}{\rho} = \frac{\varepsilon \frac{e}{T}}{\frac{(p - e) + \varepsilon e}{T}} = \frac{\varepsilon e}{p - (1 - \varepsilon)e} \approx \varepsilon \frac{e}{p}$$
- **混合比 $w\,(\text{g/g}$ 或 $\text{g/kg})$**：
  $$w = \frac{m_v}{m_d} = \frac{\rho_v}{\rho_d} = \frac{\varepsilon e}{p - e}$$
- **$q$ 与 $w$ 的互算公式**：
  $$q = \frac{w}{1 + w}, \quad w = \frac{q}{1 - q}$$
- **相对湿度 $f\,(\%)$**：
  $$f = \frac{e}{E} \times 100\% \approx \frac{w}{w_s} \times 100\% \approx \frac{q}{q_s} \times 100\%$$
- **饱和差 $d\,(\text{hPa})$**：
  $$d = E - e = E (1 - f)$$
- **露点温度 $T_d\,({}^\circ\text{C}$ 或 $\text{K})$**：气压不变且水汽含量未变时，空气冷却至达到饱和时的温度。当 $e = E(T_d)$ 时成立。
- **劳伦斯 (Lawrence) 近似公式**：相对湿度与露点差 $(T - T_d)$ 关系：
  $$f \approx 100 - 5 (T - T_d) \quad (当\ f > 50\%\ 时精度极高)$$

---

#### 4. 克劳修斯-克拉佩龙方程 (Clausius-Clapeyron) 与冰水面饱和水汽压

由热力学第一与第二定律推导相变平衡方程：
$$\frac{dE}{dT} = \frac{L}{T (\alpha_v - \alpha_l)}$$

因 $\alpha_v \gg \alpha_l$ 且 $\alpha_v = \frac{R_v T}{E}$，可得微分形式：
$$\frac{d \ln E}{dT} = \frac{L}{R_v T^2}$$

积分形式（假设相变潜热 $L$ 为常数）：
$$E(T) = E_0 \exp\left[ \frac{L}{R_v} \left( \frac{1}{T_0} - \frac{1}{T} \right) \right]$$

气象学常用经验公式（马格努斯-泰藤斯 Magnus-Tetens）：
- **水面**：$E_w(t) = 6.112 \exp\left[ \frac{17.67 t}{t + 243.5} \right] \quad (t\ 以\ {}^\circ\text{C}\ 计)$
- **冰面**：$E_i(t) = 6.112 \exp\left[ \frac{22.46 t}{t + 272.62} \right]$

**冰水面差异与贝吉隆过程 (Bergeron Process)**：  
由于冰升华潜热 $L_s$ 大于水汽化潜热 $L_v$，在负温 $(t < 0\,{}^\circ\text{C})$ 下，水分子克服分子间力脱离液面比脱离冰面更容易，故 **$E_w > E_i$**（在 $-12 \sim -15\,{}^\circ\text{C}$ 处 $\Delta E = E_w - E_i$ 达到极大值）。在冷云中，当实际水汽压 $e$ 满足 $E_i < e < E_w$ 时，环境对水滴未饱和（水滴蒸发），对冰晶过饱和（水汽凝华至冰晶），导致冰晶快速长大、水滴蒸发消失。

---

#### 5. 大气垂直分层与结构 (Vertical Structure)

大气总质量 $M_{\text{atm}} \approx 5.27 \times 10^{18}\,\text{kg}$。按温度垂直递减率 $\gamma = -\frac{dT}{dz}$ 可分为五层：

- **对流层 (Troposphere)**：平均厚度赤道 $17 \sim 18\,\text{km}$、中纬度 $10 \sim 12\,\text{km}$、极地 $8 \sim 9\,\text{km}$。集中了全大气 **$78\%$ 以上的质量** 和几乎全部水汽。平均温度递减率 $\gamma \approx 6.5\,{}^\circ\text{C/km}$，对流运动旺盛，天气现象复杂。
- **平流层 (Stratosphere)**：对流层顶至 $50 \sim 55\,\text{km}$。集中了大气中大部分臭氧 $(\text{O}_3)$，在 $20 \sim 30\,\text{km}$ 形成臭氧层。$\text{O}_3$ 强烈吸收太阳紫外辐射产生增温，形成深厚逆温（上暖下冷），大气稳定，以平流运动为主。
- **中间层 (Mesosphere)**：平流层顶至 $85\,\text{km}$。无 $\text{O}_3$ 加热，$\text{CO}_2$ 强辐射冷却，温度随高度急剧下降，顶部达到全大气最低温（约 $-90\,{}^\circ\text{C} / 180\,\text{K}$）。
- **热层 (Thermosphere)**：中间层顶至 $800\,\text{km}$。$\text{O}_2$、$\text{N}_2$ 吸收极紫外辐射强烈增温，温度可达上千开尔文，气体处于高度电离状态（电离层）。
- **散逸层 (Exosphere)**：$800\,\text{km}$ 以上，气体极其稀薄，分子平均自由程极大，轻气体分子（$\text{H}$、$\text{He}$）可逃逸入行星际空间。

---

## 三、典型例题与计算标准

**综合计算例题**：  
某气象站测得气压 $p = 1000.0\,\text{hPa}$，温度 $t = 27.0\,{}^\circ\text{C}$ ($T = 300.15\,\text{K}$)，相对湿度 $f = 80\%$。已知 $27\,{}^\circ\text{C}$ 时饱和水汽压 $E = 35.67\,\text{hPa}$。  
求：
1. 实际水汽压 $e$；
2. 混合比 $w$ 与比湿 $q$；
3. 绝对湿度 $a$；
4. 虚温 $T_v$；
5. 真实湿空气密度 $\rho$ 并与忽略湿度计算的密度比较。

**标准步骤与解答**：
1. **实际水汽压**：
   $$e = f \cdot E = 0.80 \times 35.67\,\text{hPa} = 28.54\,\text{hPa}$$
2. **混合比与比湿**：
   $$w = \frac{\varepsilon e}{p - e} = \frac{0.622 \times 28.54}{1000.0 - 28.54} = 0.01827\,\text{kg/kg} = 18.27\,\text{g/kg}$$
   $$q = \frac{w}{1 + w} = \frac{0.01827}{1.01827} = 0.01794\,\text{kg/kg} = 17.94\,\text{g/kg}$$
3. **绝对湿度**：
   $$a = 216.7 \left( \frac{e}{T} \right) = 216.7 \times \left( \frac{28.54}{300.15} \right) = 20.60\,\text{g/m}^3$$
4. **虚温**：
   $$T_v = T (1 + 0.608 q) = 300.15 \times (1 + 0.608 \times 0.01794) = 303.42\,\text{K} \quad (30.27\,{}^\circ\text{C})$$
5. **真实密度与误差比较**：
   $$\rho = \frac{p}{R_d T_v} = \frac{100000\,\text{Pa}}{287.05\,\text{J/(kg}\cdot\text{K)} \times 303.42\,\text{K}} = 1.1482\,\text{kg/m}^3$$
   若误用实际温度 $T$ 计算干空气密度：
   $$\rho_{\text{dry}} = \frac{p}{R_d T} = \frac{100000}{287.05 \times 300.15} = 1.1607\,\text{kg/m}^3$$
   相对误差达：
   $$\frac{1.1607 - 1.1482}{1.1482} \approx +1.09\% \quad (\text{高估了空气质量})$$

---

## 四、南信大考研与期末重点复习题

#### 1. 名词解释
- **虚温**
- **比湿**
- **露点温度**
- **饱和差**
- **均质层与非均质层**
- **贝吉隆过程**

#### 2. 严密证明题
1. 从道尔顿分压定律出发，严格推导虚温公式 $T_v = T(1 + 0.608q)$，并说明常数 $0.608$ 的物理本质。
2. 导出绝对湿度计算公式 $a = 216.7\left(\frac{e}{T}\right)$，指出系数 $216.7$ 的来源与单位约束。

#### 3. 简答题
1. 为什么湿空气比干空气轻？请从微观分子和宏观密度两方面解释。
2. 简述对流层的主要物理特征及其高度在纬度与季节上的变化规律。
3. 为什么平流层呈现“上暖下冷”的逆温结构？这对其大气运动有何影响？
4. 在负温条件下，为什么水面饱和水汽压 $E_w$ 恒大于冰面饱和水汽压 $E_i$？这在降水形成中有何重要意义？
