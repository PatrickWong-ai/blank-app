import streamlit as st
from clips import Environment
import textwrap

# ---------------------------------------------------------
# Expert System – Create Environment + Rules
# ---------------------------------------------------------
def create_environment():

    env = Environment()

    clips_code = textwrap.dedent("""
    (deftemplate symptom
        (slot name)
        (slot value))

    (deftemplate result
        (slot diagnosis))

    (defrule covid-possible
        (symptom (name fever) (value yes))
        (symptom (name cough) (value yes))
        =>
        (assert (result (diagnosis "Possible COVID-19 infection. Please test and isolate."))))

    (defrule covid-unlikely
        (symptom (name fever) (value no))
        (symptom (name cough) (value no))
        =>
        (assert (result (diagnosis "Unlikely COVID-19 from these symptoms."))))
    """)

    env.build(clips_code)
    return env


# ---------------------------------------------------------
# Run Expert System
# ---------------------------------------------------------
def run_expert_system(has_fever: bool, has_cough: bool) -> str:
    env = create_environment()
    env.reset()

    fever_value = "yes" if has_fever else "no"
    cough_value = "yes" if has_cough else "no"

    env.assert_string(f"(symptom (name fever) (value {fever_value}))")
    env.assert_string(f"(symptom (name cough) (value {cough_value}))")

    env.run()

    for fact in env.facts():
        if fact.template.name == "result":
            return fact["diagnosis"]

    return "No rule fired."


# ---------------------------------------------------------
# Streamlit UI
# ---------------------------------------------------------
def main():

    st.title("🩺 COVID-19 Diagnosis Expert System (CLIPS + Streamlit)")

    st.write("Simple CLIPS expert system for education only.")

    fever = st.radio("Do you have fever?", ["No", "Yes"], horizontal=True)
    cough = st.radio("Do you have cough?", ["No", "Yes"], horizontal=True)

    has_fever = fever == "Yes"
    has_cough = cough == "Yes"

    if st.button("Diagnose"):
        result = run_expert_system(has_fever, has_cough)
        st.success(result)


if __name__ == "__main__":
    main()
