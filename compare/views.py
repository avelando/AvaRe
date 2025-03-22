import random
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from importer.models import FeedbackDataset, LlmsDataset, UserProfile, UserResponse

def start(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        if not username:
            return render(request, "start.html", {"error": "Por favor, digite um nome."})

        user_profile, created = UserProfile.objects.get_or_create(name=username)

        request.session["user_id"] = user_profile.id

        return redirect("compare-detail")

    return render(request, "start.html")


def compare_detail(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("compare-start")
    user_profile = UserProfile.objects.get(pk=user_id)

    pairs = []
    for fb in FeedbackDataset.objects.all():
        match = LlmsDataset.objects.filter(
            topic=fb.id_prompt,
            sup_text=fb.supporting_text,
            essay=fb.essay_text
        ).first()
        if match:
            rows = []
            for i in range(1, 6):
                human = getattr(fb, f"c{i}")
                ia = getattr(match, f"c{i}")
                if random.choice([True, False]):
                    left = {"text": human, "origin": "human"}
                    right = {"text": ia, "origin": "ia"}
                else:
                    left = {"text": ia, "origin": "ia"}
                    right = {"text": human, "origin": "human"}
                rows.append({"left": left, "right": right})
            try:
                response = UserResponse.objects.get(user=user_profile, feedback=fb, llm=match)
            except UserResponse.DoesNotExist:
                response = None
            pairs.append({"feedback": fb, "llm": match, "rows": rows, "response": response})

    pairs = pairs[:44]
    if len(pairs) < 44:
        pairs.extend([None] * (44 - len(pairs)))

    paginator = Paginator(pairs, 1)
    page_number = request.GET.get("page", 1)
    try:
        page_number = int(page_number)
    except ValueError:
        page_number = 1
    if page_number > 44:
        page_number = 44
    page = paginator.page(page_number)
    return render(request, "common_list.html", {"page": page})
