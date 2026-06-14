import streamlit as st

# Import your recipe data
from recipe_data import RECIPES_DATA

st.set_page_config(
    page_title="Recipe Premix Explorer",
    page_icon="🍽️",
    layout="wide"
)

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("🍽️ Recipe Explorer")

search_text = st.sidebar.text_input(
    "🔍 Search Recipe",
    placeholder="Type recipe name..."
)

categories = sorted(
    list(set(recipe["category"] for recipe in RECIPES_DATA))
)

selected_category = st.sidebar.selectbox(
    "Select Category",
    ["All"] + categories
)

# -----------------------------
# FILTER RECIPES
# -----------------------------
filtered_recipes = RECIPES_DATA

if selected_category != "All":
    filtered_recipes = [
        r for r in filtered_recipes
        if r["category"] == selected_category
    ]

if search_text:
    filtered_recipes = [
        r for r in filtered_recipes
        if search_text.lower() in r["name"].lower()
    ]

if not filtered_recipes:
    st.warning("No recipes found.")
    st.stop()

recipe_names = [r["name"] for r in filtered_recipes]

selected_recipe_name = st.sidebar.selectbox(
    "Choose Recipe",
    recipe_names
)

recipe = next(
    r for r in filtered_recipes
    if r["name"] == selected_recipe_name
)

# -----------------------------
# HEADER
# -----------------------------
st.title(f"🍽️ {recipe['name']}")

st.markdown(f"""
### 📖 About

{recipe['about']}
""")

col1, col2 = st.columns(2)

with col1:
    st.success(f"📂 Category: {recipe['category']}")

with col2:
    st.info(f"📦 Shelf Life: {recipe['shelf']}")

st.divider()

# -----------------------------
# TABS
# -----------------------------
tab1, tab2, tab3 = st.tabs(
    ["🛒 Premix", "🍳 Cooking", "💡 Tips"]
)

# -----------------------------
# PREMIX TAB
# -----------------------------
with tab1:

    st.subheader("🧂 Premix Ingredients")

    for item in recipe["premix"]:
        st.checkbox(item, key=f"premix_{item}")

    st.subheader("🏭 Premix Preparation")

    for i, step in enumerate(recipe["premix_steps"], start=1):
        with st.expander(f"Step {i}"):
            st.write(step)

# -----------------------------
# COOKING TAB
# -----------------------------
with tab2:

    st.subheader("🛒 Additional Ingredients")

    for item in recipe["cook_ingr"]:
        st.checkbox(item, key=f"cook_{item}")

    st.subheader("👨‍🍳 Cooking Instructions")

    for i, step in enumerate(recipe["cook_steps"], start=1):

        st.markdown(
            f"""
            ### Step {i}

            {step}
            """
        )

# -----------------------------
# TIPS TAB
# -----------------------------
with tab3:

    st.subheader("💡 Chef's Tip")

    st.success(recipe["tip"])

    st.subheader("📦 Shelf Life")

    st.info(recipe["shelf"])

# -----------------------------
# BOTTOM CARD
# -----------------------------
st.divider()

st.markdown(
    f"""
    ### 🎯 Quick Summary

    **Recipe:** {recipe['name']}

    **Category:** {recipe['category']}

    **Shelf Life:** {recipe['shelf']}

    **Tip:** {recipe['tip']}
    """
)