# ── MUST BE FIRST: fix tesseract path on Windows ──
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

import os
os.environ.pop("HTTP_PROXY", None)
os.environ.pop("HTTPS_PROXY", None)
os.environ.pop("http_proxy", None)
os.environ.pop("https_proxy", None)


def process_images_with_captions(raw_chunks, use_ollama=True, model_name="llava"):
    import requests
    from unstructured.documents.elements import FigureCaption, Image

    OLLAMA_URL = "http://localhost:11434/api/generate"

    def query_ollama(model, prompt, image_base64):
        payload = {
            "model": model,
            "prompt": prompt,
            "images": [image_base64],
            "stream": False,
        }
        response = requests.post(OLLAMA_URL, json=payload, timeout=300)
        response.raise_for_status()
        return response.json()["response"]

    processed_images = []
    encountered_errors = []

    for idx, chunk in enumerate(raw_chunks):
        if isinstance(chunk, Image):
            if idx + 1 < len(raw_chunks) and isinstance(raw_chunks[idx + 1], FigureCaption):
                caption = raw_chunks[idx + 1].text
            else:
                caption = "No caption available"

            image_data = {
                "caption": caption,
                "image_text": chunk.text if hasattr(chunk, "text") else "",
                "base64_image": chunk.metadata.image_base64,
                "content": chunk.text if hasattr(chunk, "text") else "",
                "content_type": "image",
                "filename": chunk.metadata.filename if hasattr(chunk, "metadata") else "",
            }

            error_data = {"error": None, "error_message": None}

            if use_ollama:
                try:
                    prompt = (
                        f"Generate a comprehensive and detailed description of this image from a technical document about Retrieval-Augmented Generation (RAG).\n\n"
                        f"CONTEXT INFORMATION:\n"
                        f"- Caption: {caption}\n"
                        f"- Text extracted from image: {chunk.text if hasattr(chunk, 'text') else 'No text'}\n\n"
                        f"DESCRIPTION REQUIREMENTS:\n"
                        f"1. Begin with a clear overview of what the image shows (diagram, chart, architecture, etc.)\n"
                        f"2. If it's a diagram or flowchart: describe components, connections, data flow direction, and system architecture\n"
                        f"3. If it's a chart or graph: explain axes, trends, key data points, and significance\n"
                        f"4. Explain technical terminology and abbreviations that appear in the image\n"
                        f"5. Interpret how this visual relates to RAG concepts and implementation\n"
                        f"6. Include any numerical data, performance metrics, or comparative results shown\n"
                        f"7. Target length: 150-300 words for complex diagrams, 100-150 words for simpler images\n\n"
                        f"Focus on providing information that would be valuable in a technical context for someone implementing or researching RAG systems."
                    )

                    description = query_ollama(model_name, prompt, chunk.metadata.image_base64)
                    image_data["content"] = description

                except requests.exceptions.ConnectionError:
                    msg = "Could not connect to Ollama. Make sure Ollama is running: 'ollama serve'"
                    print(f"Warning: {msg}")
                    error_data["error"] = "ConnectionError"
                    error_data["error_message"] = msg
                    encountered_errors.append(error_data)

                except Exception as e:
                    print(f"Warning: Error generating description: {str(e)}")
                    error_data["error"] = str(e)
                    error_data["error_message"] = "Error generating description with Ollama."
                    encountered_errors.append(error_data)

            processed_images.append(image_data)

    print(f"Processed {len(processed_images)} images with captions and descriptions")
    print(f"Errors encountered: {len(encountered_errors)}")
    return processed_images, encountered_errors


def process_tables_with_descriptions(raw_chunks, model_name="gemma3:4b"):
    import requests
    from unstructured.documents.elements import Table

    OLLAMA_URL = "http://localhost:11434/api/generate"

    processed_tables = []
    encountered_errors = []

    for idx, chunk in enumerate(raw_chunks):
        if isinstance(chunk, Table):
            table_data = {
                "table_as_html": chunk.metadata.text_as_html,
                "table_text": chunk.text,
                "content": chunk.text,
                "content_type": "table",
                "filename": chunk.metadata.filename if hasattr(chunk, "metadata") else "",
            }

            try:
                payload = {
                    "model": model_name,
                    "prompt": (
                        f"Analyze the following table from a technical document about Retrieval-Augmented Generation (RAG) "
                        f"and provide a detailed summary of its contents, including the structure, key data points, "
                        f"and any notable trends or insights.\n\n"
                        f"TABLE HTML:\n{chunk.metadata.text_as_html}\n\n"
                        f"REQUIREMENTS:\n"
                        f"1. Provide an overview of the table's purpose in the context of RAG.\n"
                        f"2. Explain the significance of each column and row, including key metrics.\n"
                        f"3. Describe trends, comparisons, or notable findings.\n"
                        f"4. Target length: 150-300 words.\n"
                        f"Directly return the summary without preamble."
                    ),
                    "stream": False,
                    "options": {"temperature": 0.2},
                }

                response = requests.post(OLLAMA_URL, json=payload, timeout=300)
                response.raise_for_status()
                table_data["content"] = response.json().get("response", "No response from model")

            except requests.exceptions.ConnectionError:
                msg = "Could not connect to Ollama. Make sure Ollama is running: 'ollama serve'"
                print(f"Warning: {msg}")
                encountered_errors.append({"error": "ConnectionError", "error_message": msg})

            except Exception as e:
                print(f"Warning: Error generating table description: {str(e)}")
                encountered_errors.append({
                    "error": str(e),
                    "error_message": "Error generating description with Ollama.",
                })

            processed_tables.append(table_data)

    print(f"Processed {len(processed_tables)} tables with descriptions")
    print(f"Errors encountered: {len(encountered_errors)}")
    return processed_tables, encountered_errors


def create_semantic_chunks(chunks):
    from unstructured.documents.elements import CompositeElement

    processed_chunks = []
    for idx, chunk in enumerate(chunks):
        if isinstance(chunk, CompositeElement):
            chunk_data = {
                "content": chunk.text,
                "content_type": "text",
                "filename": chunk.metadata.filename if hasattr(chunk, "metadata") else "",
            }
            processed_chunks.append(chunk_data)

    print(f"Created {len(processed_chunks)} semantic chunks from document")
    return processed_chunks


if __name__ == "__main__":
    print("Starting script...")
    from unstructured.partition.pdf import partition_pdf

    pdf_file_path = "files/RRGLLM.pdf"

    # 1. Extract raw chunks
    raw_chunks = partition_pdf(
        filename=pdf_file_path,
        strategy="hi_res",
        infer_table_structure=True,
        extract_image_block_types=["Image", "Figure", "Table"],
        extract_image_block_to_payload=True,
        chunking_strategy=None,
    )

    # 2. Process images with captions (uses llava)
    processed_images, image_errors = process_images_with_captions(raw_chunks)

    # 3. Process tables with descriptions (uses gemma3:4b)
    # processed_tables, table_errors = process_tables_with_descriptions(raw_chunks)

    # 4. Partition the PDF into chunks
    # chunks = partition_pdf(
    #     filename=pdf_file_path,
    #     strategy="hi_res",
    #     chunking_strategy="by_title",
    #     max_characters=2000,
    #     min_chars_to_combine=500,
    #     chars_before_new_chunk=1500,
    # )

    # 5. Create semantic chunks
    # semantic_chunks = create_semantic_chunks(chunks)
    # print(f"Extracted {len(semantic_chunks)} semantic chunks from the document")