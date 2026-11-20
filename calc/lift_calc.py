#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Детермінований розрахунок підйомної сили (OCL-демо, потік G).

Формула НЕ «в пам'яті» моделі — вона взята з бази знань:
  sources/nasa-glenn/lift-equation.md, рядок L12:
      L = Cl · (ρ·V²/2) · A
Формула зворотної перевірки:
  sources/nasa-glenn/lift-coefficient.md, рядок L13:
      Cl = L / (q·A)

Запуск: python calc/lift_calc.py
"""
import json, os, sys

# --- вхідні умови (приклад: легкий літак Cessna-класу) ---
COND = {"Cl": 0.6, "rho_kg_m3": 1.225, "V_m_s": 50.0, "A_m2": 16.2}

def lift(cl, rho, v, a):
    """L = Cl · (ρ·V²/2) · A   [nasa-glenn/lift-equation.md:L12]"""
    return cl * (rho * v**2 / 2.0) * a

def cl_check(L, rho, v, a):
    """Cl = L / (q·A), q = ½ρV²   [nasa-glenn/lift-coefficient.md:L13]"""
    q = 0.5 * rho * v**2
    return L / (q * a)

def main():
    L = lift(cl=COND["Cl"], rho=COND["rho_kg_m3"], v=COND["V_m_s"], a=COND["A_m2"])
    cl_back = cl_check(L, COND["rho_kg_m3"], COND["V_m_s"], COND["A_m2"])
    q = 0.5 * COND["rho_kg_m3"] * COND["V_m_s"] ** 2
    out = {
        "умови": COND,
        "динамічний_тиск_q_Па": round(q, 2),
        "підйомна_сила_L_Н": round(L, 1),
        "підйомна_сила_L_kgf": round(L / 9.80665, 1),
        "зворотна_перевірка_Cl": round(cl_back, 6),
        "джерела": [
            "sources/nasa-glenn/lift-equation.md:L12",
            "sources/nasa-glenn/lift-coefficient.md:L13",
        ],
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    assert abs(cl_back - COND["Cl"]) < 1e-9, "зворотна перевірка не зійшлась"
    print("OK: зворотна перевірка зійшлась")

if __name__ == "__main__":
    main()
