import os
import pdfminer.high_level
from typing import List, Tuple
from pdf2image import convert_from_path
import pytesseract
import logging

logger = logging.getLogger(__name__)

class FileProcessor:
    @staticmethod
    def extract_text_from_pdf(pdf_path: str) -> str:
        """Extract text from PDF using pdfminer.six with OCR fallback"""
        try:
            # First try pdfminer
            text = pdfminer.high_level.extract_text(pdf_path)
            if len(text.strip()) > 100:
                return text
            
            # Fallback to OCR if text extraction fails
            logger.info("Falling back to OCR for text extraction")
            images = convert_from_path(pdf_path)
            ocr_text = " ".join([pytesseract.image_to_string(image) for image in images])
            return ocr_text
        except Exception as e:
            logger.error(f"Text extraction failed: {str(e)}")
            raise Exception(f"Failed to extract text: {str(e)}")
    
    @staticmethod
    async def process_uploaded_files(files: List[Tuple[str, bytes]]) -> List[dict]:
        processed_files = []
        temp_dir = "temp_uploads"
        os.makedirs(temp_dir, exist_ok=True)
        
        for filename, file_bytes in files:
            temp_path = os.path.join(temp_dir, filename)
            try:
                with open(temp_path, "wb") as f:
                    f.write(file_bytes)
                
                text_content = FileProcessor.extract_text_from_pdf(temp_path)
                processed_files.append({
                    "filename": filename,
                    "content": text_content
                })
            except Exception as e:
                logger.error(f"Failed to process file {filename}: {str(e)}")
                processed_files.append({
                    "filename": filename,
                    "content": "",
                    "error": str(e)
                })
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
        
        return processed_files