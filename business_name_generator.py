import streamlit as st
import openai
import os

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to generate business names
def generate_business_names(business_type, target_audience, branding_tone, keywords, max_words, num_names):
    """
    Generates business names based on user input with a strict word limit.
    """
    prompt = (
        f"I need {num_names} creative and unique business name suggestions for a {business_type}. "
        f"The target audience is {target_audience}. The branding tone should be {branding_tone}. "
        f"Include the following keywords: {keywords}. Each name should be no more than {max_words} words long. "
        "Provide only the names, separated by commas."
    )
    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )
    names = response['choices'][0]['message']['content']
    # Parse and filter names to ensure word limit
    filtered_names = [name.strip() for name in names.split(",") if len(name.split()) <= max_words]
    return filtered_names

# Streamlit app
st.title("💡 Business Name Generator")
st.markdown("### Generate creative and relevant names for your business idea!")

# Sidebar Information
st.sidebar.header("🤖 About the Model")
st.sidebar.markdown(
    """
    - **Model Used**: GPT-3.5 Turbo  
    - **Capabilities**: Generates human-like text, perfect for creative tasks.  
    - **Output Length**: Names are concise, limited to user-defined word length.  
    """
)

# Collect user inputs
st.header("Enter Details About Your Business")
business_type = st.text_input("Type of Business", "e.g., Coffee shop, Tech startup")
target_audience = st.text_input("Target Audience", "e.g., Eco-conscious millennials, Pet lovers")
branding_tone = st.text_input("Branding Tone", "e.g., Playful, Professional, Modern")
keywords = st.text_input("Keywords to Include (comma-separated)", "e.g., green, eco, tech")
max_words = 5  # Fixed maximum word limit
num_names = st.slider("Number of Names to Generate", min_value=1, max_value=5, value=3)

# Generate names on button click
if st.button("Generate Business Names"):
    if business_type and target_audience and branding_tone:
        with st.spinner("Generating creative names..."):
            names = generate_business_names(business_type, target_audience, branding_tone, keywords, max_words, num_names)
        st.subheader("Here are your business name ideas:")
        if names:
            for i, name in enumerate(names, 1):
                st.write(f"{i}. {name}")
        else:
            st.warning("No names were generated with the specified criteria. Try relaxing the inputs!")
    else:
        st.error("Please fill in all required fields!")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using [Streamlit](https://streamlit.io/) and OpenAI's GPT-3.5.")
