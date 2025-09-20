from llmsherpa.readers import LayoutPDFReader

path = "../documents/Imperial Dynamic Plan (HMO) 012-8-18.pdf"
# url of the llmsherpa api 
pdf_reader = LayoutPDFReader("https://readers.llmsherpa.com/api/document/developer/parseDocument?renderFormat=all")
doc = pdf_reader.read_pdf(path)

print(doc)