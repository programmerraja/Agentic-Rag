"""
Docling-based document parser.
"""
import os
from typing import List, Dict, Any
from pathlib import Path
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions, TesseractOcrOptions
from parsers.base_parser import BaseParser
from llama_index.core.schema import Document


class DoclingParser(BaseParser):
    """Docling-based document parser with OCR and table structure support."""
    
    def __init__(self, enable_ocr: bool = True, table_structure: bool = True, 
                 enable_cache: bool = True, cache_dir: str = "cache", **kwargs):
        """
        Initialize Docling parser.
        
        Args:
            enable_ocr: Enable OCR processing
            table_structure: Enable table structure detection
            enable_cache: Enable caching functionality
            cache_dir: Directory to store cache files
            **kwargs: Additional configuration
        """
        super().__init__(enable_cache=enable_cache, cache_dir=cache_dir, **kwargs)
        self.enable_ocr = enable_ocr
        self.table_structure = table_structure
        self._converter = None
    
    def _get_converter(self) -> DocumentConverter:
        """Get or create document converter."""
        if self._converter is None:
            if self.enable_ocr:
                pipeline_options = PdfPipelineOptions()
                pipeline_options.do_ocr = True
                pipeline_options.do_table_structure = self.table_structure
                pipeline_options.table_structure_options.do_cell_matching = True
                
                ocr_options = TesseractOcrOptions(force_full_page_ocr=True)
                pipeline_options.ocr_options = ocr_options
                
                self._converter = DocumentConverter(
                    format_options={
                        InputFormat.PDF: PdfFormatOption(
                            pipeline_options=pipeline_options,
                        )
                    }
                )
            else:
                self._converter = DocumentConverter()
        
        return self._converter
    
    def parse(self, file_path: {str,str}, **kwargs) -> List[Document]:
        """
        Parse a document using Docling with caching support.
        
        Args:
            file_path: Path to the document to parse
            **kwargs: Additional parsing options
            
        Returns:
            List of Document objects
        """
        if not self.validate_file(file_path["path"]):
            raise ValueError(f"File {file_path['path']} is not supported by DoclingParser")
        
        # Check if document is already cached
        if self._is_cached(file_path["path"]):
            cached_markdown = self._get_cached_markdown(file_path["path"])
            if cached_markdown is not None:
                print(f"Using cached markdown for {file_path}")
                # Create Document object from cached markdown
                metadata = {
                    "plan_name": file_path["name"],
                    "parser": "docling",
                }
                document = self._create_document(cached_markdown, metadata)
                return [document]
        
        # Parse the document if not cached
        converter = self._get_converter()
        
        try:
            result = converter.convert(file_path["path"])
            doc = result.document
            
            markdown_content = doc.export_to_markdown()
            
            metadata = {
                "plan_name": file_path["name"],
                "parser": "docling",
            }
            
            document = self._create_document(markdown_content, metadata)
            documents = [document]
            
            cache_metadata = {
                "parsing_options": kwargs
            }
            self._cache_markdown(file_path["path"], markdown_content, cache_metadata)
            
            return documents
            
        except Exception as e:
            raise RuntimeError(f"Failed to parse document {file_path["path"]}: {str(e)}")
    
    def get_supported_formats(self) -> List[str]:
        """Get supported file formats."""
        return ['.pdf', '.docx', '.doc', '.txt', '.md']
    
    def get_parser_name(self) -> str:
        """Get parser name."""
        return "DoclingParser"
