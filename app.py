import streamlit as st
import openai
from PIL import Image
import requests
from io import BytesIO

# Function to set OpenAI API key in the sidebar
def set_openai_api_key():
    openai_api_key = st.sidebar.text_input("Enter your OpenAI API key:", type="password", key="openai_key")
    st.sidebar.write("(You can set your API key here for future sessions.)")
    return openai_api_key

# Streamlit App
def main():
    st.title("")  # Empty title to make room for the container

    # Create a layout with two columns
    col1, col2 = st.columns(2)

    # Add a logo to the first column
    logo = Image.open(r"logo.png")  # Replace with the path to your logo image
    col1.image(logo, use_column_width=True)

    # Add the app name to the second column
    col2.title("AI Image Generator Demo")

    # Set OpenAI API key in the sidebar
    openai_api_key = set_openai_api_key()

    # User input prompt
    prompt = st.text_input("Enter your prompt:")

    # Slider for controlling the number of images to generate
    num_images = st.slider("Number of Images", 1, 5, 1)

    # Check if API key, prompt, and number of images are provided
    if openai_api_key and prompt and num_images:

        # Initialize OpenAI client with the provided API key
        openai.api_key = openai_api_key  # Set the API key for the OpenAI library

        # Generate button
        if st.button(f"Generate {'Image' if num_images == 1 else 'Images'}"):
            try:
                # Generate image(s) using DALL-E 3
                image_urls = []

                for _ in range(num_images):
                    response = openai.Image.create(
                        model="dall-e-3",
                        prompt=prompt,
                        size="1024x1024",
                        quality="standard",
                        n=1,
                    )
                    image_urls.append(response['data'][0]['url'])

                # Display disclaimer text
                st.text("Disclaimer: This is just for demo purposes only.")

                # Display generated images in vertical boxes
                for i, image_url in enumerate(image_urls):
                    col1, col2 = st.columns(2)
                    generated_image = Image.open(BytesIO(requests.get(image_url).content))
                    col1.image(generated_image, caption=f"Generated Image {i + 1}/{num_images}", use_column_width=True)

            except Exception as e:
                st.error(f"Error generating images: {e}")
    else:
        st.warning("Please enter the OpenAI API key, a prompt, and select the number of images before generating.")

if __name__ == "__main__":
    main()