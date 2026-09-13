import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000/ask"


st.set_page_config(
    page_title="Zepto Support Assistant",
    page_icon="🛒",
    layout="centered",
)


st.title("🛒 Zepto Support Assistant")
st.write("Ask questions about Zepto delivery, returns, refunds, membership, and more.")


question = st.text_area(
    "Enter your question",
    placeholder="Can I cancel my order after it is packed?",
    height=100,
)


if st.button("Ask Assistant", type="primary"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        try:
            with st.spinner("Finding the best answer..."):
                response = requests.post(
                    API_URL,
                    json={"query": question},
                    timeout=30,
                )

            if response.status_code == 200:
                result = response.json()

                st.subheader("Answer")
                st.write(result["answer"])

                st.subheader("Sources")
                if result["sources"]:
                    for source in result["sources"]:
                        st.write(f"- {source}")
                else:
                    st.write("No source documents available.")

                st.metric(
                    "Confidence",
                    f"{result['confidence']:.0%}",
                )
            else:
                st.error(
                    f"API request failed with status code "
                    f"{response.status_code}"
                )

        except requests.exceptions.ConnectionError:
            st.error(
                "Could not connect to the FastAPI server. "
                "Please start the backend first."
            )
        except requests.exceptions.Timeout:
            st.error("The request timed out. Please try again.")