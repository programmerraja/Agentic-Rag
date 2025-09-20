from docling.document_converter import DocumentConverter

# Initialize converter
converter = DocumentConverter()

# Convert your PDF
path = "../../documents/Family Health Optima Insurance Plan.pdf"
result = converter.convert(path)
doc = result.document

# Export to markdown
markdown_content = doc.export_to_markdown()
# print(markdown_content)
open("family_health_optima_insurance_plan.md", "w").write(markdown_content)

# # Export to JSON (structured format)
# json_content = doc.export_to_json()
# open("doclling_json.json", "w").write(json_content)

# # Export to HTML
# html_content = doc.export_to_html()
# open("doclling_html.html", "w").write(html_content)
