from molmass import Formula, FormulaError # USE COMMA TO SEPARATE MULTIPLE VALUES YOU WANT TO IMPORT
import streamlit as st
from pint import UnitRegistry, DimensionalityError

# functions
def unit_conversion(value, orig_unit, new_unit):
    ureg = UnitRegistry()
    Q_ = ureg.Quantity
    initial = (float(value) * ureg(orig_unit))  # using input in this allows you to use user generated response since it allows string parsing.
    final = Q_(initial, new_unit)
    return final
def molar_mass(comp):
        formula = Formula(comp)
        molarmass = formula.mass
        return molarmass

# classes
class Molarity:
    def get_M(self, moles, volume):  # need self parameter to indicate as a method, otherwise it can only be used inside the class.
        return moles/volume
    def get_moles(self, value, comp):
        molarmass = molar_mass(comp)
        return value/molarmass
    def get_liters(self, value, unit):
        liters = unit_conversion(value, unit, "liter")
        return liters

class Molality(Molarity):  # don't need parenthesis if you're not doing inheritance.
    def get_m(self, moles, mass):
        return moles/mass
    def m_to_kg(self, moles, solutecomp):
        formula = Formula(solutecomp)
        molarmass = formula.mass
        return moles*molarmass*1000


st.set_page_config(page_title = "General Chemistry 2 Calculator", layout = "wide", initial_sidebar_state = "collapsed")
st.title("_M&m_: A Molarity and Molality Calculator")
st.subheader("Created by Ezra Del Rosario")
st.caption("""
Personal coding project for practice. Integrates knowledge from Chemistry classes and coding tutorials.

""")
st.markdown("____"*50)
user_inp = st.selectbox("General Chemistry 2 Calculator: ", ["Molarity", "Molality"], key = "ones")


# SYSTEM
try:
    if user_inp == "Molarity":
        M_solutecomp = str(st.text_input("Enter the correct chemical formula for the solute", key="twos"))
        M_soluteval = str(st.text_input("Enter the value for the solute (please separate the value and the unit)", key="threes")).split(" ")
        M_solutionval = str(st.text_input("Enter the value of the solution (please separate the value and the unit)", key="fives")).split(" ")
        M_soluteval[0] = float(M_soluteval[0])
        M_soluteval[1] = str(M_soluteval[1]).lower()
        M_solutionval[0] = float(M_solutionval[0])
        M_solutionval[1] = str(M_solutionval[1]).lower()
        molarity = Molarity()
        if M_soluteval[1] in ["mol", "moles", "mole"]:
            if M_solutionval[1] in ["liters", "liter", "l"]:
                st.success(molarity.get_M(M_soluteval[0], M_solutionval[0]))
            elif not M_solutionval[1] in ["liters", "liter", "l"]:
                new_unit = str(unit_conversion(M_solutionval[0], M_solutionval[1], "liters")).split()
                st.success(molarity.get_M(M_soluteval[0], float(new_unit[0])))
        elif not M_soluteval[1] in ["mol", "moles", "mole"]:  # not is used after if or elif
            if not M_soluteval[1] in ["g", "grams", "gram"]:
                M_solute_new_unit = str(unit_conversion(M_soluteval[0], M_soluteval[1], "gram")).split()
                M_solutemoles = molarity.get_moles(float(M_solute_new_unit[0]), M_solutecomp)  # the variables made in the if statments are exclusive to that block.
            else:
                M_solutemoles = molarity.get_moles(M_soluteval[0], M_solutecomp) # since 
            if M_solutionval[1] in ["liters", "liter"]:
                st.success(molarity.get_M(M_solutemoles, M_solutionval[0]))
            elif not M_solutionval[1] in ["liters", "liter"]:
                new_unit = str(unit_conversion(M_solutionval[0], M_solutionval[1], "liter")).split()
                st.success(molarity.get_M(M_solutemoles, float(new_unit[0])))
    if user_inp == "Molality":
            m_solutecomp = str(st.text_input("Enter the correct chemical formula for the solute ", key="two"))
            m_soluteval = str(st.text_input("Enter the value for the solute (please separate the value and the unit)", key="three")).split()  # default set to whitespace
            m_solventcomp = str(st.text_input("Enter the correct chemical formula for the solvent ", key="four"))
            m_solventval = str(st.text_input("Enter the value for the solvent (please separate the value and the unit)", key="five")).split()
            m_soluteval[0] = float(m_soluteval[0])
            m_soluteval[1] = str(m_soluteval[1]).lower()
            m_solventval[0] = float(m_solventval[0])
            m_solventval[1] = str(m_solventval[1]).lower()
            molality = Molality()
            if m_soluteval[1] in ["mol", "moles", "mole"]:
                if m_solventval[1] in ["kilogram", "kilograms", "kg"]:  # for nested if, it is not exclusive to the first condition. you can do whatever you want, whatever is necessary
                    st.success(molality.get_m(m_soluteval[0], m_solventval[0]))
                elif m_solventval[1] in ["mol", "moles", "mole"]:
                    new_unit = molality.m_to_kg(m_solventval[0], m_solventcomp)
                    st.success(molality.get_m(m_soluteval[0], new_unit))
                elif not m_solventval[1] in ["kilogram", "kilograms", "kg"]:
                    new_unit = str(unit_conversion(m_solventval[0], m_solventval[1], "kilogram")).split()
                    st.success(molality.get_m(m_soluteval[0], float(new_unit[0])))
            elif m_soluteval[1] not in ["mol", "moles", "mole"]: 
                if m_soluteval[1].lower() not in ["g", "grams", "gram"]:
                    m_solute_new_unit = str(unit_conversion(m_soluteval[0], m_soluteval[1], "gram")).split()
                    m_solutemoles = molality.get_moles(float(m_solute_new_unit[0]), m_solutecomp)
                else:
                    m_solutemoles = molality.get_moles(m_soluteval[0], m_solutecomp)
                if m_solventval[1] in ["kilograms", "kilogram", "kg"]:
                    st.success(molality.get_m(m_solutemoles, m_solventval[0]))
                elif not m_solventval[1] in ["kilograms", "kilogram", "kg"]:
                    new_unit = str(unit_conversion(m_solventval[0], m_solventval[1], "kilogram")).split()
                    st.success(molality.get_m(m_solutemoles, float(new_unit[0])))
except FormulaError:
    st.error("Make sure to enter a correct chemical formula.")
except DimensionalityError:
    st.error("Make sure to enter a proper unit.")
except IndexError:
    st.error("Make sure to separate the value and the unit with a space.")
except ValueError:
    st.error("Enter a correct input.")
else:
    st.balloons()

# TURN [0] INTO A STRING TO SPLIT FIRST THEN FLOAT() THAT'S THE ONLY REASON WE TURN IT INTO A STRING IS TO USE THE DOT SYNTAX .SPLIT() TO IT.





































# variables inside if statements are local to that if statement.
# when a function yields two values, you can separate those values by assigning different variables names respectively

# WE STILL KNOW HOW TO CODE, IT DOESN'T FEEL LIKE THAT ANYMORE BECAUSE WE HAVE GOTTEN SO USED TO IT
# print("right?"*2)  # WE ABSOLUTELY KNOW AND WE CAN RECALL THE FUNDAMENTALS, WATCH IF NECESSARY.


# Tama naman lahat ng cinode mo DON'T FORGET, THIS IS BECAUSE WE ARE NOT PRACTICING AS OFTEN PERO TAMA NAMAN AND IT IS WORKING




# finish numpy first para full attention dito sa project. please please please, yes yes then after ng project na to yung intermediate projects na, then intermediate tuts

    
    