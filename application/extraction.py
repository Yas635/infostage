"""Extraction automatique du texte des rapports (PDF et Word) à l'import."""
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

MAX_CHARS = 1_000_000  # garde-fou pour les très gros documents


def extract_text(uploaded_file) -> str:
    """Retourne le texte d'un fichier PDF ou DOCX ; chaîne vide sinon.

    Ne lève jamais d'exception : un fichier illisible ne doit pas bloquer l'import.
    Le curseur du fichier est remis au début pour permettre son enregistrement.
    """
    suffix = Path(getattr(uploaded_file, "name", "")).suffix.lower()
    text = ""
    try:
        uploaded_file.seek(0)
        if suffix == ".pdf":
            from pdfminer.high_level import extract_text as pdf_extract

            text = pdf_extract(uploaded_file)
        elif suffix == ".docx":
            from docx import Document

            doc = Document(uploaded_file)
            parts = [p.text for p in doc.paragraphs]
            for table in doc.tables:
                for row in table.rows:
                    parts.extend(cell.text for cell in row.cells)
            text = "\n".join(parts)
    except Exception:  # noqa: BLE001
        logger.warning("Extraction impossible pour %s", getattr(uploaded_file, "name", "?"), exc_info=True)
        text = ""
    finally:
        try:
            uploaded_file.seek(0)
        except Exception:  # noqa: BLE001
            pass
    return (text or "").replace("\x00", "").strip()[:MAX_CHARS]
