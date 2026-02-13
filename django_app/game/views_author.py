from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import StoryForm
from .services import flask_api
from .models import StoryOwnership

@login_required
def create_story(request):
    if not request.user.profile.is_author:
        return render(request, "403.html")

    if request.method == "POST":
        form = StoryForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # 1. Create story in Flask
            story = flask_api.create_story(data)

            # 2. Store ownership in Django
            StoryOwnership.objects.create(
                user=request.user,
                flask_story_id=story["id"]
            )

            return redirect("edit_story", story_id=story["id"])
    else:
        form = StoryForm()

    return render(request, "game/author/create_story.html", {"form": form})

@login_required
def edit_story(request, story_id):
    if not user_owns_story(request.user, story_id):
        return render(request, "403.html")

    story = flask_api.get_story(story_id)

    if request.method == "POST":
        form = StoryForm(request.POST)
        if form.is_valid():
            flask_api.update_story(story_id, form.cleaned_data)
            return redirect("edit_story", story_id=story_id)
    else:
        form = StoryForm(initial=story)

    return render(request, "game/author/edit_story.html", {
        "form": form,
        "story": story
    })


@login_required
def delete_story(request, story_id):
    if not user_owns_story(request.user, story_id):
        return render(request, "403.html")

    if request.method == "POST":
        flask_api.delete_story(story_id)
        StoryOwnership.objects.filter(flask_story_id=story_id).delete()
        return redirect("author_dashboard")

    return render(request, "game/author/confirm_delete.html")

@login_required
def create_page(request, story_id):
    if not user_owns_story(request.user, story_id):
        return render(request, "403.html")

    if request.method == "POST":
        form = PageForm(request.POST)
        if form.is_valid():
            flask_api.create_page(story_id, form.cleaned_data)
            return redirect("edit_story", story_id=story_id)
    else:
        form = PageForm()

    return render(request, "game/author/create_page.html", {"form": form})

@login_required
def create_choice(request, page_id):
    page = flask_api.get_page(page_id)
    story_id = page["story_id"]

    if not user_owns_story(request.user, story_id):
        return render(request, "403.html")

    if request.method == "POST":
        form = ChoiceForm(request.POST)
        if form.is_valid():
            flask_api.create_choice(page_id, form.cleaned_data)
            return redirect("edit_story", story_id=story_id)
    else:
        form = ChoiceForm()

    return render(request, "game/author/create_choice.html", {"form": form})

@api_bp.post("/stories/<int:story_id>/pages")
def create_page(story_id):
    data = request.json
    page = Page(
        story_id=story_id,
        text=data["text"],
        is_ending=data.get("is_ending", False),
        ending_label=data.get("ending_label"),
        illustration_url=data.get("illustration_url")
    )
    db.session.add(page)
    db.session.commit()
    return jsonify({"id": page.id}), 201


@api_bp.post("/pages/<int:page_id>/choices")
def create_choice(page_id):
    data = request.json
    choice = Choice(
        page_id=page_id,
        text=data["text"],
        next_page_id=data["next_page_id"]
    )
    db.session.add(choice)
    db.session.commit()
    return jsonify({"id": choice.id}), 201

@api_bp.post("/stories")
def create_story():
    data = request.json
    story = Story(
        title=data["title"],
        description=data.get("description"),
        illustration_url=data.get("illustration_url"),
        status="draft"
    )
    db.session.add(story)
    db.session.commit()
    return jsonify({"id": story.id}), 201


