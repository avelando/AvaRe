from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.db import transaction
from importer.models import FeedbackDataset, LlmsDataset, UserResponse, UserProfile

@require_POST
def save_response(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("compare-start")
    try:
        user_profile = UserProfile.objects.get(pk=user_id)
    except UserProfile.DoesNotExist:
        return redirect("compare-start")

    feedback_id = request.POST.get("feedback_id")
    llm_id = request.POST.get("llm_id")
    if not (feedback_id and llm_id):
        return redirect("compare-detail")
    
    choices = [request.POST.get(f"choice_{i}") for i in range(1, 6)]
    if not all(choices):
        return redirect("compare-detail")
    
    try:
        feedback = FeedbackDataset.objects.get(pk=feedback_id)
        llm = LlmsDataset.objects.get(pk=llm_id)
    except (FeedbackDataset.DoesNotExist, LlmsDataset.DoesNotExist):
        return redirect("compare-detail")

    with transaction.atomic():
        response, created = UserResponse.objects.update_or_create(
            user=user_profile,
            feedback=feedback,
            llm=llm,
            defaults={
                "choice_c1": choices[0],
                "choice_c2": choices[1],
                "choice_c3": choices[2],
                "choice_c4": choices[3],
                "choice_c5": choices[4],
            }
        )
    try:
        page_number = int(request.POST.get("page_number", "1"))
    except ValueError:
        page_number = 1
    if page_number < 44:
        next_page = page_number + 1
        return redirect(f"/compare/questions/?page={next_page}")
    else:
        return redirect("/complete/")
    

def complete(request):
    return render(request, "complete.html")