import streamlit as st
from clips import Environment   # Correct import (NO clips.Environment usage)


# ---------------------------------------------------------
# Expert System (ES) – CLIPS Environment and Rules
# ---------------------------------------------------------
def create_environment():
    """
    Create and return a CLIPS Environment with templates and rules.
    """

    env = Environment()

    # Define templates & rules in CLIPS language
    clips_code = """
        ;; Template for symptoms
        (deftemplate symptom
            (slot name)
            (slot value))

        ;; Template for results
        (deftemplate result
            (slot diagnosis))

        ;; Rule 1: fever = yes AND cough = yes
        (defrule covid-possible
            (symptom (name fever) (value yes))
            (symptom (name cough) (value yes))
            =>
            (assert (result (diagnosis
                "Possible COVID-19 infection. Please take a COVID-19 test and self-isolate."))))

        ;; Rule 2: fever = no AND cough = no
        (defrule covid-unlikely
            (symptom (name fever) (value no))
            (symptom (name cough) (value no))
            =>
            (assert (result (diagnosis
                "Unlikely to be COVID-19 based on these symptoms."))))
    """

    # Build CLIPS logic
    env.build(clips_code)

    return env


# ---------------------------------------------------------
# Run Expert System
# ---------------------------------------------------------
def run_expert_system(has_fever: bool, has_cough: bool) -> str:
    """
    Accept symptom booleans, assert facts into CLIPS,
    run inference, and return diagnosis result.
    """

    env = create_environment()
    env.reset()

    # Convert to yes/no
    fever_value = "yes" if has_fever else "no"
    cough_value = "yes" if has_cough else "no"

    # Assert CLIPS facts
    env.assert_string(f"(symptom (name fever) (value {fever_value}))")
    env.assert_string(f"(symptom (name cough) (value {cough_value}))")

    env.run()

    # Get diagnosis
    diagnosis = "No rule matched. Please consult a medical professional."
    for fact in env.facts():
        if fact.template.name == "result":
            diagnosis = fact["diagnosis"]
            break

    return diagnosis


# ---------------------------------------------------------
# Streamlit UI
# ---------------------------------------------------------
def main():
    st.title("🩺 COVID-19 Diagnosis Expert System (CLIPS + Streamlit)")

    st.write("""
        This is a simple **rule-based Expert System** using clipspy.
        It uses 2 rules to provide a basic COVID-19 assessment.
        
        ⚠️ *This is for educational purposes only.*
    """)

    st.markdown("---")
    st.header("1️⃣ Enter Your Symptoms")

    fever_choice = st.radio(
        "Do you have a fever?",
        ("No", "Yes"),
        horizontal=True,
    )

    cough_choice = st.radio(
        "Do you have a cough?",
        ("No", "Yes"),
        horizontal=True,
    )

    # Convert UI input to booleans
    has_fever = fever_choice == "Yes"
    has_cough = cough_choice == "Yes"

    st.markdown("---")
    st.header("2️⃣ Run Diagnosis")

    if st.button("🧪 Diagnose"):
        result = run_expert_system(has_fever, has_cough)
        st.success(result)

        with st.expander("Show details"):
            st.write(f"Fever: {has_fever}")
            st.write(f"Cough: {has_cough}")
            st.code(
                """
                Rule 1: IF fever=yes AND cough=yes → Possible COVID-19
                Rule 2: IF fever=no  AND cough=no  → Unlikely COVID-19
                """,
                language="text",
            )

    st.markdown("---")
    st.caption("Built for TES6313 Lab – Expert System using CLIPS + Streamlit.")


if __name__ == "__main__":
    main()
