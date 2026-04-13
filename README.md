# Thermodynamics Exam Cheat Sheet (Chapters 1 & 2)

## 1. Thermodynamic Systems & Variables
*   **System Types**:
    *   **Open**: Exchanges energy and matter.
    *   **Closed**: Exchanges energy ONLY (mass $\Delta m = 0$).
    *   **Isolated**: Exchanges NEITHER energy nor matter ($W = 0$, $Q = 0$).
*   **State Variables**: ($n$, $p$, $V$, $T$)
    *   **Extensive** (Depends on system size, additive): Volume ($V$), Amount of substance ($n$), mass ($m$).
    *   **Intensive** (Independent of size, not additive): Temperature ($T$), Pressure ($p$), Density ($\rho$).
*   **Thermodynamic Equilibrium**: Macroscopic properties are constant over time. Requires Thermal (uniform $T$), Mechanical (uniform $p$), and Chemical equilibrium.

## 2. Ideal and Real Gases
*   **Ideal Gas Law**: $pV = nRT$
    *   $R = 8.314 \text{ J/(mol}\cdot\text{K)}$
    *   **STP (Standard Temperature & Pressure)**: $T = 0^\circ\text{C} = 273.15\text{ K}$, $p = 1\text{ atm} = 101325\text{ Pa}$. Molar volume $V_m = 22.4 \text{ L/mol}$.
*   **Real Gas (Van der Waals)**: $(p + a\frac{n^2}{V^2})(V - nb) = nRT$
    *   Accounts for molecular volume ($b$) and attractive forces ($a$).

## 3. Thermodynamic Transformations & Clapeyron Diagram
*   **Types of Processes**:
    *   **Isobaric**: Constant internal pressure ($p = const$).
    *   **Monobaric**: Constant external pressure ($p_{ext} = const$).
    *   **Isochoric**: Constant volume ($V = const$).
    *   **Isothermal**: Constant internal temperature ($T = const$).
    *   **Quasi-static**: A very slow process proceeding through a continuous succession of equilibrium states ($p_{ext} \approx p_{sys}$).
*   **Clapeyron Diagram (p-V)**:
    *   **X-axis** = Volume $V$, **Y-axis** = Pressure $p$.
    *   **Isobaric** = Horizontal line. **Isochoric** = Vertical line. **Isothermal** = Hyperbola.
    *   **Area**: Work exchanged is the opposite of the area under the curve ($W = -\int p dV$).
    *   **Cycles**: Clockwise = Engine / Motor ($W_{tot} < 0$), Counter-clockwise = Receiver / Refrigerator ($W_{tot} > 0$).

## 4. Work Exchange (Mechanical & Electrical)
*   **Mechanical Work (Pressure forces)**:
    *   General formula: $W = -\int_{V_A}^{V_B} p_{ext} dV$
    *   **Isochoric**: $W = 0$
    *   **Isobaric / Monobaric**: $W = -p_{ext}(V_B - V_A) = -p_{ext} \Delta V$
    *   **Isothermal (Ideal Gas, Quasi-static)**: $W = -\int \frac{nRT}{V} dV = -nRT \ln\left(\frac{V_B}{V_A}\right) = nRT \ln\left(\frac{p_B}{p_A}\right)$
*   **Electrical Work**:
    *   Joule heating from a resistor: $W_{elec} = P_J \Delta t = U I \Delta t = R I^2 \Delta t$

## 5. Heat Transfer & Phase Changes
*   **Sensible Heat** (Causes Temperature Change):
    *   $Q_s = m c \Delta T$ (where $c$ is specific heat capacity in $\text{J/(kg}\cdot\text{K)}$).
    *   Or $Q_s = n c_{m} \Delta T$ (where $c_m$ is molar heat capacity).
*   **Latent Heat** (Causes Phase Change at Constant Temperature):
    *   $Q_L = m L$ (where $L$ is specific latent heat in $\text{J/kg}$).
    *   Types: $L_f$ (fusion: solid $\to$ liquid), $L_v$ (vaporization: liquid $\to$ gas), $L_s$ (sublimation: solid $\to$ gas).

