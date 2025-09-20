from docling.datamodel import vlm_model_specs
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import VlmPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.pipeline.vlm_pipeline import VlmPipeline

# Use the latest Granite-Docling model
pipeline_options = VlmPipelineOptions(
    vlm_options=vlm_model_specs.GRANITEDOCLING_MLX,  # For Mac with MPS
    # vlm_options=vlm_model_specs.GRANITEDOCLING_TRANSFORMERS,  # For general use
)

converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(
            pipeline_cls=VlmPipeline,
            pipeline_options=pipeline_options,
        ),
    }
)

# Convert your PDF
source = "../documents/Imperial Dynamic Plan (HMO) 012-8-18.pdf"
doc = converter.convert(source=source).document
print(doc.export_to_markdown())
