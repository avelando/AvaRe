import csv
import ast
import re
from django.core.management.base import BaseCommand
from importer.models import FeedbackDataset, LlmsDataset

class Command(BaseCommand):
    help = "Importa feedback_dataset_filtered.csv em FeedbackDataset e llms.csv em LlmsDataset"

    def add_arguments(self, parser):
        parser.add_argument("feedback_path", type=str)
        parser.add_argument("llm_path", type=str)

    def handle(self, *args, **opts):
        pattern = re.compile(r'^[\u2022•]?\s*\d+\)\s*')
        
        with open(opts["feedback_path"], encoding="utf-8") as f_fb:
            reader_fb = csv.DictReader(f_fb)
            for row in reader_fb:
                comments = ast.literal_eval(row.get("specific_comment", "[]"))
                cleaned_comments = [pattern.sub('', comment) for comment in comments]
                
                FeedbackDataset.objects.create(
                    feedback_id=row["id"],
                    id_prompt=row.get("id_prompt"),
                    prompt=row.get("prompt"),
                    supporting_text=row.get("supporting_text"),
                    essay_title=row.get("essay_title"),
                    essay_text=row.get("essay_text"),
                    essay_year=int(row.get("essay_year") or 0) or None,
                    general_comment=row.get("general_comment"),
                    c1=cleaned_comments[0] if len(cleaned_comments) > 0 else "",
                    c2=cleaned_comments[1] if len(cleaned_comments) > 1 else "",
                    c3=cleaned_comments[2] if len(cleaned_comments) > 2 else "",
                    c4=cleaned_comments[3] if len(cleaned_comments) > 3 else "",
                    c5=cleaned_comments[4] if len(cleaned_comments) > 4 else "",
                    reference=row.get("reference"),
                )

        with open(opts["llm_path"], encoding="utf-8") as f_ll:
            reader_ll = csv.DictReader(f_ll)
            for row in reader_ll:
                LlmsDataset.objects.create(
                    topic=row.get("topic"),
                    sup_text=row.get("sup_text"),
                    essay=row.get("essay"),
                    c1=row.get("C1", ""),
                    c2=row.get("C2", ""),
                    c3=row.get("C3", ""),
                    c4=row.get("C4", ""),
                    c5=row.get("C5", ""),
                )

        self.stdout.write(self.style.SUCCESS("Importação de ambos os arquivos concluída com sucesso!"))