## 6. The First Law of Thermodynamics
*   **Statement**: The variation of internal energy $\Delta U$ of a closed system is equal to the sum of work and heat exchanged.
    *   $\Delta U = W + Q$
    *   *Note: Internal energy $U$ is a state function. $\Delta U$ depends ONLY on initial and final states, not the path taken!*
*   **Sign Convention ("Banker's Rule")**:
    *   Energy Received BY the system $\implies$ Positive ($> 0$).
    *   Energy Lost / Given BY the system $\implies$ Negative ($< 0$).
*   **Special Cases**:
    *   **Isolated system**: $W = 0$, $Q = 0 \implies \Delta U = 0$
    *   **Cyclic transformation**: $\Delta U = 0 \implies W = -Q$
    *   **Isochoric transformation**: $W = 0 \implies \Delta U = Q_V$
    *   **Adiabatic transformation**: $Q = 0 \implies \Delta U = W$

## 7. Joule's Laws (Internal Energy & Enthalpy)
*   **First Joule Law**: For an ideal gas, Internal Energy ($U$) depends ONLY on Temperature.
    *   $\Delta U = C_V \Delta T = n c_{V,mol} \Delta T = m c_v \Delta T$
    *   *Applies to ANY transformation for an ideal gas!*
*   **Second Joule Law**: For an ideal gas, Enthalpy ($H = U + pV$) depends ONLY on Temperature.
    *   In an **isobaric** process, heat exchanged is the variation of enthalpy: $Q_p = \Delta H$
    *   $\Delta H = C_p \Delta T = n c_{p,mol} \Delta T = m c_p \Delta T$
*   **Mayer's Relation**: $C_p - C_V = nR$
    *   For Monoatomic Ideal Gas: $C_V = \frac{3}{2} nR$, $C_p = \frac{5}{2} nR$
    *   For Diatomic Ideal Gas (e.g., $N_2, O_2$, air): $C_V = \frac{5}{2} nR$, $C_p = \frac{7}{2} nR$
*   **Dense Phases (Liquids/Solids)**: Volume variation is negligible ($\Delta V \approx 0$).
    *   $C_p \approx C_V \implies \Delta H \approx \Delta U$

---

## 8. TD1 & TD2 Tips: How to Solve the Exercises
*(Remember: Laplace’s Law $pV^\gamma = const$ is omitted for this exam.)*

1.  **Crucial Unit Conversions**:
    *   **Temperature**: $T (K) = T (^\circ C) + 273.15$ (Always use Kelvin for $pV = nRT$!).
    *   **Pressure**: $1 \text{ bar} = 10^5 \text{ Pa}$. $1 \text{ atm} = 101325 \text{ Pa}$.
    *   **Volume**: $1 \text{ m}^3 = 1000 \text{ L}$. $1 \text{ L} = 1 \text{ dm}^3 = 10^{-3} \text{ m}^3$.
2.  **General Cycle / Transformation Strategy**:
    *   **Step A**: Write down the state variables $(p, V, T)$ for each state (State 1, State 2, etc.). Use $pV = nRT$ to deduce the missing variable.
    *   **Step B**: Identify the process (isobaric, isochoric, isothermal, adiabatic).
    *   **Step C**: Calculate $\Delta U$ using the First Joule Law ($\Delta U = n C_{V,mol} \Delta T$). This works for an ideal gas regardless of the path.
    *   **Step D**: Calculate $W$ using the proper formula based on the process type.
    *   **Step E**: Deduce $Q$ logically using the First Law: $Q = \Delta U - W$.
3.  **Sanity Checks**:
    *   Does the gas expand ($V_2 > V_1$)? Then Work $W$ must be negative!
    *   Is the system heated at constant volume? Then $W = 0$, and both $T$ and $p$ must increase.
    *   Is it an adiabatic compression? Then $Q = 0$ and $W > 0 \implies \Delta U > 0$, so Temperature MUST increase. Even without Laplace's law, you can compute $W$ if you know the temperatures, because $W = \Delta U = n C_V \Delta T$.
