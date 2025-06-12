import streamlit as st
from search.search_classical import classical_search
from search.search_best_pair import best_pair_search
from llm import generate_response

st.set_page_config(page_title="🔍 Multimodal Search The Batch")
st.image("data/the-batch-logo.webp", width=300)
st.title("Multimodal Assistant")

mode = st.selectbox("🔎 Select the search mode:", ["Classical RAG", "Multimodal RAG"])
query = st.text_input("📝 Enter the text query:")

if query:
    if mode == "Classical RAG":
        results = classical_search(query, k=3)
    else:
        results = best_pair_search(query, k=3)

    st.markdown(f"### 📄 Results found: {len(results)}")

    for i, meta in enumerate(results):
        st.markdown(f"### 🔹 Result {i + 1}")
        if meta.get("title"):
            st.markdown(f"**📖 Name:** {meta['title']}")
        if meta.get("date"):
            st.markdown(f"**📅 Date of publication:** {meta['date']}")
        if meta.get("description"):
            st.markdown(f"**📝 Description:** {meta['description']}")
        if meta.get("image_url"):
            st.image(meta["image_url"], use_container_width=True)
        if meta.get("content"):
            st.markdown("**📚 Part of the article:**")
            st.write(meta["content"][:500] + "...")
        if meta.get("source_url"):
            st.markdown(f"[🔗 Read the full article →]({meta['source_url']})")
        st.markdown("---")

    if st.button("🧠 Generate a response to a query"):
        docs = [
            {
                "title": meta.get("title", ""),
                "description": meta.get("description", ""),
                "content": meta.get("content", "")
            }
            for meta in results
        ]

        response = generate_response(query, docs)
        st.markdown("### 🤖 Generated Response:")
        st.success(response)