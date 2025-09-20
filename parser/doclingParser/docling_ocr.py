from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions, TesseractOcrOptions

pipeline_options = PdfPipelineOptions()
pipeline_options.do_ocr = True
pipeline_options.do_table_structure = True
pipeline_options.table_structure_options.do_cell_matching = True

ocr_options = TesseractOcrOptions(force_full_page_ocr=True)
pipeline_options.ocr_options = ocr_options

converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(
            pipeline_options=pipeline_options,
        )
    }
)

# Convert document
result = converter.convert("../../documents/Imperial Dynamic Plan (HMO) 012-8-18.pdf")
doc = result.document
markdown_content = doc.export_to_markdown()
print(markdown_content)
