import streamlit as st
import ollama

st.set_page_config(
    page_title="AI Event Planner",
    page_icon="🎉",
    layout="wide"
)

st.title("🎉 AI Event Planner")
st.write("✨ Plan your perfect event with AI!")

st.divider()

# Event Details

st.header("📝 Event Details")

event_name = st.text_input(
    "🎉 Event Name",
    placeholder="Example: Annual College Fest"
)

event_type = st.selectbox(
    "📌 Event Type",
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

location = st.text_input(
    "📍 Location",
    placeholder="Example: Hyderabad"
)

col1, col2 = st.columns(2)

with col1:

    guests = st.number_input(
        "👥 Number of Guests",
        min_value=1,
        value=50,
        step=10
    )

with col2:

    budget = st.number_input(
        "💰 Budget (₹)",
        min_value=1000,
        value=50000,
        step=5000
    )

theme = st.text_input(
    "🎨 Theme",
    placeholder="Example: Modern, Traditional, Colorful"
)

requirements = st.text_area(
    "📋 Special Requirements",
    placeholder="Example: Vegetarian food, DJ, photography, games..."
)

st.divider()


# Generate Event Plan

if st.button("✨ Generate Event Plan"):

    if event_name == "":
        st.warning("⚠️ Please enter the event name.")

    elif location == "":
        st.warning("⚠️ Please enter the location.")

    else:

        st.success("🎉 Event details received!")

        # Event Details

        st.header("📋 Event Overview")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "🎉 Event",
                event_name
            )

        with col2:
            st.metric(
                "👥 Guests",
                guests
            )

        with col3:
            st.metric(
                "💰 Budget",
                f"₹{budget:,.0f}"
            )

        with col4:
            st.metric(
                "📍 Location",
                location
            )

        st.divider()

        # Budget

        st.header("💰 Suggested Budget")

        venue = budget * 0.25
        food = budget * 0.35
        decoration = budget * 0.15
        entertainment = budget * 0.10
        photography = budget * 0.10
        miscellaneous = budget * 0.05

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "🏛️ Venue",
                f"₹{venue:,.0f}"
            )

        with col2:
            st.metric(
                "🍽️ Food",
                f"₹{food:,.0f}"
            )

        with col3:
            st.metric(
                "🎨 Decoration",
                f"₹{decoration:,.0f}"
            )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "🎵 Entertainment",
                f"₹{entertainment:,.0f}"
            )

        with col2:
            st.metric(
                "📸 Photography",
                f"₹{photography:,.0f}"
            )

        with col3:
            st.metric(
                "📦 Miscellaneous",
                f"₹{miscellaneous:,.0f}"
            )

        st.divider()

        # AI Prompt

        prompt = f"""
You are a professional AI event planner.

Create a complete event plan for:

Event Name: {event_name}
Event Type: {event_type}
Location: {location}
Number of Guests: {guests}
Budget: ₹{budget}
Theme: {theme}
Special Requirements: {requirements}

Give the plan in these sections:

1. 🎯 Event Summary
2. 🕒 Event Schedule
3. 🍽️ Catering Suggestions
4. 🎨 Decoration Ideas
5. 🎵 Entertainment Ideas
6. 📸 Photography Ideas
7. ✅ Event Checklist
8. 💡 AI Recommendations

Make the suggestions practical and suitable for the given budget,
number of guests and event type.
"""

        # Ollama

        try:

            with st.spinner(
                "🤖 Ollama is creating your event plan..."
            ):

                response = ollama.chat(
                    model="llama3.2",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

            plan = response["message"]["content"]

            st.success(
                "✨ Your AI Event Plan is Ready!"
            )

            st.header("🤖 AI Generated Event Plan")

            st.write(plan)

            st.divider()

            st.download_button(
                "📥 Download Event Plan",
                plan,
                file_name="AI_Event_Plan.txt",
                mime="text/plain"
            )

        except Exception:

            st.error(
                "❌ Could not connect to Ollama."
            )

            st.info(
                "Please start Ollama using:"
            )

            st.code(
                "ollama run llama3.2"
            )