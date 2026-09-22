import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from google import genai
from google.genai import types

from src.pii_redaction.presidio_service import ClinicalPIIRedactor
from nemoguardrails import RailsConfig, LLMRails

load_dotenv()

class GeminiClinicalRAGEngine:
    def __init__(self):
        print("⏳ Booting Enterprise Zero-Trust Pipeline Middlewares...")
        
        # 1. Initialize Safeguard Layers
        self.redactor = ClinicalPIIRedactor()
        config = RailsConfig.from_path("./src/guardrails")
        self.rails = LLMRails(config)
        
        # 2. Boot Local ModernBERT Model for vector queries
        self.embedder = SentenceTransformer('NeuML/bioclinical-modernbert-base-embeddings')
        
        # 3. Configure Gemini SDK natively
        gemini_key = os.getenv("GEMINI_API_KEY")
        if not gemini_key:
            raise ValueError("❌ Missing GEMINI_API_KEY environment variable in your .env profile.")
        
        self.ai_client = genai.Client(api_key=gemini_key)
        self.model_name = "gemini-3.6-flash"
        print(f"✅ Google Gemini Connected. Production Sandbox Engine: {self.model_name}")

    def _get_db_engine(self):
        db_user = os.getenv("DB_USER", "fde_admin")
        db_pass = os.getenv("DB_PASSWORD", "SecureEHR2026!")
        db_host = os.getenv("DB_HOST", "3.7.80.38")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME", "ehr_db")
        
        DB_URL = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        return create_engine(DB_URL, pool_pre_ping=True)

    def generate_clinical_insight(self, patient_id: str, user_question: str) -> str:
        try:
            # 1. Convert user question into a 768-dim vector array
            query_vector = self.embedder.encode(user_question).tolist()
            
            # 2. Extract context via pgvector similarity search from your AWS database
            engine = self._get_db_engine()
            with engine.connect() as conn:
                # Optimized query matching your exact verification file columns
                query = text("""
                    SELECT drug, admission_type, drg_severity, description, comments 
                    FROM patient_encounters 
                    WHERE subject_id = :subject_id AND clinical_embedding IS NOT NULL
                    ORDER BY clinical_embedding <=> CAST(:query_embedding AS vector(768))
                    LIMIT 3;
                """)
                
                result = conn.execute(query, {
                    "subject_id": int(patient_id),
                    "query_embedding": str(query_vector)
                })
                rows = result.fetchall()
                
                if not rows:
                    return f"⚠️ System Alert: No historical embedded records found in AWS for Patient ID {patient_id}."
                
                context_lines = []
                for row in rows:
                    context_lines.append(
                        f"Drug: {row.drug} | Admission: {row.admission_type} | Severity: {row.drg_severity} | "
                        f"Diagnosis: {row.description} | Notes: {row.comments}"
                    )
                real_db_context = f"[Sanitized Records for Subject ID: {patient_id}]\n" + "\n".join(context_lines)

            # 3. Anonymize data arrays using Microsoft Presidio (PHI/PII scrubbing)
            safe_context = self.redactor.redact_clinical_context(raw_text=real_db_context)
            
            # 4. Formulate the composite retrieval prompt block
            augmented_prompt = f"Clinical Context:\n{safe_context}\n\nUser Question: {user_question}"
            
            # 5. Evaluate semantic boundaries using NeMo Guardrails
            nemo_messages = [{"role": "user", "content": augmented_prompt}]
            guardrail_check = self.rails.generate(messages=nemo_messages)
            
            # Check if safety rails triggered our prescriptive advice refusal block
            if "I am an enterprise EHR retrieval system" in guardrail_check['content']:
                return f"🛡️ [Guardrail Intercepted Action]: {guardrail_check['content']}"

            # 6. Execute direct API generation via official SDK if guardrails allow it
            response = self.ai_client.models.generate_content(
                model=self.model_name,
                contents=augmented_prompt,
                config=types.GenerateContentConfig(
                    system_instruction="You are a secure, enterprise clinical AI assistant. Rely strictly on the provided context.",
                    temperature=0.1,
                    max_output_tokens=512
                )
            )
            return response.text.strip()

        except Exception as e:
            return f"❌ Execution error in Gemini RAG engine: {str(e)}"
