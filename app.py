import json
import streamlit as st
from frontend_streamlit.image_processing import ImageProcessing, pipeline_steps

# Initialize session state
if 'pipeline_steps' not in st.session_state:
    st.session_state['pipeline_steps'] = []


st.title("Image Processing Visualization")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

new_step = st.selectbox("Add a processing step:", [list(pipeline_steps.keys())[i] for i in range(len(pipeline_steps))], key="new_step")

if st.button("Add Step"):
    # Add the selected step to the pipeline (implementation below)
    st.session_state['pipeline_steps'].append({
        "name": new_step, 
        "function": pipeline_steps[new_step]["function"],
        "params": pipeline_steps[new_step].get("params")
        })

if len(st.session_state['pipeline_steps']) > 0:
    st.subheader("Current Pipeline")

for i, step in enumerate(st.session_state['pipeline_steps']):
    cols = st.columns(4)

    with cols[0]:
        st.write(f"{i+1}. {step['name']}", key=f"step_{i}_{step['name']}")

    if len(st.session_state['pipeline_steps']) > 1:
        with cols[1]:

            if st.button("Move Up", key=f"up_{i}"):
                if i > 0:
                    st.session_state['pipeline_steps'][i], st.session_state['pipeline_steps'][i - 1] = \
                        st.session_state['pipeline_steps'][i - 1], st.session_state['pipeline_steps'][i]
        with cols[2]:
            if st.button("Move Down", key=f"down_{i}"):
                if i < len(st.session_state['pipeline_steps']) - 1:
                    st.session_state['pipeline_steps'][i], st.session_state['pipeline_steps'][i + 1] = \
                        st.session_state['pipeline_steps'][i + 1], st.session_state['pipeline_steps'][i]

    with cols[3]:
        if st.button("Remove", key=f"remove_{i}"):
            del st.session_state['pipeline_steps'][i]

if len(st.session_state['pipeline_steps']) > 0:
    if st.button("Clear Pipeline"):
        st.session_state['pipeline_steps'] = []

if uploaded_file is not None:
    image_processing = ImageProcessing(uploaded_file)
    image_processing.process_image(st.session_state['pipeline_steps'])

    list_of_steps = ['Original Image']
    list_of_steps.extend([step['name'] for step in st.session_state['pipeline_steps']])
    list_of_steps.append("All Steps")

    select_view_step = st.selectbox("See other steps:", list_of_steps)
    st.subheader(select_view_step)
    if select_view_step == "All Steps":
        for i, image in enumerate(image_processing.processed_images):
            st.markdown(list_of_steps[i])
            st.image(image, caption=f"Step {i + 1}")
    else:
        st.image(image_processing.processed_images[list_of_steps.index(select_view_step)])

    if len(st.session_state['pipeline_steps']) > 0:
        json_data = json.dumps(st.session_state['pipeline_steps'], indent=4)

        st.download_button(
            label="Download Pipeline as JSON",
            data=json_data,
            file_name="image_processing_pipeline.json",
            mime="application/json"
        )