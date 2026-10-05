import streamlit as st

st.set_page_config(
    page_title="AI Event Planner",
    page_icon="🎉",
    layout="wide"
)

st.title("🎉 AI Event Planner")
st.write("Plan your perfect event with AI!")

event_name = st.text_input("Event Name")

event_type = st.selectbox(
    "Event Type",
    [
        "Birthday",
        "Wedding",
        "College Event",
        "Corporate Event",
        "Conference",
        "Workshop",
        "Party"
    ]
)

location = st.text_input("Location")

guests = st.number_input(
    "Number of Guests",
    min_value=1,
    value=50
)

budget = st.number_input(
    "Budget (₹)",
    min_value=1000,
    value=50000
)

theme = st.text_input("Theme")

requirements = st.text_area(
    "Special Requirements"
)

if st.button("✨ Generate Event Plan"):
    st.success("Event plan generated!")

    st.subheader("📋 Event Details")

    st.write("**Event:**", event_name)
    st.write("**Type:**", event_type)
    st.write("**Location:**", location)
    st.write("**Guests:**", guests)
    st.write("**Budget:** ₹", budget)
    st.write("**Theme:**", theme)

    st.subheader("💰 Suggested Budget")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Venue", f"₹{budget * 0.25:,.0f}")

    with col2:
        st.metric("Food", f"₹{budget * 0.35:,.0f}")

    with col3:
        st.metric("Decoration", f"₹{budget * 0.15:,.0f}")